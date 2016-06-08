#!/usr/bin/python2
#-*- coding: utf-8 -*-
#  OptimizeModel.py
#  Author: Larvasapiens <sebastian.narvaez@correounivalle.edu.co>
#  Created: 2016-01-19
#  Last Modified: 2016-01-19
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

import sys
import copy
import cPickle
import operator
from Utils import TestSuite
from Utils.PyramsFinder import Parameter, ParametersFinder

from Learning.EncoderFactory import CustomCategoryEncoder

from Learning import TotalTrainingSet as trainingSet
from Learning import TotalTrainingSet as testSet

from Learning.LearningModels.OneLevelModel import OneLevelModel as CurrentModel
import Learning.ModelParameters.OneLevel__ as BestResults

def saveParamsToFile(population, nonOptimParams, fileName):
    """
    Prints the params of the model to a file.
    """
    with open(fileName, 'wb') as savingFile:
        savingFile.write("bestScores = {}\n".format(
            [indiv.score for indiv in population[:3]]
        ))

        paramDicts = []

        for i in xrange(3):
            paramDicts.append(dict())

            for param in population[i].parameters:
                paramDicts[i][param.name] = param.value

            paramDicts[i].update(nonOptimParams)

        savingFile.write("bestFindings = {}\n".format(
            [organizeParamsByModule(params) for params in
                paramDicts]
        ))


def organizeParamsByModule(params):
    """
    @param params: A dictionary whose keys have the format
        "{moduleName}___{paramName}" and whose values are the
        associated parameter values.
    @return: A dictionary of the parameters organized by the
        module they belong.
    """

    paramsByModule = {}

    for module___param in params:
        if len(module___param.split('___')) == 2:
            moduleName, paramName = module___param.split('___')

            if moduleName not in paramsByModule:
                paramsByModule[moduleName] = {}

            #print("model_paramName: {}".format(modelParams[model___param]))
            paramsByModule[moduleName][paramName] = params[module___param]

    return paramsByModule


def getModelScore(model, trainIterations, trainMaxTime, testsMaxTime,
        **modelParams):
    """
    @param model
    @param trainIterations: Number of iterations the model is
        going to be trained.
    @param trainMaxTime: Training stops if maxTime (in minutes) is
        exceeded. Note that this may interrupt an ongoing train
        ireration. -1 is no time restrictions.
    @param testsMaxTime: If maxTime (in minutes) is exceeded, the tests
        will end. Note that this won't interrupt an ongoing test.
        The TestSuite will wait until the sequence is passed to
        the model and the corresponding result is processed.
    @param modelParams
    """

    paramsByModule = organizeParamsByModule(modelParams)
    tempModel = copy.deepcopy(model)
    tempModel.iterationsTrained = 0

    for moduleName in paramsByModule:
        tempModel.modules[moduleName] = tempModel.modules[moduleName].__class__(
            **paramsByModule[moduleName])

    print('\n-----------------------------\n')

    print(tempModel.spParametersStr())
    print(tempModel.tmParametersStr())

    print('Training...')

    tempModel.train(trainIterations, maxTime=trainMaxTime, verbosity=0)
    results = TestSuite.testModel(tempModel, testSet.trainingData,
        maxTime=testsMaxTime, saveResults=False)

    print("Success: {}%".format(results['successPercent']))

    return results['successPercent']


def createParameters(model, trainingSet, wordEncoder, actionEncoder):

    paramDict = dict()
    nonMutableParams = dict()

    # OptimizeModel Non-Mutable Parameters
    nonMutableParams['model'] = model
    nonMutableParams['trainIterations'] = 50
    nonMutableParams['trainMaxTime'] = 20
    nonMutableParams['testsMaxTime'] = 15

    nWords = len(trainingSet.categories[trainingSet.inputIdx['wordInput']])
    nActions = len(trainingSet.categories[trainingSet.inputIdx['actionInput']])

    inputDimensions = max(
        wordEncoder.getWidth(),
        actionEncoder.getWidth()
    )

    # WordSP Non-Mutable Parameters
#    nonMutableParams['wordSP___inputDimensions'] = (wordEncoder.getWidth(),)
#    nonMutableParams['wordSP___columnDimensions'] = (nWords * 3,)
#    nonMutableParams['wordSP___numActiveColumnsPerInhArea'] = -1.0
#    nonMutableParams['wordSP___seed'] = model.spSeed
#    nonMutableParams['wordSP___spVerbosity'] = 0
#
#    # wordTM Non-Mutable Parameters
#    nonMutableParams['wordTM___columnDimensions'] = (nWords * 3,)
#    nonMutableParams['wordTM___seed'] = model.tmSeed
#
#    # actionSP Non-Mutable Parameters
#    nonMutableParams['actionSP___inputDimensions'] = (actionEncoder.getWidth(),)
#    nonMutableParams['actionSP___columnDimensions'] = (nActions * 3,)
#    nonMutableParams['actionSP___numActiveColumnsPerInhArea'] = -1.0
#    nonMutableParams['actionSP___seed'] = model.spSeed
#    nonMutableParams['actionSP___spVerbosity'] = 0
#
#    # actionTM Non-Mutable Parameters
#    nonMutableParams['actionTM___columnDimensions'] = (nActions * 3,)
#    nonMutableParams['actionTM___seed'] = model.tmSeed
#
#    # actionSP Non-Mutable Parameters
#    nonMutableParams['actionSP___inputDimensions'] = (actionEncoder.getWidth(),)
#    nonMutableParams['actionSP___columnDimensions'] = (nActions * 3,)
#    nonMutableParams['actionSP___numActiveColumnsPerInhArea'] = -1.0
#    nonMutableParams['actionSP___seed'] = model.spSeed
#    nonMutableParams['actionSP___spVerbosity'] = 0

#    # actionTM Non-Mutable Parameters
#    nonMutableParams['actionTM___columnDimensions'] = (nActions * 3,)
#    nonMutableParams['actionTM___seed'] = model.tmSeed

    for moduleName in model.modules:

        if moduleName.endswith('SP'):

            nonMutableParams[moduleName + '___inputDimensions'] = \
                model.modules[moduleName]._inputDimensions
            nonMutableParams[moduleName + '___columnDimensions'] = \
                model.modules[moduleName]._columnDimensions
            nonMutableParams[moduleName + '___numActiveColumnsPerInhArea'] = \
                model.modules[moduleName]._numActiveColumnsPerInhArea
            nonMutableParams[moduleName + '___seed'] = \
                model.spSeed
            nonMutableParams[moduleName + '___spVerbosity'] = \
                model.modules[moduleName]._spVerbosity

            paramName = moduleName + '___potentialRadius'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='int',
                value=model.modules[moduleName]._potentialRadius,
                minVal=1,
                maxVal=297,
                maxChange=29,
                mutationProb=1.0
            )

            paramName = moduleName + '___potentialPct'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='float',
                value=model.modules[moduleName]._potentialPct,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.3,
                mutationProb=1.0
            )

            paramName = moduleName + '___globalInhibition'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='bool',
                value=model.modules[moduleName]._globalInhibition,
                minVal=0,
                maxVal=1,
                maxChange=1,
                mutationProb=0.5
            )

            paramName = moduleName + '___localAreaDensity'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='float',
                value=model.modules[moduleName]._localAreaDensity,
                minVal=0.0,
                maxVal=1.0,
                maxChange=2.0,
                mutationProb=1.0
            )

            paramName = moduleName + '___stimulusThreshold'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='int',
                value=model.modules[moduleName]._stimulusThreshold,
                minVal=0,
                maxVal=10,
                maxChange=5,
                mutationProb=1.0
            )

            paramName = moduleName + '___synPermInactiveDec'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='float',
                value=model.modules[moduleName]._synPermInactiveDec,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.3,
                mutationProb=1.0
            )

            paramName = moduleName + '___synPermActiveInc'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='float',
                value=model.modules[moduleName]._synPermActiveInc,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.3,
                mutationProb=1.0
            )

            paramName = moduleName + '___synPermConnected'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='float',
                value=model.modules[moduleName]._synPermConnected,
                minVal=0.0,
                maxVal=0.9,
                maxChange=0.3,
                mutationProb=1.0
            )

            paramName = moduleName + '___minPctOverlapDutyCycle'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='float',
                value=model.modules[moduleName]._minPctOverlapDutyCycles,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.2,
                mutationProb=1.0
            )

            paramName = moduleName + '___minPctActiveDutyCycle'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='float',
                value=model.modules[moduleName]._minPctActiveDutyCycles,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.2,
                mutationProb=1.0
            )

            paramName = moduleName + '___dutyCyclePeriod'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='int',
                value=model.modules[moduleName]._dutyCyclePeriod,
                minVal=1,
                maxVal=200,
                maxChange=10,
                mutationProb=1.0
            )

            paramName = moduleName + '___maxBoost'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='float',
                value=model.modules[moduleName]._maxBoost,
                minVal=1.0,
                maxVal=50.0,
                maxChange=4.0,
                mutationProb=1.0
            )

            paramName = moduleName + '___wrapAround'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='bool',
                value=model.modules[moduleName]._wrapAround,
                minVal=0,
                maxVal=9223372036854775807,
                maxChange=9223372036854775807,
                mutationProb=0.5
            )

        elif moduleName.endswith('TM'):

            nonMutableParams[moduleName + '___columnDimensions'] = \
                model.modules[moduleName].columnDimensions
            nonMutableParams[moduleName + '___seed'] = \
                model.tmSeed

            paramName = moduleName + '___cellsPerColumn'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='int',
                value=model.modules[moduleName].cellsPerColumn,
                minVal=1,
                maxVal=500,
                maxChange=15,
                mutationProb=1.0
            )

            paramName = moduleName + '___activationThreshold'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='int',
                value=model.modules[moduleName].activationThreshold,
                minVal=1,
                maxVal=499,
                maxChange=5,
                mutationProb=1.0
            )

            paramName = moduleName + '___initialPermanence'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='float',
                value=model.modules[moduleName].initialPermanence,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.3,
                mutationProb=1.0
            )

            paramName = moduleName + '___connectedPermanence'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='float',
                value=model.modules[moduleName].connectedPermanence,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.3,
                mutationProb=1.0
            )

            paramName = moduleName + '___minThreshold'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='int',
                value=model.modules[moduleName].minThreshold,
                minVal=1,
                maxVal=100,
                maxChange=5,
                mutationProb=1.0
            )

            paramName = moduleName + '___maxNewSynapseCount'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='int',
                value=model.modules[moduleName].maxNewSynapseCount,
                minVal=1,
                maxVal=20,
                maxChange=3,
                mutationProb=1.0
            )

            paramName = moduleName + '___permanenceIncrement'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='float',
                value=model.modules[moduleName].permanenceIncrement,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.3,
                mutationProb=1.0
            )

            paramName = moduleName + '___permanenceDecrement'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='float',
                value=model.modules[moduleName].permanenceDecrement,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.3,
                mutationProb=1.0
            )

            paramName = moduleName + '___predictedSegmentDecrement'
            paramDict[paramName] = Parameter(
                name=paramName,
                dataType='float',
                value=model.modules[moduleName].predictedSegmentDecrement,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.2,
                mutationProb=1.0
            )

    # generalSP Non-Mutable Parameters
#    nonMutableParams['generalSP___inputDimensions'] = inputDimensions
#    nonMutableParams['generalSP___columnDimensions'] = (columnDimensions,)
#    nonMutableParams['generalSP___numActiveColumnsPerInhArea'] = -1.0
#    nonMutableParams['generalSP___seed'] = model.spSeed
#    nonMutableParams['generalSP___spVerbosity'] = 0
    #wordTMnCells = reduce(operator.mul,
    #    nonMutableParams['wordTM___columnDimensions'], 1) * \
    #    paramDict['wordTM___cellsPerColumn'].value
    #actionTMnCells = reduce(operator.mul,
    #    nonMutableParams['actionTM___columnDimensions'], 1) * \
    #    paramDict['actionTM___cellsPerColumn'].value

    # generalTM Non-Mutable Parameters
    #nonMutableParams['generalTM___columnDimensions'] = (2, max(
    #    wordTMnCells, actionTMnCells))
    #nonMutableParams['generalTM___seed'] = model.tmSeed

    return paramDict, nonMutableParams

if __name__ == '__main__':

    wordEncoder = CustomCategoryEncoder(
        11,
        list(trainingSet.categories[trainingSet.inputIdx['wordInput']]),
        nAdditionalCategorySlots=15,
        forced=True
    )
    actionEncoder = CustomCategoryEncoder(
        11,
        list(trainingSet.categories[trainingSet.inputIdx['actionInput']]),
        nAdditionalCategorySlots=15,
        forced=True
    )
#    wordEncoder = actionEncoder = UnifiedCategoryEncoder(trainingSet.categories)
#    wordEncoder = actionEncoder = RandomizedLetterEncoder(600, 10)
#    wordEncoder = actionEncoder = TotallyRandomEncoder(50, 10)

    modulesParams = BestResults.bestFindings[0]
    model = CurrentModel(wordEncoder, actionEncoder, trainingSet,
        modulesParams)

    # Extract all the SPs and TMs parameters
    paramDict, nonMutableParams = createParameters(model, trainingSet,
        wordEncoder, actionEncoder)

    paramsFinder = ParametersFinder(
        getModelScore,
        paramDict.values(),
        nonOptimParams=nonMutableParams
    )

    bestParameters = paramsFinder.findParams(
        populationSize=5,
        maxMutations=4,
        variety=3,
        elitism=1,
        selectionTechnique='RouletteWheel',
        randomizeFirstGen=True,
        maxIterations=-1,
        maxTime=24 * 60,  # hours
        #maxTime=-1,
        minScore=95,
        nParallelEvals=4,
        savingFrequency=1,
        savingFunc=saveParamsToFile,
        verbosity=2
    )

#    print("Saving the model...")
#    with open((fileName + '.pck'), 'wb') as modelFile:
#        cPickle.dump(model, modelFile, -1)
#    print("Done!")

