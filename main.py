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

    #encoderName = "Unified Category Encoder\n"
    #wordEncoder = actionEncoder = EncoderFactory.unifiedCategoryEnc(MTS.categories)
    encoderName = "Randomized Letter Encoder\n"
    wordEncoder = actionEncoder = EncoderFactory.RandomizedLetterEncoder(300, 10)
    #encoderName = "Totally Random Encoder\n"
    #wordEncoder = actionEncoder = EncoderFactory.TotallyRandomEncoder(50, 10)
    print(encoderName)

    modelName = "Classic Model"
    model = ClassicModel(wordEncoder, actionEncoder, MTS)
    model.train(50, verbose=0)

    modelDescription = "{0}\n{1}\n{2}\n{3}".format(modelName, model.__doc__,
        encoderName, wordEncoder.__doc__)
    TestSuite.testModel(model, MTS.trainingData, modelDescription, 
        fileName='Classic-RLE_Results')

    #print("Saving the model...")
    #with open('Classic-UCE.pck', 'wb') as modelFile:
    #with open('Classic-RLE.pck', 'wb') as modelFile:
    #with open('Classic-TRE.pck', 'wb') as modelFile:
        #cPickle.dump(model, modelFile, -1)
    #print("Done!")

    app = QApplication([])
    window = MainWindow(model)
    app.exec_()
    #sys.exit(app.exec_())
