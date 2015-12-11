#!python2
#-*- coding: utf-8 -*-
#  main.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-11-04
#  Fecha última modificación: 2015-12-01
#  Versión: 1.2

import sys
import cPickle
import TestSuite
from PyQt5.QtWidgets import QApplication
from GUI.MainWindow import MainWindow
from Learning import EncoderFactory
from Learning.LearningModels import *
from Learning import MovementTrainingSet as MTS

if __name__ == '__main__':

    wordEncoder = actionEncoder = EncoderFactory.UnifiedCategoryEncoder(MTS.categories)
    #wordEncoder = actionEncoder = EncoderFactory.RandomizedLetterEncoder(300, 10)
    #wordEncoder = actionEncoder = EncoderFactory.TotallyRandomEncoder(50, 10)
    encoderName = wordEncoder.__class__.__name__

    #model = ClassicModel(wordEncoder, actionEncoder, MTS)
    model = OneRegionModel(wordEncoder, actionEncoder, MTS)
    model.train(1, verbose=0)
    modelName = model.__class__.__name__
    
    print(modelName)
    print(encoderName)

    modelDescription = "{0}\n{1}\n{2}\n{3}".format(modelName,
        model.__doc__, encoderName, wordEncoder.__doc__)
    # Strips the 'Model' fron the name
    fileName = modelName[:-5] + '-'
    # Appends only the Capital letters
    fileName += ''.join(cap for cap in encoderName if cap.isupper())
    
    TestSuite.testModel(model, MTS.trainingData, modelDescription, 
        fileName=(fileName + '_Results'))

    print("Saving the model...")
    with open((fileName + '.pck'), 'wb') as modelFile:
        cPickle.dump(model, modelFile, -1)
    print("Done!")

    #app = QApplication([])
    #window = MainWindow(model)
    #app.exec_()
    #sys.exit(app.exec_())
