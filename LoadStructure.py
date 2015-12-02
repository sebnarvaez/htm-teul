#!python2
#-*- coding: utf-8 -*-
#  main.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-11-30
#  Fecha última modificación: 2015-12-01
#  Versión: 1.0 [Stable]

import sys
import cPickle
from PyQt5.QtWidgets import QApplication
from GUI.MainWindow import MainWindow
from Learning import MovementTrainingSet as MTS

if __name__ == '__main__':
    
    encoder = None
    structure = None
    
    print("Loading the structure...")
    with open('UCE_Structure.pck', 'rb') as structureFile:
    #with open('RLE_Structure.pck', 'rb') as structureFile:
    #with open('TRE_Structure.pck', 'rb') as structureFile:
        structure = cPickle.load(structureFile)
    
    #structure.train(MTS.trainingData, 5, verbose=0)
    print("Done!")
    
    app = QApplication([])
    window = MainWindow(structure)
    app.exec_()
    #sys.exit(app.exec_())
