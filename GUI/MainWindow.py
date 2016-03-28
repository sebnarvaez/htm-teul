#!python2
#-*- coding: utf-8 -*-
#  MainWindow.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-10-27
#  Fecha última modificación: 2015-11-22
#  Versión: 1.2 [Stable]

from VirtualWorld import VirtualWorld
from functools import partial
from PyQt5 import uic

class MainWindow:

    def __init__(self, model):
        
        self.model = model
        
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
        
        self.frame.btn_grab.clicked.connect(self.world.grabObj)
        
        self.frame.btn_speak.clicked.connect(self.talk)
        
        self.frame.btn_insertObj.clicked.connect(self.insertObj)
        
        self.frame.btn_execSentence.clicked.connect(self.execSentence)
        self.frame.lnEdt_sentence_execute.returnPressed.connect(
            self.execSentence)
        
        self.frame.btn_clearLog.clicked.connect(self.frame.txtEdt_log.clear)
        
        self.frame.cmbBx_action.currentIndexChanged.connect(
            self.actionForTrainChanged,
        )
    
    def execSentence(self):
        
        sentence = self.frame.lnEdt_sentence_execute.text().lower()
        
        if (sentence == None) or (not sentence):
            sentence = "-"
        
        self.frame.txtEdt_log.append("<b>>></b> " + sentence)
        sentence = sentence.split()
        predictions = self.model.inputSentence(sentence, verbosity=2,
            learn=False)
        
        task = predictions[0]
        argument = predictions[1][:-6]
        
        if task == 'mover-event':
            self.frame.txtEdt_log.append(self.world.moveObj('P1', argument))
            
        elif task == 'recoger-event':
            self.frame.append(self.world.grabObj())
        
        elif task == 'hablar-event':
            self.talk(argument)
        
        else:
            self.frame.txtEdt_log.append('<font color="Red">'\
                'P1: No se que hacer'\
                '</font><br>')
            
        self.model.reset()
    
    def talk(self, speech=None):
        """ Displays a sentence in the log """
        
        if (speech == None) or (not speech):
            speech = self.frame.lnEdt_speak.displayText()
        
        self.frame.txtEdt_log.append('<font color="Green">'\
            'P1: ' + speech +\
            '</font><br>')
    
    def actionForTrainChanged(self):
        
        newAction = self.frame.cmbBx_action.currentText()
        print(newAction)
        self.frame.lnEdt_argument.setEnabled((newAction == 'Saludar') or\
            (newAction == 'Hablar'))
    
    def insertObj(self):
        
        objType = self.frame.cmbBx_insertObj.currentText()
        self.world.insertObj(objType)
