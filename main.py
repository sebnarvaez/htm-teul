#!python2
#-*- coding: utf-8 -*-
#  main.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-11-04
#  Fecha última modificación: 2015-12-01
#  Versión: 1.2

import sys
import cPickle
from PyQt5.QtWidgets import QApplication
from GUI.MainWindow import MainWindow
from Learning import EncoderFactory
from Learning.LearningModels import *
from Learning import MovementTrainingSet as MTS

if __name__ == '__main__':
    
    print("Unified Category Encoder")
    wordEncoder = actionEncoder = EncoderFactory.unifiedCategoryEnc(MTS.categories)
    #print("Randomized Letter Encoder")
    #wordEncoder = actionEncoder = EncoderFactory.RandomizedLetterEncoder(200, 10)
    #print("Totally Random Encoder")
    #wordEncoder = actionEncoder = EncoderFactory.TotallyRandomEncoder(50, 10)
    
    structure = ClassicModel(wordEncoder, actionEncoder, MTS.categories,
        MTS.inputIdx)
    structure.train(MTS.trainingData, 15, verbose=0)
    
    #print("Saving the structure...")
    ##with open('UCE_Structure.pck', 'wb') as structureFile:
    ##with open('RLE_Structure.pck', 'wb') as structureFile:
    #with open('TRE_Structure.pck', 'wb') as structureFile:
        #cPickle.dump(structure, structureFile, -1)
    #print("Done!")
    app = QApplication([])
    window = MainWindow(structure)
    app.exec_()
    #sys.exit(app.exec_())
