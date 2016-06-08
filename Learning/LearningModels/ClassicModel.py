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

from Utils.CLAClassifierCond import CLAClassifierCond
from nupic.research.spatial_pooler import SpatialPooler
from nupic.research.temporal_memory import TemporalMemory
from Learning.Layer import Layer
from LearningModel import LearningModel


class ClassicModel(LearningModel):
    """
     Structure:
       WordEncoder -> WordsSP -> SentencesTM
       ActionEncoder -> ActionsSP -> ActionsSeqTM
           SentencesTM + ActionsSeqTM -> generalTM
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

        super(ClassicModel, self).__init__(wordEncoder, actionEncoder,
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
            'generalSP': self.generalSP,
            'wordTM': self.wordTM,
            'wordSP': self.wordSP,
            'wordEnc': self.wordEncoder,
            'actionTM': self.actionTM,
            'actionSP': self.actionSP,
            'actionEnc': self.actionEncoder
        }

        self.layer = Layer(self.structure, self.modules,
            self.classifier)

    def initModules(self, categories, inputIdx):

        modulesNames = {'wordSP', 'wordTM', 'actionSP', 'actionTM',
            'generalSP', 'generalTM'}

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

            generalInputDimensions = max(
                self.wordTM.numberOfCells() + 1,
                self.actionTM.numberOfCells() + 1
            )
            generalColumnDimensions = (len(self.trainingData) * 3,)

            defaultGeneralSPParams = {
                'inputDimensions': generalInputDimensions,
                'columnDimensions': generalColumnDimensions,
                'seed': self.spSeed
            }
            defaultGeneralTMParams = {
                'columnDimensions': generalColumnDimensions,
                'seed': self.tmSeed
            }

            self.modulesParams['generalSP'].update(defaultGeneralSPParams)
            self.modulesParams['generalTM'].update(defaultGeneralTMParams)

            self.generalSP = SpatialPooler(**self.modulesParams['generalSP'])
            self.generalTM = TemporalMemory(**self.modulesParams['generalTM'])
            print("Using external Parameters!")

        else:
            self.wordSP = SpatialPooler(**self.defaultWordSPParams)
            self.wordTM = TemporalMemory(**self.defaultWordTMParams)
            self.actionSP = SpatialPooler(**self.defaultActionSPParams)
            self.actionTM = TemporalMemory(**self.defaultActionTMParams)
            print("External parameters invalid or not found, using"\
                " the default ones")

            generalInputDimensions = max(
                self.wordTM.numberOfCells() + 1,
                self.actionTM.numberOfCells() + 1
            )
            generalColumnDimensions = (len(self.trainingData) * 3,)

            defaultGeneralSPParams = {
                'inputDimensions': generalInputDimensions,
                'columnDimensions': generalColumnDimensions,
                'seed': self.spSeed
            }
            defaultGeneralTMParams = {
                'columnDimensions': generalColumnDimensions,
                'seed': self.tmSeed
            }

            self.generalSP = SpatialPooler(**defaultGeneralSPParams)
            self.generalTM = TemporalMemory(**defaultGeneralTMParams)

        self.classifier = CLAClassifierCond(
            steps=[1, 2, 3],
            alpha=0.1,
            actValueAlpha=0.3,
            verbosity=0
        )

    def inputSentence(self, sentence, verbosity=1, learn=False):

        inputData = [('wordInput', sentence)]

        return self.layer.processInput(inputData, verbosity, learn)

