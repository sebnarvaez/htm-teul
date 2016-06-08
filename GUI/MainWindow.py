#!python2
#-*- coding: utf-8 -*-
#  MainWindow.py
#  Author: Larvasapiens <sebastian.narvaez@correounivalle.edu.co>
#  Created: 2015-10-27
#  Last Modification: 2015-11-22
#  Version: 1.2 [Stable]
#
#  Copyright (C) {2016}  {Sebastián Narváez Rodríguez}
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from VirtualWorld import VirtualWorld
from functools import partial
from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QIntValidator
import imp


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

        # Init the table of inputs widget
        self.frame.tblWdgt_trainingList.setColumnCount(3)
        self.frame.tblWdgt_trainingList.setHorizontalHeaderLabels(
            ['Frase', 'Accion', 'Argumento']
        )
        self.frame.tblWdgt_trainingList.horizontalHeader().setStretchLastSection(
            True)

        self.frame.lnEdt_iterations.setValidator(QIntValidator(0, 1000,
            self.frame))

        self.initEvents()

    def configVirtualWorld(self):

        self.world.setMinimumWidth(500)
        self.world.setMinimumHeight(600)
        self.world.setFocus()

    def initEvents(self):

        self.frame.btn_left.clicked.connect(partial(self.world.moveObj,
            objId="P1", direction='izquierda'))
        self.frame.btn_right.clicked.connect(partial(self.world.moveObj,
            objId="P1", direction='derecha'))
        self.frame.btn_up.clicked.connect(partial(self.world.moveObj,
            objId="P1", direction='arriba'))
        self.frame.btn_down.clicked.connect(partial(self.world.moveObj,
            objId="P1", direction='abajo'))

        self.frame.btn_grab.clicked.connect(self.world.grabObj)

        self.frame.btn_dance.clicked.connect(self.world.dance)

        self.frame.btn_insertObj.clicked.connect(self.insertObj)

        self.frame.btn_execSentence.clicked.connect(self.execSentence)
        self.frame.lnEdt_sentence_execute.returnPressed.connect(
            self.execSentence)

        self.frame.btn_clearLog.clicked.connect(self.frame.txtEdt_log.clear)

        self.frame.btn_addTrainInput.clicked.connect(self.addTrainInput)
        self.frame.lnEdt_sentence_train.returnPressed.connect(
                self.addTrainInput)

        self.frame.btn_train.clicked.connect(self.trainFromInputList)
        self.frame.btn_clear_train.clicked.connect(self.clearInputTable)

    def execSentence(self):

        sentence = self.frame.lnEdt_sentence_execute.text().lower()

        if (sentence is None) or (not sentence):
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
            self.frame.txtEdt_log.append(self.world.grabObj())

        elif task == 'bailar-event':
            self.frame.txtEdt_log.append(self.world.dance())

        else:
            self.frame.txtEdt_log.append('<font color="Red">'
                'P1: No se que hacer'
                '</font><br>')

        self.model.reset()

    def talk(self, speech=None):
        """ Displays a sentence in the log """

        if (speech is None) or (not speech):
            speech = self.frame.lnEdt_speak.displayText()
            self.frame.lnEdt_speak.clear()

        self.frame.txtEdt_log.append('<font color="Green">'
            'P1: ' + speech +
            '</font><br>')

    def addTrainInput(self):
        """
        Adds an input to the list of inputs that will be used for
        training.
        """
        
        sentence = self.frame.lnEdt_sentence_train.text()
        action = self.frame.cmbBx_action.currentText()
        
        if action == 'Mover arriba':
            action = 'mover-event'
            argument = 'arriba-event'
        
        elif action == 'Mover abajo':
            action = 'mover-event'
            argument = 'abajo-event'
        
        elif action == 'Mover izquierda':
            action = 'mover-event'
            argument = 'izquierda-event'
        
        elif action == 'Mover derecha':
            action = 'mover-event'
            argument = 'derecha-event'
        
        elif action == 'Hablar':
            action = 'hablar-event'
            argument = self.frame.lnEdt_argument.text()
            
            if argument == '':
                argument = 'nothing-event'
        
        elif action == 'Bailar':
            action = 'bailar-event'
            argument = 'nothing-event'
        
        elif action == 'Recoger':
            action = 'recoger-event'
            argument = 'nothing-event'
        
        else:
            action = 'nothing-event'
            argument = 'nothing-event'
        
        rowCount = self.frame.tblWdgt_trainingList.rowCount()
        self.frame.tblWdgt_trainingList.setRowCount(rowCount + 1)
        self.frame.tblWdgt_trainingList.setItem(
            rowCount,
            0,
            QTableWidgetItem(sentence)
        )
        self.frame.tblWdgt_trainingList.setItem(
            rowCount,
            1,
            QTableWidgetItem(action)
        )
        self.frame.tblWdgt_trainingList.setItem(
            rowCount,
            2,
            QTableWidgetItem(argument)
        )
        self.frame.tblWdgt_trainingList.resizeColumnsToContents()
    
    def trainFromInputList(self):
        """
        Gets the Input List from the tblWdgt_trainingList and starts
        training the model.
        """
        
        trainingList = []
        sourceTable = self.frame.tblWdgt_trainingList
        
        for row in xrange(sourceTable.rowCount()):
            sentence = sourceTable.item(row, 0).text().split()
            event = [sourceTable.item(row, 1).text(),
                sourceTable.item(row, 2).text()]
            
            trainingList.append((sentence, event))
        
        iterations = int(self.frame.lnEdt_iterations.text())
        self.frame.controlPanel.setEnabled(False)
        self.frame.statusBar().showMessage("Training in progress...")
        self.model.train(iterations, trainingData=trainingList, maxTime=-1,
            verbosity=1)
        self.frame.controlPanel.setEnabled(True)
        self.frame.statusBar().showMessage("Done!", 2000)

    def importInputList(self):
        """
        Opens a file selection window to select the csv where the Inputs
        List is going to be imported from.
        """

        fileData = QFileDialog.getOpenFileName(self.frame, "Import Input List",
            "", "Python Files (*.py)")

        trainingSet = imp.load_source('TrainingSet', fileData[0])

    def clearInputTable(self):

        self.frame.tblWdgt_trainingList.clear()
        self.frame.tblWdgt_trainingList.setRowCount(0)
        self.frame.tblWdgt_trainingList.setHorizontalHeaderLabels(
            ['Frase', 'Accion', 'Argumento']
        )
        self.frame.tblWdgt_trainingList.horizontalHeader().setStretchLastSection(
            True)

    def insertObj(self):
        
        objType = self.frame.cmbBx_insertObj.currentText()
        self.world.insertObj(objType)
