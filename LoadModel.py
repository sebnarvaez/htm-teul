#!python2
#-*- coding: utf-8 -*-
#  main.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-11-30
#  Fecha última modificación: 2015-12-01
#  Versión: 1.1 [Stable]

import sys
import cPickle
import TestSuite
from PyQt5.QtWidgets import QApplication
from GUI.MainWindow import MainWindow
from Learning import MovementTrainingSet as MTS

if __name__ == '__main__':
    
    encoder = None
    model = None
    
    print("Loading the model...")
    modelName = "Classic Model"
    encoderName = "Unified Category Encoder"
    #encoderName = "Randomized Letter Encoder"
    #encoderName = "Totally Random Encoder"
    
    with open('Classic-UCE.pck', 'rb') as modelFile:
    #with open('Classic-RLE.pck', 'rb') as modelFile:
    #with open('Classic-TRE.pck', 'rb') as modelFile:
        model = cPickle.load(modelFile)
        
    print("Done!")
    #model.train(MTS.trainingData, 5, verbose=0)
    
    #modelDescription = "{0}\n{1}\n{2}\n{3}".format(modelName, model.__doc__,
    #    encoderName, model.wordEncoder.__doc__)
    #TestSuite.testModel(model, MTS.trainingData, modelDescription)
    
    app = QApplication([])
    window = MainWindow(model)
    app.exec_()
    #sys.exit(app.exec_())
