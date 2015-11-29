#!python2
#-*- coding: utf-8 -*-
#  main.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-11-04
#  Fecha última modificación: 2015-11-04
#  Versión: 1.01

import sys
from PyQt5.QtWidgets import QApplication
from GUI.MainWindow import MainWindow
from Learning import EncoderFactory
from Learning.LearningModels import *
from Learning import MovementTrainingSet as MTS

if __name__ == '__main__':
    
    #print("Unified Encoder")
    #wordEncoder = actionEncoder = EncoderFactory.unifiedCategoryEnc(MTS.categories)
    print("Randomized Letter Encoder")
    wordEncoder = actionEncoder = EncoderFactory.RandomizedLetterEncoder(200, 10)
    structure = ClassicModel(wordEncoder, actionEncoder, MTS)
    structure.train(80, verbose=0)
    
    app = QApplication([])
    window = MainWindow(structure)
    sys.exit(app.exec_())
