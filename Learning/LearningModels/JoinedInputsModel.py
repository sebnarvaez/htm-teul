#!python2
#-*- coding: utf-8 -*-
#  LearningModels.py
#  Author: Larvasapiens <sebastian.narvaez@correounivalle.edu.co>
#  Created: 2015-09-30
#  Last Modification: 2015-11-22
#  Version: 1.2
#
#  Copyright (C) {2016}  {Sebastián Narváez Rodríguez}
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from __future__ import print_function

import time
import numpy

from Utils.CLAClassifierCond import CLAClassifierCond
from nupic.research.spatial_pooler import SpatialPooler
from nupic.research.temporal_memory import TemporalMemory
from Learning.Layer import Layer
from LearningModel import LearningModel


class JoinedInputsModel(LearningModel):
    """
    Joins all the words in the sentence in one SDR and tries to predict
    the sequence of actions.
    Structure:
       WordEncoder, ActionEncoder -> GeneralSP -> GeneralTM
    """

    def __init__(self, wordEncoder, actionEncoder, trainingSet,
            modulesParams=None):
        """
        @param wordEncoder
        @param actionEncoder
        @param dataSet: A module containing the trainingData, all of
            its categories and the inputIdx dict that maps each index
            in categories to an input name.
        """

        super(JoinedInputsModel, self).__init__(wordEncoder, actionEncoder,
            trainingSet, modulesParams)

        self.buckets = dict()
        self.iterationsTrained = 0

        self.initModules(trainingSet.categories, trainingSet.inputIdx)

        self.structure = {
            'wordInput': 'wordEnc',
            'wordEnc': 'generalSP',
            ###
            'actionInput': 'actionEnc',
            'actionEnc': 'generalSP',
            ###
            'generalSP': 'generalTM',
            'generalTM': None
        }
        self.modules = {
            'generalTM': self.generalTM,
            'generalSP': self.generalSP,
            'wordEnc': self.wordEncoder,
            'actionEnc': self.actionEncoder
        }

        self.layer = Layer(self.structure, self.modules, self.classifier)

    def initModules(self, categories, inputIdx):

        modulesNames = {'generalSP', 'generalTM'}

        nWords = len(categories[inputIdx['wordInput']])
        nActions = len(categories[inputIdx['actionInput']])


        inputDimensions = max(
            self.wordEncoder.getWidth(),
            self.actionEncoder.getWidth()
        )

        columnDimensions = (max((nWords + nActions),
            len(self.trainingData)) * 2, )

        defaultGeneralSPParams = {
            'inputDimensions': inputDimensions,
            'columnDimensions': columnDimensions,
            'seed': self.spSeed
        }

        defaultGeneralTMParams = {
            'columnDimensions': columnDimensions,
            'seed': self.tmSeed
        }

        if (self.modulesParams is not None) and\
                (set(self.modulesParams) == modulesNames):
            self.modulesParams['generalSP'].update(defaultGeneralSPParams)
            self.modulesParams['generalTM'].update(defaultGeneralTMParams)

            self.generalSP = SpatialPooler(**self.modulesParams['generalSP'])
            self.generalTM = TemporalMemory(**self.modulesParams['generalTM'])
            print("Using external Parameters!")

        else:
            self.generalSP = SpatialPooler(**defaultGeneralSPParams)
            self.generalTM = TemporalMemory(**defaultGeneralTMParams)
            print("External parameters invalid or not found, using"\
                " the default ones")

        self.classifier = CLAClassifierCond(
            steps=[1, 2],
            alpha=0.1,
            actValueAlpha=0.3,
            verbosity=0
        )

    def train(self, numIterations, trainingData=None, maxTime=-1, verbosity=0,
            learn=True):

        startTime = time.time()
        maxTimeReached = False

        if trainingData is None:
            trainingData = self.trainingData

        for iteration in xrange(numIterations):
            if verbosity > 0:
                print("Iteration "  + str(iteration))

            recordNum = 0

            for sentence, actionSeq in trainingData:
                self.inputSentence(sentence, verbosity, learn)
                recordNum += 1

                for action in actionSeq:
                    inputData = ('actionInput', action)
                    self.processInput(inputData, recordNum, verbosity, learn)
                    recordNum += 1

                self.reset()

                if (maxTime > 0):
                    elapsedMinutes = (time.time() - startTime) * (1.0 / 60.0)

                    if (elapsedMinutes > maxTime):
                        maxTimeReached = True
                        print("maxTime reached, training stoped at iteration "\
                            "{}!".format(self.iterationsTrained))
                        break

            if maxTimeReached:
                break

            self.iterationsTrained += 1

    def processInput(self, inputData, recordNum, verbosity=0, learn=False):

        inputName = inputData[0]
        actualValue = inputData[1]

        if verbosity > 1:
            print("===== " + inputName + ": " + str(actualValue) + " =====")

        encodedValue = numpy.zeros(
            self.generalSP.getInputDimensions(),
            dtype=numpy.uint8
        )

        if inputName == 'wordInput':
            for word in actualValue:
                encodedValue[self.wordEncoder.getBucketIndices(word)] = 1

            actualValue = ' '.join(actualValue)

        elif(inputName == 'actionInput'):
            aux = self.actionEncoder.encode(actualValue)
            encodedValue[numpy.where(aux > 1)] = 1

        if actualValue not in self.buckets:
            self.buckets[actualValue] = len(self.buckets)

        bucketIndex = self.buckets[actualValue]

        if verbosity > 1:
            print("Encoded Value: {0}\n"\
                "Bucket Index: {1}\n".format(encodedValue, bucketIndex))

        spOutput = numpy.zeros(self.generalSP.getColumnDimensions(),
                    dtype=numpy.uint8)
        self.generalSP.compute(encodedValue, learn, spOutput)

        tmInput = numpy.where(spOutput > 0)[0]
        self.generalTM.compute(set(tmInput), learn)

        retVal = self.classifier.compute(
                recordNum=recordNum,
                patternNZ=self.generalTM.activeCells,
                classification={
                    'bucketIdx': self.buckets[actualValue],
                    'actValue': actualValue
                },
                learn=learn,
                infer=True,
                conditionFunc=lambda x: x.endswith("-event")
            )

        bestPredictions = []

        for step in retVal:
            if step == 'actualValues':
                continue

            higherProbIndex = numpy.argmax(retVal[step])
            bestPredictions.append(
                retVal['actualValues'][higherProbIndex]
            )

        if verbosity > 2 :
            print("  |  CLAClassifier best predictions for step1: ")
            top = sorted(retVal[1].tolist(), reverse=True)[:3]

            for prob in top:
                probIndex = retVal[1].tolist().index(prob)
                print(str(retVal['actualValues'][probIndex]) +
                    " - " + str(prob))

            print("  |  CLAClassifier best predictions for step2: ")
            top = sorted(retVal[2].tolist(), reverse=True)[:3]

            for prob in top:
                probIndex = retVal[2].tolist().index(prob)
                print(str(retVal['actualValues'][probIndex]) +
                    " - " + str(prob))

            print("")
            print("---------------------------------------------------")
            print("")

        return bestPredictions

    def inputSentence(self, sentence, verbosity=0, learn=False):

        inputData = ('wordInput', sentence)
        bestPredictions = self.processInput(inputData, 0, verbosity, learn)

        if verbosity > 1:
            print('Best Predictions: ' + str(bestPredictions))

        return bestPredictions

