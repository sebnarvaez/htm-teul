#!python2
#-*- coding: utf-8 -*-
#  VentanaPrincipal.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-10-22
#  Fecha última modificación: 2015-10-22
#  Versión: 0.1

"""
ZetCode PyQt5 tutorial 

This is a VentanaPrincipal game clone.

author: Jan Bodnar
website: zetcode.com 
last edited: January 2015
"""

import sys, random
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication,\
    QLabel, QGridLayout
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QSize
from PyQt5.QtGui import QPainter, QColor, QPixmap

resourcesPath = 'Resources/'
imgPaths = {
    'ectatomma' : resourcesPath + 'Ectatomma.png',
    'ectatomma-hunter' : resourcesPath + 'Ectatomma-Hunter.png',
    'ectatomma-nurse' : resourcesPath + 'Ectatomma-Nurse.png',
    'hat-hunter' : resourcesPath + 'Hat-Hunter.png',
    'hat-nurse' : resourcesPath + 'Hat-Nurse.png'
}

class VirtualWorld(QFrame):
    
    worldGrid = []
    numColumns = 5
    numRows = 5
    #Speed = 300

    def __init__(self, parent):
        super(VirtualWorld, self).__init__(parent)
        
        self.initVirtualWorld()
        
        
    def initVirtualWorld(self):     

        #self.timer = QBasicTimer()
        self.resize(500, 600)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setLineWidth(1)
        
        self.p1 = WorldObject(
            'ectatomma',
            3,
            3,
            (self.width() // self.numColumns) - 10,
            (self.height() // self.numRows) - 10
        )

        grid = QGridLayout()
        self.setLayout(grid)
        
        for column in range(self.numColumns):
            self.worldGrid.append([])
            for row in range(self.numRows):
                self.worldGrid[column].append(QLabel())
                self.worldGrid[column][row].setStyleSheet(
                    "QLabel { background-color : green }"
                )
                grid.addWidget(self.worldGrid[column][row], column, row)
        
        self.worldGrid[self.p1.y][self.p1.x].setPixmap(self.p1.pixmap)
                
    def moveP1(self, direction):
        if direction == 'izquierda':
            if self.p1.x > 0: 
                self.worldGrid[self.p1.y][self.p1.x].setPixmap(QPixmap())
                self.p1.x += -1 
                self.worldGrid[self.p1.y][self.p1.x].setPixmap(self.p1.pixmap)
            return "Me he movido a la izquierda\n"
            
        elif direction == 'derecha':
            if self.p1.x < self.numColumns - 1:
                self.worldGrid[self.p1.y][self.p1.x].setPixmap(QPixmap())
                self.p1.x += 1 
                self.worldGrid[self.p1.y][self.p1.x].setPixmap(self.p1.pixmap)
            return "Me he movido a la derecha\n"
            
        elif direction == 'arriba':
            if self.p1.y > 0: 
                self.worldGrid[self.p1.y][self.p1.x].setPixmap(QPixmap())
                self.p1.y += -1
                self.worldGrid[self.p1.y][self.p1.x].setPixmap(self.p1.pixmap)
            return "Me he movido hacia arriba\n"
            
        elif direction == 'abajo':
            if self.p1.y < self.numRows - 1: 
                self.worldGrid[self.p1.y][self.p1.x].setPixmap(QPixmap())
                self.p1.y += 1
                self.worldGrid[self.p1.y][self.p1.x].setPixmap(self.p1.pixmap)
            return "Me he movido hacia abajo\n"
        
        else:
            return "No se a que direccion moverme"
            
class WorldObject:
    
    def __init__(self, objType, x, y, imgWidth, imgHeight):
        
        self.x = x
        self.y = y
        self.img = imgPaths[objType]
        self.pixmap = QPixmap(self.img).scaled(imgWidth, imgHeight, Qt.KeepAspectRatio)
        
    def resizePixmap(self, imgWidth, imgHeight):
        self.pixmap = self.pixmap.scaled(imgWidth, imgHeight, Qt.KeepAspectRatio)

if __name__ == '__main__':
    
    app = QApplication([])
    mundo = QMainWindow()
    tboard = VirtualWorld(mundo)
    mundo.setCentralWidget(tboard)
    
    mundo.resize(500, 600)
    mundo.setWindowTitle('Virtual World')
    mundo.show()

    screen = QDesktopWidget().screenGeometry()
    size = mundo.geometry()
    mundo.move((screen.width()-size.width())/2, 
        (screen.height()-size.height())/2)
    
    sys.exit(app.exec_())
