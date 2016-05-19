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

class LearningModel(object):
    """
    This class is intended as a guide for Learning Structure classes.
    It doesn't do anything by itself.
    """

    def __init__(self):
        """
        Initialize the module objects, the modules and the structure
        dicts, the layer and any other object you'll need for your
        learning structure.

        self.initModules()
        self.structure = dict()
        self.modules = dict()
        """

        self.iterationsTrained = 0
        self.spSeed = 42
        self.tmSeed = 42

    def initModules(self):

        pass

    def inputSentence(self, sentence, verbosity=1, learn=False):

        pass

    def train(self, numIterations, trainingData=None, maxTime=-1, verbosity=0):
        """
        @param numIterations
        @param trainingData: (default: None) An iterable, where each
            element is a sequence corresponding to an input for the
            model. if None, the default trainingData for the model
            is used.
        @param maxTime: Training stops if maxTime (in minutes) is
            exceeded. Note that this may interrupt an ongoing train
            ireration. -1 is no time restrictions.
        @param verbosity: How much verbose about the process. 0 doesn't
            print anything.
        """

        startTime = time.time()
        maxTimeReached = False

        if trainingData is None:
            trainingData = self.trainingData

        for iteration in xrange(numIterations):
            print("Iteration " + str(iteration))

            for sentence, actionSeq in trainingData:
                inputData = [
                    ('wordInput', sentence),
                    ('actionInput', actionSeq)
                ]
                self.layer.processInput(inputData, verbosity)
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

    def reset(self):
        """
        Resets all the components of the structure to receive a new
        sequence
        """

        for modName in self.modules:
            if modName.endswith('TM'):
                self.modules[modName].reset()

    def spParametersStr(self):
        params = ""

        for modName in self.modules:
            if modName.endswith('SP'):
                params += "{0}Args = {{\n".format(modName)
                params += "\t'inputDimensions': {0},\n".format(
                    self.modules[modName]._inputDimensions)
                params += "\t'columnDimensions': {0},\n".format(
                    self.modules[modName]._columnDimensions)
                params += "\t'potentialRadius': {0},\n".format(
                    self.modules[modName]._potentialRadius)
                params += "\t'potentialPct': {0},\n".format(
                    self.modules[modName]._potentialPct)
                params += "\t'globalInhibition': {0},\n".format(
                    self.modules[modName]._globalInhibition)
                params += "\t'localAreaDensity': {0},\n".format(
                    self.modules[modName]._localAreaDensity)
                params += "\t'numActiveColumnsPerInhArea': {0},\n".format(
                    self.modules[modName]._numActiveColumnsPerInhArea)
                params += "\t'stimulusThreshold': {0},\n".format(
                    self.modules[modName]._stimulusThreshold)
                params += "\t'synPermInactiveDec': {0},\n".format(
                    self.modules[modName]._synPermInactiveDec)
                params += "\t'synPermActiveInc': {0},\n".format(
                    self.modules[modName]._synPermActiveInc)
                params += "\t'synPermConnected': {0},\n".format(
                    self.modules[modName]._synPermConnected)
                params += "\t'minPctOverlapDutyCycle': {0},\n".format(
                    self.modules[modName]._minPctOverlapDutyCycles)
                params += "\t'minPctActiveDutyCycle': {0},\n".format(
                    self.modules[modName]._minPctActiveDutyCycles)
                params += "\t'dutyCyclePeriod': {0},\n".format(
                    self.modules[modName]._dutyCyclePeriod)
                params += "\t'maxBoost': {0},\n".format(
                    self.modules[modName]._maxBoost)
                params += "\t'seed': {0},\n".format(
                    self.spSeed)
                params += "\t'spVerbosity': {0},\n".format(
                    self.modules[modName]._spVerbosity)
                params += "\t'wrapAround': {0}\n".format(
                    self.modules[modName]._wrapAround)
                params += "}"

        return params

    def tmParametersStr(self):
        params = ""

        for modName in self.modules:
            if modName.endswith('TM'):
                params += "{0}Args = {{\n".format(modName)
                params += "\t'columnDimensions': {0},\n".format(
                    self.modules[modName].columnDimensions)
                params += "\t'cellsPerColumn': {0},\n".format(
                    self.modules[modName].cellsPerColumn)
                params += "\t'activationThreshold': {0},\n".format(
                    self.modules[modName].activationThreshold)
                params += "\t'initialPermanence': {0},\n".format(
                    self.modules[modName].initialPermanence)
                params += "\t'connectedPermanence': {0},\n".format(
                    self.modules[modName].connectedPermanence)
                params += "\t'minThreshold': {0},\n".format(
                    self.modules[modName].minThreshold)
                params += "\t'maxNewSynapseCount': {0},\n".format(
                    self.modules[modName].maxNewSynapseCount)
                params += "\t'permanenceIncrement': {0},\n".format(
                    self.modules[modName].permanenceIncrement)
                params += "\t'permanenceDecrement': {0},\n".format(
                    self.modules[modName].permanenceDecrement)
                params += "\t'predictedSegmentDecrement': {0},\n".format(
                    self.modules[modName].predictedSegmentDecrement)
                params += "\t'seed': {0}\n".format(self.tmSeed)
                params += "}"

        return params

