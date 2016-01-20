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

def getModelScore(model, trainIterations, trainMaxTime, **modelParams):
    
    
    model.train(trainIterations, maxTime=trainMaxTime, verbosity=0)
    results = TestSuite.testModel(model, MTS.trainingData, saveResults=False)
    
    return results[successPercent]

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
    
    nWords = len(MTS.categories[inputIdx['wordInput']])
    nActions = len(MTS.categories[inputIdx['actionInput']])
    
    inputDimensions = max(
        self.wordEncoder.getWidth(),
        self.actionEncoder.getWidth()
    )
    
    columnDimensions = 4 * max((nWords + nActions),
            len(self.trainingData))
    
    nonMutableParams['model'] = model
    nonMutableParams['trainIterations'] = 50
    nonMutableParams['trainMaxTime'] = 30
    
    # Extract all the SPs and TMs parameters
    for moduleName in model.modules:
        
        if moduleName.endswith('SP'):
            nonMutableParams[moduleName + '___inputDimensions'] = inputDimensions
            nonMutableParams[moduleName + '___columnDimensions'] = (columnDimensions,)
            nonMutableParams[moduleName + '___localAreaDensity'] = -1.0
            nonMutableParams[moduleName + '___seed'] = model.spSeed
            nonMutableParams[moduleName + '___spVerbosity'] = 0
            
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
                    minVal=0,
                    maxVal=1,
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
                    minVal=0,
                    maxVal=1,
                    maxChange=0.1
                ))
            paramList.append(Parameter(
                    moduleName + '___synPermActiveInc',
                    'float', 
                    value=0.1,
                    minVal=0,
                    maxVal=1,
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
                    value=20,
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
                    value=0.5,
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
                    value=0.05,
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
        
        elif moduleName.endswith('classifier'):
            nonMutableParams[moduleName + '___steps'] = 
            
    paramsFinder = ParametersFinder(5)
    bestParameters = paramsFinder.findParams(
            evalFunc,
            (
                Parameter('a', 'int', minVal=0, maxVal=50, maxChange=5),
                Parameter('b', 'int', minVal=0, maxVal=50, maxChange=5)
            ),
            variety=2,
            maxTime=-1,
            maxIterations=-1,
            minScore=50
        )

    #print("Saving the model...")
    #with open((fileName + '.pck'), 'wb') as modelFile:
        #cPickle.dump(model, modelFile, -1)
    #print("Done!")

    #app = QApplication([])
    #window = MainWindow(model)
    #app.exec_()
    #sys.exit(app.exec_())
