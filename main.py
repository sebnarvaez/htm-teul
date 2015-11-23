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
from Learning.TrainingData import *
from Learning.MovementTrainingSet import *

if __name__ == '__main__':
    
    wordEncoder = actionEncoder = EncoderFactory.unifiedCategoryEnc(movementData)
    structure = ClassicModel(wordEncoder, actionEncoder)
    structure.train(movementData, 8, verbose=0)
    
    app = QApplication([])
    window = MainWindow(structure)
    sys.exit(app.exec_())
