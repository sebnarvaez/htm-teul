#!python2
#-*- coding: utf-8 -*-
#  OptimizeModel.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2016-01-19
#  Fecha última modificación: 2016-01-19
#  Versión: 1.2

import sys
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

def getModelScore(model, trainIterations, trainMaxTime, **modelParams):
    
    paramsByModule = {}
    
    #print("Evaluating {}".format(modelParams))
    
    for model___param in modelParams:
        moduleName, paramName = model___param.split('___')
        
        if moduleName not in paramsByModule:
            paramsByModule[moduleName] = {}
        
        #print("model_paramName: {}".format(modelParams[model___param]))
        paramsByModule[moduleName][paramName] = modelParams[model___param]
    
    for moduleName in paramsByModule:
        model.modules[moduleName] = model.modules[moduleName].__class__(
                **paramsByModule[moduleName])
    
    print('\n-----------------------------\n')
    
    print(model.spParametersStr())
    print(model.tmParametersStr())
    
    print('Training...')
    
    model.train(trainIterations, maxTime=trainMaxTime, verbosity=0)
    results = TestSuite.testModel(model, MTS.trainingData, saveResults=False)
    
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
    nonMutableParams['model'] = model
    nonMutableParams['trainIterations'] = 20
    nonMutableParams['trainMaxTime'] = 30
    
    nWords = len(MTS.categories[MTS.inputIdx['wordInput']])
    nActions = len(MTS.categories[MTS.inputIdx['actionInput']])
    
    inputDimensions = max(
        wordEncoder.getWidth(),
        actionEncoder.getWidth()
    )
    
    columnDimensions = 4 * max((nWords + nActions),
            len(MTS.trainingData))
    
    # Extract all the SPs and TMs parameters
    for moduleName in model.modules:
        
        if moduleName.endswith('SP'):
            nonMutableParams[moduleName + '___inputDimensions'] = inputDimensions
            nonMutableParams[moduleName + '___columnDimensions'] = (columnDimensions,)
            nonMutableParams[moduleName + '___localAreaDensity'] = -1.0
            nonMutableParams[moduleName + '___seed'] = model.spSeed
            nonMutableParams[moduleName + '___spVerbosity'] = 0
            
            Parameter(
name='generalTM___cellsPerColumn',
            dataType='int',
            value=80,
            minVal=1,
            maxVal=500,
            maxChange=5,
            mutationProb=1.0),
            
            Parameter(
name='generalTM___activationThreshold',
            dataType='int',
            value=4,
            minVal=1,
            maxVal=499,
            maxChange=5,
            mutationProb=1.0),
            
            Parameter(
name='generalTM___initialPermanence',
            dataType='float',
            value=0.22382208699,
            minVal=0.0,
            maxVal=1.0,
            maxChange=0.1,
            mutationProb=1.0),
            
            Parameter(
name='generalTM___connectedPermanence',
            dataType='float',
            value=0.575611110106,
            minVal=0.0,
            maxVal=1.0,
            maxChange=0.1,
            mutationProb=1.0),
            
            Parameter(
name='generalTM___minThreshold',
            dataType='int',
            value=4,
            minVal=1,
            maxVal=100,
            maxChange=4,
            mutationProb=1.0),
            
            Parameter(
name='generalTM___maxNewSynapseCount',
            dataType='int',
            value=4,
            minVal=1,
            maxVal=20,
            maxChange=2,
            mutationProb=1.0),
            
            Parameter(
name='generalTM___permanenceIncrement',
            dataType='float',
            value=0.117671359444,
            minVal=0.0,
            maxVal=1.0,
            maxChange=0.1,
            mutationProb=1.0),
            
            Parameter(
name='generalTM___permanenceDecrement',
            dataType='float',
            value=0.143945674364,
            minVal=0.0,
            maxVal=1.0,
            maxChange=0.1,
            mutationProb=1.0),
            
            Parameter(
name='generalTM___predictedSegmentDecrement',
            dataType='float',
            value=0.0,
            minVal=0.0,
            maxVal=1.0,
            maxChange=0.05,
            mutationProb=1.0),
            
            Parameter(
name='generalSP___potentialRadius',
            dataType='int',
            value=297,
            minVal=1,
            maxVal=297,
            maxChange=29,
            mutationProb=1.0),
            
            Parameter(
name='generalSP___potentialPct',
            dataType='float',
            value=0.5,
            minVal=0.0,
            maxVal=1.0,
            maxChange=0.1,
            mutationProb=1.0),
            
            Parameter(
name='generalSP___globalInhibition',
            dataType='bool',
            value=True,
            minVal=0,
            maxVal=9223372036854775807,
            maxChange=9223372036854775807,
            mutationProb=0.5),
            
            Parameter(
name='generalSP___numActiveColumnsPerInhArea',
            dataType='float',
            value=4.0,
            minVal=0.0,
            maxVal=297,
            maxChange=1.0,
            mutationProb=1.0),
            
            Parameter(
name='generalSP___stimulusThreshold',
            dataType='int',
            value=0,
            minVal=0,
            maxVal=10,
            maxChange=1,
            mutationProb=1.0),
            
            Parameter(
name='generalSP___synPermInactiveDec',
            dataType='float',
            value=0.121754178434,
            minVal=0.0,
            maxVal=1.0,
            maxChange=0.1,
            mutationProb=1.0),
            
            Parameter(
name='generalSP___synPermActiveInc',
            dataType='float',
            value=0.1,
            minVal=0.0,
            maxVal=1.0,
            maxChange=0.1,
            mutationProb=1.0),
            
            Parameter(
name='generalSP___synPermConnected',
            dataType='float',
            value=0.15,
            minVal=0.0,
            maxVal=0.9,
            maxChange=0.1,
            mutationProb=1.0),
            
            Parameter(
name='generalSP___minPctOverlapDutyCycle',
            dataType='float',
            value=0.1,
            minVal=0.0,
            maxVal=1.0,
            maxChange=0.05,
            mutationProb=1.0),
            
            Parameter(
name='generalSP___minPctActiveDutyCycle',
            dataType='float',
            value=0.1,
            minVal=0.0,
            maxVal=1.0,
            maxChange=0.05,
            mutationProb=1.0),
            
            Parameter(
name='generalSP___dutyCyclePeriod',
            dataType='int',
            value=16,
            minVal=1,
            maxVal=200,
            maxChange=5,
            mutationProb=1.0),
            
            Parameter(
name='generalSP___maxBoost',
            dataType='float',
            value=3.0,
            minVal=1.0,
            maxVal=50.0,
            maxChange=2.0,
            mutationProb=1.0),
            
            Parameter(
name='generalSP___wrapAround',
            dataType='bool',
            value=True,
            minVal=0,
            maxVal=9223372036854775807,
            maxChange=9223372036854775807,
            mutationProb=0.5)
            
            paramList.append(Parameter(
                    moduleName + '___potentialRadius',
                    'int', 
                    value=inputDimensions,
                    minVal=1,
                    maxVal=inputDimensions,
                    maxChange=inputDimensions/10
                ))
            paramList.append(Parameter(
                    moduleName + '___potentialPct',
                    'float', 
                    value=0.5,
                    minVal=0.0,
                    maxVal=1.0,
                    maxChange=0.1
                ))
            paramList.append(Parameter(
                    moduleName + '___globalInhibition',
                    'bool',
                    value=True,
                    mutationProb=0.5
                ))
            paramList.append(Parameter(
                    moduleName + '___numActiveColumnsPerInhArea',
                    'float', 
                    value=4.0,
                    minVal=0.0,
                    maxVal=inputDimensions,
                    maxChange=1.0
                ))
            paramList.append(Parameter(
                    moduleName + '___stimulusThreshold',
                    'int', 
                    value=0,
                    minVal=0,
                    maxVal=10,
                    maxChange=1
                ))
            paramList.append(Parameter(
                    moduleName + '___synPermInactiveDec',
                    'float', 
                    value=0.1,
                    minVal=0.0,
                    maxVal=1.0,
                    maxChange=0.1
                ))
            paramList.append(Parameter(
                    moduleName + '___synPermActiveInc',
                    'float', 
                    value=0.1,
                    minVal=0.0,
                    maxVal=1.0,
                    maxChange=0.1
                ))
            paramList.append(Parameter(
                    moduleName + '___synPermConnected',
                    'float', 
                    value=0.15,
                    minVal=0.0,
                    maxVal=0.9,
                    maxChange=0.1
                ))
            paramList.append(Parameter(
                    moduleName + '___minPctOverlapDutyCycle',
                    'float', 
                    value=0.1,
                    minVal=0.0,
                    maxVal=1.0,
                    maxChange=0.05
                ))
            paramList.append(Parameter(
                    moduleName + '___minPctActiveDutyCycle',
                    'float', 
                    value=0.1,
                    minVal=0.0,
                    maxVal=1.0,
                    maxChange=0.05
                ))
            paramList.append(Parameter(
                    moduleName + '___dutyCyclePeriod',
                    'int', 
                    value=16,
                    minVal=1,
                    maxVal=200,
                    maxChange=5
                ))
            paramList.append(Parameter(
                    moduleName + '___maxBoost',
                    'float', 
                    value=3.0,
                    minVal=1.0,
                    maxVal=50.0,
                    maxChange=2.0
                ))
            paramList.append(Parameter(
                    moduleName + '___wrapAround',
                    'bool', 
                    value=True,
                    mutationProb=0.5
                ))
        
        elif moduleName.endswith('TM'):
            nonMutableParams[moduleName + '___columnDimensions'] = (columnDimensions,)
            nonMutableParams[moduleName + '___seed'] = model.tmSeed
            
            paramList.append(Parameter(
                    moduleName + '___cellsPerColumn',
                    'int', 
                    value=80,
                    minVal=1,
                    maxVal=500,
                    maxChange=5
                ))
            paramList.append(Parameter(
                    moduleName + '___activationThreshold',
                    'int', 
                    value=4,
                    minVal=1,
                    maxVal=499,
                    maxChange=5
                ))
            paramList.append(Parameter(
                    moduleName + '___initialPermanence',
                    'float', 
                    value=0.3,
                    minVal=0.0,
                    maxVal=1.0,
                    maxChange=0.1
                ))
            paramList.append(Parameter(
                    moduleName + '___connectedPermanence',
                    'float', 
                    value=0.575611110106,
                    minVal=0.0,
                    maxVal=1.0,
                    maxChange=0.1
                ))
            paramList.append(Parameter(
                    moduleName + '___minThreshold',
                    'int', 
                    value=4,
                    minVal=1,
                    maxVal=100,
                    maxChange=4
                ))
            paramList.append(Parameter(
                    moduleName + '___maxNewSynapseCount',
                    'int', 
                    value=4,
                    minVal=1,
                    maxVal=20,
                    maxChange=2
                ))
            paramList.append(Parameter(
                    moduleName + '___permanenceIncrement',
                    'float', 
                    value=0.05,
                    minVal=0.0,
                    maxVal=1.0,
                    maxChange=0.1
                ))
            paramList.append(Parameter(
                    moduleName + '___permanenceDecrement',
                    'float', 
                    value=0.143945674364,
                    minVal=0.0,
                    maxVal=1.0,
                    maxChange=0.1
                ))
            paramList.append(Parameter(
                    moduleName + '___predictedSegmentDecrement',
                    'float', 
                    value=0.0,
                    minVal=0.0,
                    maxVal=1.0,
                    maxChange=0.05
                ))
    
    paramsFinder = ParametersFinder(
        getModelScore, 
        paramList,
        nonOptimParams=nonMutableParams
    )
    bestParameters = paramsFinder.findParams(
        populationSize=4,
        maxMutations=4,
        variety=3,
        maxIterations=-1,
        maxTime=60 * 8, #hours
        #maxTime=-1,
        minScore=98,
        parallelization=True,
        nCores=2,
        savingFrequency=2,
        verbosity=1
    )
    
    #print("Saving the model...")
    #with open((fileName + '.pck'), 'wb') as modelFile:
        #cPickle.dump(model, modelFile, -1)
    #print("Done!")

    #app = QApplication([])
    #window = MainWindow(model)
    #app.exec_()
    #sys.exit(app.exec_())
