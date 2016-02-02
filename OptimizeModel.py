#!python2
#-*- coding: utf-8 -*-
#  OptimizeModel.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2016-01-19
#  Fecha última modificación: 2016-01-19
#  Versión: 1.2

import sys
import copy
import cPickle
from Utils import TestSuite
from Utils.PyramsFinder import *
from Learning.EncoderFactory import *
from Learning.LearningModels import *
from Learning import MovementTrainingSet as MTS

def organizeParamsByModule(params):
    
    paramsByModule = {}
    
    for model___param in params:
        moduleName, paramName = model___param.split('___')
        
        if moduleName not in paramsByModule:
            paramsByModule[moduleName] = {}
        
        #print("model_paramName: {}".format(modelParams[model___param]))
        paramsByModule[moduleName][paramName] = params[model___param]
    
    return paramsByModule

def getModelScore(model, trainIterations, trainMaxTime, testsMaxTime,
        **modelParams):
    
    paramsByModule = {}
    
    #print("Evaluating {}".format(modelParams))
    
    for model___param in modelParams:
        moduleName, paramName = model___param.split('___')
        
        if moduleName not in paramsByModule:
            paramsByModule[moduleName] = {}
        
        #print("model_paramName: {}".format(modelParams[model___param]))
        paramsByModule[moduleName][paramName] = modelParams[model___param]
    
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
    results = TestSuite.testModel(tempModel, MTS.trainingData, 
        maxTime=testsMaxTime, saveResults=False)
    
    print("Success: {}%".format(results['successPercent']))
    
    return results['successPercent']

if __name__ == '__main__':
    
    wordEncoder = actionEncoder = UnifiedCategoryEncoder(MTS.categories)
    #wordEncoder = actionEncoder = RandomizedLetterEncoder(600, 10)
    #wordEncoder = actionEncoder = TotallyRandomEncoder(50, 10)
    
    #model = ClassicModel(wordEncoder, actionEncoder, MTS)
    #model = OneLevelModel(wordEncoder, actionEncoder, MTS)
    model = OneLevelExpModel(wordEncoder, actionEncoder, MTS)
    #model = JoinedInputsModel(wordEncoder, actionEncoder, MTS)
    
    paramList = []
    nonMutableParams = {}
    # getModelScore args:
    
    nWords = len(MTS.categories[MTS.inputIdx['wordInput']])
    nActions = len(MTS.categories[MTS.inputIdx['actionInput']])
    
    inputDimensions = max(
        wordEncoder.getWidth(),
        actionEncoder.getWidth()
    )
    
    columnDimensions = 5 * max((nWords + nActions),
            len(MTS.trainingData))
    
    # Extract all the SPs and TMs parameters
    for moduleName in model.modules:
        
        if moduleName.endswith('SP'):
            nonMutableParams[moduleName + '___inputDimensions'] = inputDimensions
            nonMutableParams[moduleName + '___columnDimensions'] = (columnDimensions,)
            nonMutableParams[moduleName + '___localAreaDensity'] = -1.0
            nonMutableParams[moduleName + '___seed'] = model.spSeed
            nonMutableParams[moduleName + '___spVerbosity'] = 0
            
            paramList.append(Parameter(
                name='generalSP___potentialRadius',
                dataType='int',
                value=297,
                minVal=1,
                maxVal=297,
                maxChange=29,
                mutationProb=1.0
            )) 
            paramList.append(Parameter(
                name='generalSP___potentialPct',
                dataType='float',
                value=0.726248028695,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.3,
                mutationProb=1.0
            )) 
            paramList.append(Parameter(
                name='generalSP___globalInhibition',
                dataType='bool',
                value=True,
                minVal=0,
                maxVal=9223372036854775807,
                maxChange=9223372036854775807,
                mutationProb=0.5
            )) 
            paramList.append(Parameter(
                name='generalSP___numActiveColumnsPerInhArea',
                dataType='float',
                value=4.0,
                minVal=0.0,
                maxVal=297,
                maxChange=2.0,
                mutationProb=1.0
            )) 
            paramList.append(Parameter(
                name='generalSP___stimulusThreshold',
                dataType='int',
                value=0,
                minVal=0,
                maxVal=10,
                maxChange=5,
                mutationProb=1.0
            )) 
            paramList.append(Parameter(
                name='generalSP___synPermInactiveDec',
                dataType='float',
                value=0.121754178434,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.3,
                mutationProb=1.0
            )) 
            paramList.append(Parameter(
                name='generalSP___synPermActiveInc',
                dataType='float',
                value=0.1,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.3,
                mutationProb=1.0
            )) 
            paramList.append(Parameter(
                name='generalSP___synPermConnected',
                dataType='float',
                value=0.107148493503,
                minVal=0.0,
                maxVal=0.9,
                maxChange=0.3,
                mutationProb=1.0
            )) 
            paramList.append(Parameter(
                name='generalSP___minPctOverlapDutyCycle',
                dataType='float',
                value=0.137190887797,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.2,
                mutationProb=1.0
            )) 
            paramList.append(Parameter(
                name='generalSP___minPctActiveDutyCycle',
                dataType='float',
                value=0.1,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.2,
                mutationProb=1.0
            )) 
            paramList.append(Parameter(
                name='generalSP___dutyCyclePeriod',
                dataType='int',
                value=15,
                minVal=1,
                maxVal=200,
                maxChange=10,
                mutationProb=1.0
            )) 
            paramList.append(Parameter(
                name='generalSP___maxBoost',
                dataType='float',
                value=1.0,
                minVal=1.0,
                maxVal=50.0,
                maxChange=4.0,
                mutationProb=1.0
            )) 
            paramList.append(Parameter(
                name='generalSP___wrapAround',
                dataType='bool',
                value=False,
                minVal=0,
                maxVal=9223372036854775807,
                maxChange=9223372036854775807,
                mutationProb=0.5
            ))
        
        elif moduleName.endswith('TM'):
            nonMutableParams[moduleName + '___columnDimensions'] = (columnDimensions,)
            nonMutableParams[moduleName + '___seed'] = model.tmSeed
            
            
            paramList.append(Parameter(
                name='generalTM___cellsPerColumn',
                dataType='int',
                value=64,
                minVal=1,
                maxVal=500,
                maxChange=15,
                mutationProb=1.0
            )) 
            paramList.append(Parameter(
                name='generalTM___activationThreshold',
                dataType='int',
                value=1,
                minVal=1,
                maxVal=499,
                maxChange=5,
                mutationProb=1.0
            )) 
            paramList.append(Parameter(
                name='generalTM___initialPermanence',
                dataType='float',
                value=0.22382208699,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.3,
                mutationProb=1.0
            )) 
            paramList.append(Parameter(
                name='generalTM___connectedPermanence',
                dataType='float',
                value=0.674714438958,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.3,
                mutationProb=1.0
            )) 
            paramList.append(Parameter(
                name='generalTM___minThreshold',
                dataType='int',
                value=4,
                minVal=1,
                maxVal=100,
                maxChange=5,
                mutationProb=1.0
            )) 
            paramList.append(Parameter(
                name='generalTM___maxNewSynapseCount',
                dataType='int',
                value=4,
                minVal=1,
                maxVal=20,
                maxChange=3,
                mutationProb=1.0
            )) 
            paramList.append(Parameter(
                name='generalTM___permanenceIncrement',
                dataType='float',
                value=0.117671359444,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.3,
                mutationProb=1.0
            )) 
            paramList.append(Parameter(
                name='generalTM___permanenceDecrement',
                dataType='float',
                value=0.52118115778,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.3,
                mutationProb=1.0
            )) 
            paramList.append(Parameter(
                name='generalTM___predictedSegmentDecrement',
                dataType='float',
                value=0.0,
                minVal=0.0,
                maxVal=1.0,
                maxChange=0.2,
                mutationProb=1.0
            )) 
            
    #nonMutableParams['model'] = model
    #nonMutableParams['trainIterations'] = 2
    #nonMutableParams['trainMaxTime'] = 1
    #nonMutableParams['testsMaxTime'] = 1
    
    nonMutableParams['model'] = model
    nonMutableParams['trainIterations'] = 50
    nonMutableParams['trainMaxTime'] = 30
    nonMutableParams['testsMaxTime'] = 15
    
    paramsFinder = ParametersFinder(
        getModelScore, 
        paramList,
        nonOptimParams=nonMutableParams
    )
    bestParameters = paramsFinder.findParams(
        populationSize=4,
        maxMutations=4,
        variety=3,
        elitism=1,
        selectionTechnique='RouletteWheel',
        randomizeFirstGen=True,
        maxIterations=-1,
        maxTime=20 * 60, #hours
        #maxTime=-1,
        minScore=95,
        nParallelEvals=4,
        savingFrequency=2,
        verbosity=2
    )
    
    #print("Saving the model...")
    #with open((fileName + '.pck'), 'wb') as modelFile:
        #cPickle.dump(model, modelFile, -1)
    #print("Done!")

    #app = QApplication([])
    #window = MainWindow(model)
    #app.exec_()
    #sys.exit(app.exec_())
