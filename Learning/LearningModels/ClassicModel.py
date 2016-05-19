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

from nupic.algorithms.CLAClassifier import CLAClassifier
from nupic.encoders.scalar import ScalarEncoder
from nupic.research.spatial_pooler import SpatialPooler
from nupic.research.temporal_memory import TemporalMemory
from Learning.Layer import Layer
from LearningModel import LearningModel
from Utils.ArrayCommonOverlap import CommonOverlap

class ClassicModel(LearningModel):
    """
     Structure:
       WordEncoder -> WordsSP -> SentencesTM
       ActionEncoder -> ActionsSP -> ActionsSeqTM
           SentencesTM + ActionsSeqTM -> generalTM
    """

    def __init__(self, wordEncoder, actionEncoder, trainingSet):
        """
        @param wordEncoder
        @param actionEncoder
        @param dataSet: A module containing the trainingData, all of
            its categories and the inputIdx dict that maps each index
            in categories to an input name.
        """

        super(ClassicModel, self).__init__()

        self.wordEncoder = wordEncoder
        self.actionEncoder = actionEncoder
        self.trainingData = trainingSet.trainingData

        self.initModules(trainingSet.categories, trainingSet.inputIdx)

        self.structure = {
            'wordInput' : 'wordEnc',
            'wordEnc' : 'wordSP',
            'wordSP' : 'wordTM',
            'wordTM' : 'generalSP',
            ###
            'actionInput' : 'actionEnc',
            'actionEnc' : 'actionSP',
            'actionSP' : 'actionTM',
            'actionTM' : 'generalSP',
            ###
            'generalSP' : 'generalTM',
            'generalTM' : None
        }
        self.modules = {
            'generalTM' : self.generalTM,
            'generalSP' : self.generalSP,
            'wordTM' : self.wordTM,
            'wordSP' : self.wordSP,
            'wordEnc' : self.wordEncoder,
            'actionTM' : self.actionTM,
            'actionSP' : self.actionSP,
            'actionEnc' : self.actionEncoder
        }

        self.layer = Layer(self.structure, self.modules,
            self.classifier)

    def initModules(self, categories, inputIdx):

        nWords = len(categories[inputIdx['wordInput']])
        nActions = len(categories[inputIdx['actionInput']])

        self.wordSP = SpatialPooler(
            inputDimensions=(self.wordEncoder.getWidth()),
            columnDimensions=(nWords * 3),
            potentialRadius=12,
            potentialPct=0.5,
            globalInhibition=True,
            localAreaDensity=-1.0,
            numActiveColumnsPerInhArea=5.0,
            stimulusThreshold=0,
            synPermInactiveDec=0.1,
            synPermActiveInc=0.1,
            synPermConnected=0.1,
            minPctOverlapDutyCycle=0.1,
            minPctActiveDutyCycle=0.1,
            dutyCyclePeriod=10,
            maxBoost=3,
            seed=42,
            spVerbosity=0
        )

        self.wordTM = TemporalMemory(
            columnDimensions=(nWords * 3,),
            initialPermanence=0.4,
            connectedPermanence=0.5,
            minThreshold=4,
            maxNewSynapseCount=4,
            permanenceDecrement=0.05,
            permanenceIncrement=0.05,
            activationThreshold=4,
            seed=self.tmSeed
        )

        self.actionSP = SpatialPooler(
            inputDimensions=self.actionEncoder.getWidth(),
            columnDimensions=(nActions * 3),
            potentialRadius=12,
            potentialPct=0.5,
            globalInhibition=True,
            localAreaDensity=-1.0,
            numActiveColumnsPerInhArea=5.0,
            stimulusThreshold=0,
            synPermInactiveDec=0.1,
            synPermActiveInc=0.1,
            synPermConnected=0.1,
            minPctOverlapDutyCycle=0.1,
            minPctActiveDutyCycle=0.1,
            dutyCyclePeriod=10,
            maxBoost=3,
            seed=42,
            spVerbosity=0
        )

        self.actionTM = TemporalMemory(
            columnDimensions=(nActions * 3,),
            initialPermanence=0.4,
            connectedPermanence=0.5,
            minThreshold=4,
            maxNewSynapseCount=4,
            permanenceDecrement=0.05,
            permanenceIncrement=0.05,
            activationThreshold=4,
            seed=self.tmSeed
        )

        generalInputDimensions = max(
                self.wordTM.numberOfCells() + 1,
                self.actionTM.numberOfCells() + 1
            )

        self.generalSP = SpatialPooler(
            inputDimensions=generalInputDimensions,
            columnDimensions=(len(self.trainingData) * 3,),
            potentialRadius = 28,
            potentialPct = 0.5,
            globalInhibition = True,
            localAreaDensity = -1.0,
            numActiveColumnsPerInhArea = 5.0,
            stimulusThreshold = 0,
            synPermInactiveDec = 0.1,
            synPermActiveInc = 0.1,
            synPermConnected = 0.1,
            minPctOverlapDutyCycle = 0.1,
            minPctActiveDutyCycle = 0.1,
            dutyCyclePeriod = 10,
            maxBoost = 3,
            seed = 42,
            spVerbosity = 0
        )

        self.generalTM = TemporalMemory(
            columnDimensions=(len(self.trainingData) * 3,),
            initialPermanence=0.4,
            connectedPermanence=0.5,
            minThreshold=4,
            maxNewSynapseCount=4,
            permanenceDecrement=0.05,
            permanenceIncrement=0.05,
            activationThreshold=4,
            seed=self.tmSeed
        )

        self.classifier = CLAClassifier(
            steps=[1, 2, 3],
            alpha=0.1,
            actValueAlpha=0.3,
            verbosity=0
        )

    def inputSentence(self, sentence, verbosity=1, learn=False):

        inputData = [('wordInput', sentence)]

        return self.layer.processInput(inputData, verbosity, learn)

