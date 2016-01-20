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
