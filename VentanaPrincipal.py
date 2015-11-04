#!python2
#-*- coding: utf-8 -*-
#  2SP-2TP-SP.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-10-27
#  Fecha última modificación: 2015-10-21
#  Versión: 1.01

import sys
from MundoVirtual import *
from LearningStructure import *
from functools import partial
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication

class GuiPrincipal:

    def __init__(self):

        self.structure = LearningStructure()
        self.structure.train(10)
        
        app = QApplication([])
        self.frame = uic.loadUi('VirtualWorld.ui')
        self.world = VirtualWorld(self.frame)
        
        self.configFrame()
        self.configVirtualWorld()
        
        self.frame.show()
        
        sys.exit(app.exec_())
        
    def configVirtualWorld(self):
    
        self.world.setMinimumWidth(500)
        self.world.setMinimumHeight(600)
        self.world.setFocus()
        
    def configFrame(self):
        
        self.frame.virtualWorld = self.world
        self.initEvents()
    
    def initEvents(self):
    
        self.frame.btn_left.clicked.connect(partial(self.world.moveP1, direction = 'izquierda'))
        self.frame.btn_right.clicked.connect(partial(self.world.moveP1, direction = 'derecha'))
        self.frame.btn_up.clicked.connect(partial(self.world.moveP1, direction = 'arriba'))
        self.frame.btn_down.clicked.connect(partial(self.world.moveP1, direction = 'abajo'))
        self.frame.btn_execSentence.clicked.connect(self.execSentence)
    
    def execSentence(self):
        
        sentence = self.frame.lnEdt_sentence.text().split()
        predictions = self.structure.layer.inputSentence(sentence, [], 1, learn = False)
        if predictions[0] == 'action-mover':
            self.world.moveP1(predictions[1][7:])
        self.structure.wordTM.reset()
        self.structure.actionTM.reset()
        self.structure.generalTM.reset()

GuiPrincipal()
