#!python2
#-*- coding: utf-8 -*-
#  MainWindow.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-10-27
#  Fecha última modificación: 2015-10-21
#  Versión: 1.01

from VirtualWorld import VirtualWorld
from functools import partial
from PyQt5 import uic

class MainWindow:

    def __init__(self, structure):
        
        self.structure = structure
        
        self.frame = uic.loadUi('GUI/MainWindow.ui')
        self.world = VirtualWorld(self.frame)
        
        self.configFrame()
        self.configVirtualWorld()
        
        self.frame.show()
        
    def configFrame(self):
        
        self.frame.virtualWorld = self.world
        self.initEvents()
        
    def configVirtualWorld(self):
    
        self.world.setMinimumWidth(500)
        self.world.setMinimumHeight(600)
        self.world.setFocus()
    
    def initEvents(self):
    
        self.frame.btn_left.clicked.connect(partial(self.world.moveObj,
            objId="P1", direction='izquierda'))
        self.frame.btn_right.clicked.connect(partial(self.world.moveObj,
            objId="P1",  direction='derecha'))
        self.frame.btn_up.clicked.connect(partial(self.world.moveObj,
            objId="P1", direction='arriba'))
        self.frame.btn_down.clicked.connect(partial(self.world.moveObj,
            objId="P1", direction='abajo'))
        self.frame.btn_execSentence.clicked.connect(self.execSentence)
        self.frame.btn_clearLog.clicked.connect(self.frame.txtEdt_log.clear)
    
    def execSentence(self):
        
        sentence = self.frame.lnEdt_sentence.text()
        
        if sentence == None:
            sentence = ""
        
        self.frame.txtEdt_log.append("<b>>></b>" + sentence)
        sentence = sentence.split()
        predictions = self.structure.inputSentence(sentence, verbose=1,
            learn=False)
        
        if predictions[0] == 'action-mover':
            self.frame.txtEdt_log.append(self.world.moveObj('P1', predictions[1][7:]))
            
        self.structure.wordTM.reset()
        self.structure.actionTM.reset()
        self.structure.generalTM.reset()

