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

import numpy
import time

from nupic.research.spatial_pooler import SpatialPooler
from nupic.research.temporal_memory import TemporalMemory
from nupic.algorithms.CLAClassifier import CLAClassifier
from Utils.CLAClassifierCond import CLAClassifierCond
from LearningModel import LearningModel
from Utils.ArrayCommonOverlap import CommonOverlap


class FeedbackModel(LearningModel):
    """
     Structure:
       WordEncoder -> WordSP -> WordTM
       ActionEncoder -> ActionSP -> ActionTM
       WordTM, ActionTM -> GeneralSP -> GeneralTM

    """

    def __init__(self, wordEncoder, actionEncoder, trainingSet,
            modulesParams=None):
        """
        @param wordEncoder
        @param actionEncoder
        @param trainingSet: A module containing the trainingData, all of
            its categories and the inputIdx dict that maps each index
            in categories to an input name.
        """

        super(FeedbackModel, self).__init__(wordEncoder, actionEncoder,
            trainingSet, modulesParams)

        self.initModules(trainingSet.categories, trainingSet.inputIdx)

        self.structure = {
            'wordInput': 'wordEnc',
            'wordEnc': 'wordSP',
            'wordSP': 'wordTM',
            'wordTM': 'generalSP',
            ###
            'actionInput': 'actionEnc',
            'actionEnc': 'actionSP',
            'actionSP': 'actionTM',
            'actionTM': 'generalSP',
            ###
            'generalSP': 'generalTM',
            'generalTM': None
        }
        self.modules = {
            'generalTM': self.generalTM,
            #'generalSP': self.generalSP,
            'wordTM': self.wordTM,
            'wordSP': self.wordSP,
            'wordEnc': self.wordEncoder,
            'actionTM': self.actionTM,
            'actionSP': self.actionSP,
            'actionEnc': self.actionEncoder
        }

        #self.layer = Layer(self.structure, self.modules, self.classifier)

    def initModules(self, categories, inputIdx):

        modulesNames = {'wordSP', 'wordTM', 'actionSP', 'actionTM',
            'generalTM'}

        if (self.modulesParams is not None) and\
                (set(self.modulesParams) == modulesNames):
            self.modulesParams['wordSP'].update(self.defaultWordSPParams)
            self.modulesParams['wordTM'].update(self.defaultWordTMParams)
            self.modulesParams['actionSP'].update(self.defaultActionSPParams)
            self.modulesParams['actionTM'].update(self.defaultActionTMParams)

            self.wordSP = SpatialPooler(**self.modulesParams['wordSP'])
            self.wordTM = TemporalMemory(**self.modulesParams['wordTM'])
            self.actionSP = SpatialPooler(**self.modulesParams['actionSP'])
            self.actionTM = TemporalMemory(**self.modulesParams['actionTM'])

            defaultGeneralTMParams = {
                'columnDimensions': (2, max(self.wordTM.numberOfCells(),
                     self.actionTM.numberOfCells())),
                'seed': self.tmSeed
            }

            self.modulesParams['generalTM'].update(defaultGeneralTMParams)

            self.generalTM = TemporalMemory(**self.modulesParams['generalTM'])
            print("Using external Parameters!")

        else:
            self.wordSP = SpatialPooler(**self.defaultWordSPParams)
            self.wordTM = TemporalMemory(**self.defaultWordTMParams)
            self.actionSP = SpatialPooler(**self.defaultActionSPParams)
            self.actionTM = TemporalMemory(**self.defaultActionTMParams)
            print("External parameters invalid or not found, using"\
                " the default ones")

            defaultGeneralTMParams = {
                'columnDimensions': (2, max(self.wordTM.numberOfCells(),
                     self.actionTM.numberOfCells())),
                'seed': self.tmSeed
            }

            self.generalTM = TemporalMemory(**defaultGeneralTMParams)


        self.classifier = CLAClassifierCond(
            steps=[1, 2, 3],
            alpha=0.1,
            actValueAlpha=0.3,
            verbosity=0
        )

        self.startPointOverlap = CommonOverlap('==', 1,
            self.actionTM.columnDimensions, threshold=0.5)

    def processInput(self, sentence, actionSeq, wordSDR=None,
                     actionSDR=None, verbosity=0, learn=True):

        if wordSDR is None:
            wordSDR = numpy.zeros(self.wordSP.getColumnDimensions(),
                              dtype=numpy.uint8)
        if actionSDR is None:
            actionSDR = numpy.zeros(self.actionSP.getColumnDimensions(),
                              dtype=numpy.uint8)

        nCellsFromSentence = self.generalTM.columnDimensions[1]
        sentenceActiveCells = set()
        actionSeqActiveCells = set()
        recordNum = 0

        # Feed the words from the sentence to the region 1
        for word in sentence:
            encodedWord = self.wordEncoder.encode(word)
            self.wordSP.compute(encodedWord, learn, wordSDR)
            self.wordTM.compute(
                set(numpy.where(wordSDR > 0)[0]),
                learn
            )
            region1Predicting = (self.wordTM.predictiveCells != set())
            sentenceActiveCells.update(self.wordTM.getActiveCells())

            #print("{} - {}".format(word, ))
            retVal = self.classifier.compute(
                recordNum=recordNum,
                patternNZ=self.wordTM.getActiveCells(),
                classification={
                    'bucketIdx': self.wordEncoder.getBucketIndices(word)[0],
                    'actValue': word
                },
                learn=learn,
                infer=True,
                conditionFunc=lambda x: x.endswith("-event")
            )

            recordNum += 1

        bestPredictions = []

        for step in retVal:
            if step == 'actualValues':
                continue
            higherProbIndex = numpy.argmax(retVal[step])
            bestPredictions.append(
                retVal['actualValues'][higherProbIndex]
            )

        if region1Predicting:
            # Feed the sentence to the region 2
            self.generalTM.compute(sentenceActiveCells, learn)

            generalPrediction = set(self.generalTM.mapCellsToColumns(
                self.generalTM.predictiveCells
            ).keys())

            # Normalize predictions so cells stay in the actionTM
            # range.
            generalPrediction = set([i - nCellsFromSentence
                                     for i in generalPrediction
                                     if i >= nCellsFromSentence])

#            columnsPrediction = numpy.zeros(
#                self.actionSP.getNumColumns(),
#                dtype=numpy.uint8
#            )
#            columnsPrediction[self.actionTM.mapCellsToColumns(
#                generalPrediction).keys()] = 1
#            self.startPointOverlap.updateCounts(columnsPrediction)
#
#        if len(actionSeq) <= 0:
#
#            assert region1Predicting, "Region 1 is not predicting, consider "\
#                "training the model for a longer time"
#            predictedValues = []
#
#            firstColumns = numpy.where(numpy.bitwise_and(columnsPrediction > 0,
#                self.startPointOverlap.commonElements))
#
#            predictedEnc = numpy.zeros(self.actionEncoder.getWidth(),
#                                         dtype=numpy.uint8)
#            predictedEnc[
#                [self.actionSP._mapColumn(col) for col in firstColumns]] = 1
#            predictedValues.append(self.actionEncoder.decode(predictedEnc))
#
#            print(firstColumns)
#
#            self.actionTM.predictiveCells.update(generalPrediction)
#            self.actionTM.compute(firstColumns, learn)
#
#            predictedColumns = self.actionTM.mapCellsToColumns(
#                self.actionTM.predictiveCells).keys()[0]

        for action in actionSeq:
            encodedAction = self.actionEncoder.encode(action)
            # Use the predicted cells from region 2 to bias the
            # activity of cells in region 1.

            if region1Predicting:
                self.actionTM.predictiveCells.update(generalPrediction)

            self.actionSP.compute(encodedAction, learn, actionSDR)
            self.actionTM.compute(
                set(numpy.where(actionSDR > 0)[0]),
                learn
            )
            actionActiveCells = [i + nCellsFromSentence for i in
                                 self.actionTM.getActiveCells()]
            actionSeqActiveCells.update(actionActiveCells)
            self.classifier.compute(
                recordNum=recordNum,
                patternNZ=actionActiveCells,
                classification={
                    'bucketIdx': self.wordEncoder.getWidth() +
                        self.actionEncoder.getBucketIndices(action)[0],
                    'actValue': action
                },
                learn=learn,
                infer=True,
                conditionFunc=lambda x: x.endswith("-event")
            )

            recordNum += 1

        if region1Predicting:
            self.generalTM.compute(
                actionSeqActiveCells,
                True
            )

        if verbosity > 0:
            print('Best Predictions: ' + str(bestPredictions))

        if verbosity > 3:
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

    def train(self, numIterations, trainingData=None,
              maxTime=-1, verbosity=0):
        """
        @param numIterations
        @param trainingData
        @param maxTime: (default: -1) Training stops if maxTime (in
            minutes) is exceeded. Note that this may interrupt an
            ongoing train ireration. -1 is no time restrictions.
        @param verbosity: (default: 0) How much verbose about the
            process. 0 doesn't print anything.
        """

        startTime = time.time()
        maxTimeReached = False
        recordNum = 0

        if trainingData is None:
            trainingData = self.trainingData

        wordSDR = numpy.zeros(self.wordSP.getColumnDimensions(),
                              dtype=numpy.uint8)
        actionSDR = numpy.zeros(self.actionSP.getColumnDimensions(),
                                dtype=numpy.uint8)
        #generalSDR = numpy.zeros(self.generalSP.getColumnDimensions(),
        #                         dtype=numpy.uint8)
        generalInput = numpy.zeros(self.generalTM.numberOfColumns(),
                                   dtype=numpy.uint8)

        for iteration in xrange(numIterations):
            print("Iteration " + str(iteration))

            for sentence, actionSeq in trainingData:
                self.processInput(sentence, actionSeq, wordSDR, actionSDR)
                self.reset()
                recordNum += 1

                if maxTime > 0:
                    elapsedMinutes = (time.time() - startTime) * (1.0 / 60.0)

                    if elapsedMinutes > maxTime:
                        maxTimeReached = True
                        print("maxTime reached, training stoped at iteration "\
                            "{}!".format(self.iterationsTrained))
                        break

            if maxTimeReached:
                break

            self.iterationsTrained += 1

    def inputSentence(self, sentence, verbosity=1, learn=False):

        return self.processInput(sentence, [], verbosity=verbosity, learn=learn)

