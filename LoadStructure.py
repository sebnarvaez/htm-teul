#!python2
#-*- coding: utf-8 -*-
#  main.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-11-30
#  Fecha última modificación: 2015-12-01
#  Versión: 1.0 [Stable]

import sys
import cPickle
import TestSuite
from PyQt5.QtWidgets import QApplication
from GUI.MainWindow import MainWindow
from Learning import MovementTrainingSet as MTS

if __name__ == '__main__':
    
    encoder = None
    structure = None
    
    print("Loading the structure...")
    modelName = "Classic Model"
    encoderName = "Unified Category Encoder"
    #encoderName = "Randomized Letter Encoder"
    #encoderName = "Totally Random Encoder"
    
    with open('UCE_Structure.pck', 'rb') as structureFile:
    #with open('RLE_Structure.pck', 'rb') as structureFile:
    #with open('TRE_Structure.pck', 'rb') as structureFile:
        structure = cPickle.load(structureFile)
        
    print("Done!")
    #structure.train(MTS.trainingData, 5, verbose=0)
    
    modelDescription = "{0}\n{1}\n{2}\n{3}".format(modelName, structure.__doc__,
        encoderName, structure.wordEncoder.__doc__)
    TestSuite.testModel(structure, MTS.trainingData, modelDescription)
    
    app = QApplication([])
    window = MainWindow(structure)
    app.exec_()
    #sys.exit(app.exec_())
