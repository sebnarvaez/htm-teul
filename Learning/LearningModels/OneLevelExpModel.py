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


class OneLevelExpModel(LearningModel):
    """
     Structure:
       WordEncoder, ActionEncoder -> GeneralSP -> GeneralTM
    """

    def __init__(self, wordEncoder, actionEncoder, trainingSet):
        """
        @param wordEncoder
        @param actionEncoder
        @param dataSet: A module containing the trainingData, all of
            its categories and the inputIdx dict that maps each index
            in categories to an input name.
        """

        super(OneLevelExpModel, self).__init__()

        self.wordEncoder = wordEncoder
        self.actionEncoder = actionEncoder
        self.trainingData = trainingSet.trainingData

        self.initModules(trainingSet.categories, trainingSet.inputIdx)

        self.structure = {
            'wordInput' : 'wordEnc',
            'wordEnc' : 'generalSP',
            ###
            'actionInput' : 'actionEnc',
            'actionEnc' : 'generalSP',
            ###
            'generalSP' : 'generalTM',
            'generalTM' : None
        }
        self.modules = {
            'generalTM' : self.generalTM,
            'generalSP' : self.generalSP,
            'wordEnc' : self.wordEncoder,
            'actionEnc' : self.actionEncoder
        }

        self.layer = Layer(self.structure, self.modules, self.classifier)

    def initModules(self, categories, inputIdx):

        nWords = len(categories[inputIdx['wordInput']])
        nActions = len(categories[inputIdx['actionInput']])

        inputDimensions = max(
            self.wordEncoder.getWidth(),
            self.actionEncoder.getWidth()
        )

        columnDimensions = 4 * max((nWords + nActions),
                len(self.trainingData))

        self.generalSP = SpatialPooler(
            inputDimensions=inputDimensions,
            #UCE: (nWords + nActions) * 3, RLE:
            columnDimensions=(columnDimensions,),
            #UCE: 11, RLE:1
            potentialRadius=297,
            #UCE: 11, RLE:1
            potentialPct=0.726248028695,
            globalInhibition=True,
            localAreaDensity=-1.0,
            #4, 4.5 -> 86%
            numActiveColumnsPerInhArea=4.0,
            stimulusThreshold=2,
            synPermInactiveDec=0.165088154764,
            synPermActiveInc=0.1,
            #0.15 -> 86%
            synPermConnected=0.236217765977,
            minPctOverlapDutyCycle=0.302204519404,
            minPctActiveDutyCycle=0.0,
            #20
            dutyCyclePeriod=9,
            #3
            maxBoost=1.0,
            seed=self.spSeed,
            spVerbosity=0,
            wrapAround=True
        )

        self.generalTM = TemporalMemory(
            columnDimensions=(columnDimensions,),
            cellsPerColumn=64,
            # 4
            activationThreshold=1,
            # 0.3
            initialPermanence=0.263488191214,
            connectedPermanence=0.674714438958,
            minThreshold=4,
            maxNewSynapseCount=4,
            permanenceIncrement=0.117671359444,
            permanenceDecrement=1.0,
            predictedSegmentDecrement=0.0,
            seed=self.tmSeed
        )

        #self.generalSP = SpatialPooler(
            #inputDimensions=inputDimensions,
            ##UCE: (nWords + nActions) * 3, RLE:
            #columnDimensions=(columnDimensions,),
            ##UCE: 11, RLE:1
            #potentialRadius=inputDimensions,
            ##UCE: 11, RLE:1
            #potentialPct=0.5,
            #globalInhibition=True,
            #localAreaDensity=-1.0,
            ##4, 4.5 -> 86%
            #numActiveColumnsPerInhArea=4,
            #stimulusThreshold=0,
            #synPermInactiveDec=0.1,
            #synPermActiveInc=0.1,
            ##0.15 -> 86%
            #synPermConnected=0.15,
            #minPctOverlapDutyCycle=0.1,
            #minPctActiveDutyCycle=0.1,
            ##20
            #dutyCyclePeriod=16,
            ##3
            #maxBoost=3,
            #seed=self.spSeed,
            #spVerbosity=0,
            #wrapAround=True
        #)

        #self.generalTM = TemporalMemory(
            #columnDimensions=(columnDimensions,),
            #cellsPerColumn=80,
            ## 4
            #activationThreshold=4,
            ## 0.3
            #initialPermanence=0.3,
            #connectedPermanence=0.575611110106,
            #minThreshold=4,
            #maxNewSynapseCount=4,
            #permanenceIncrement=0.05,
            #permanenceDecrement=0.143945674364,
            #predictedSegmentDecrement=0.0,
            #seed=self.tmSeed
        #)

        #generalSPArgs = {
            #'inputDimensions': [297],
            #'columnDimensions': [1440],
            #'potentialRadius': 33,
            #'potentialPct': 0.878502103883,
            #'globalInhibition': False,
            #'localAreaDensity': -1.0,
            #'numActiveColumnsPerInhArea': 282,
            #'stimulusThreshold': 3,
            #'synPermInactiveDec': 0.628325572745,
            #'synPermActiveInc': 0.252328979379,
            #'synPermConnected': 0.674231628955,
            #'minPctOverlapDutyCycle': 0.727506713123,
            #'minPctActiveDutyCycle': 0.61502196691,
            #'dutyCyclePeriod': 85,
            #'maxBoost': 22.7589495827,
            #'seed': 42,
            #'spVerbosity': 0,
            #'wrapAround': False
        #}
        #generalTMArgs = {
            #'columnDimensions': (1440,),
            #'cellsPerColumn': 296,
            #'activationThreshold': 3,
            #'initialPermanence': 0.973159425903,
            #'connectedPermanence': 0.0356029114278,
            #'minThreshold': 35,
            #'maxNewSynapseCount': 20,
            #'permanenceIncrement': 0.768559889207,
            #'permanenceDecrement': 0.932179170176,
            #'predictedSegmentDecrement': 0.358265258558,
            #'seed': 42
        #}


        #self.generalSP = SpatialPooler(**generalSPArgs)

        #self.generalTM = TemporalMemory(**generalTMArgs)

        self.classifier = CLAClassifier(
            steps=[1, 2, 3],
            alpha=0.1,
            actValueAlpha=0.3,
            verbosity=0
        )

    def inputSentence(self, sentence, verbosity=1, learn=False):

        inputData = [('wordInput', sentence)]

        return self.layer.processInput(inputData, verbosity, learn)

