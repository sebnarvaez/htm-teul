#!python2
#-*- coding: utf-8 -*-
#  VentanaPrincipal.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-10-22
#  Fecha última modificación: 2015-10-22
#  Versión: 1.1 [Stable]

"""
This code is partly based on ZetCode PyQt5 tutorial 

author: Jan Bodnar
website: zetcode.com 
"""

import sys, random
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication,\
    QLabel, QGridLayout
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QSize
from PyQt5.QtGui import QPainter, QColor, QPixmap

RESOURCES_PATH = 'Resources/'
IMG_PATHS = {
    'ectatomma' : RESOURCES_PATH + 'Ectatomma.png',
    'ectatomma-hunter' : RESOURCES_PATH + 'Ectatomma-Hunter.png',
    'ectatomma-nurse' : RESOURCES_PATH + 'Ectatomma-Nurse.png',
    'hat-hunter' : RESOURCES_PATH + 'Hat-Hunter.png',
    'hat-nurse' : RESOURCES_PATH + 'Hat-Nurse.png'
}

class VirtualWorld(QFrame):
    
    NUM_COLUMNS = 5
    NUM_ROWS = 5
    OBJECTS = dict()

    def __init__(self, parent):
    
        super(VirtualWorld, self).__init__(parent)
        
        self.initVirtualWorld()
        
    def initVirtualWorld(self):     
        
        self.worldGrid = []
        
        self.resize(500, 600)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setLineWidth(1)
        self.CELL_WIDTH = self.width() // self.NUM_COLUMNS
        self.CELL_HEIGHT = self.height() // self.NUM_ROWS

        grid = QGridLayout()
        self.setLayout(grid)
        
        for column in xrange(self.NUM_COLUMNS):
            self.worldGrid.append([])
            
            for row in xrange(self.NUM_ROWS):
                self.worldGrid[column].append(QLabel())
                self.worldGrid[column][row].setStyleSheet(
                    "QLabel { background-color : green }"
                )
                grid.addWidget(self.worldGrid[column][row], column, row)
        
        self.addObj('P1', 'ectatomma', 3, 3)
        
    def addObj(self, objId, objType, x, y, imgWidth = None, imgHeight = None):
        """ Adds an object to the Virtual World """
        
        if imgWidth == None: 
            imgWidth = self.CELL_WIDTH - 10
            
        if imgHeight == None:
            imgHeight = self.CELL_HEIGHT - 10
        obj = WorldObject(objType, x, y, imgWidth, imgHeight)
        self.OBJECTS[objId] = obj
        self.worldGrid[x][y].setPixmap(obj.pixmap)
                
    def moveObj(self, objId, direction):
        """
        Moves an object in the Virtual World
        @param objId : id of the object. See OBJECTS.keys() for a list
            of the available objects.
        @param direction
        """
        
        obj = self.OBJECTS[objId]
        
        if direction == 'izquierda':
            if obj.x > 0: 
                self.worldGrid[obj.y][obj.x].setPixmap(QPixmap())
                obj.x += -1 
                self.worldGrid[obj.y][obj.x].setPixmap(obj.pixmap)
            
        elif direction == 'derecha':
            if obj.x < self.NUM_COLUMNS - 1:
                self.worldGrid[obj.y][obj.x].setPixmap(QPixmap())
                obj.x += 1 
                self.worldGrid[obj.y][obj.x].setPixmap(obj.pixmap)
            
        elif direction == 'arriba':
            if obj.y > 0: 
                self.worldGrid[obj.y][obj.x].setPixmap(QPixmap())
                obj.y += -1
                self.worldGrid[obj.y][obj.x].setPixmap(obj.pixmap)
            
        elif direction == 'abajo':
            if obj.y < self.NUM_ROWS - 1: 
                self.worldGrid[obj.y][obj.x].setPixmap(QPixmap())
                obj.y += 1
                self.worldGrid[obj.y][obj.x].setPixmap(obj.pixmap)
        
        else:
            return "No se a que direccion moverme"
            
        return "{obj}: Me he movido hacia {direction}\n".format(
                obj = objId,
                direction = direction
            )
            
class WorldObject:
    
    def __init__(self, objType, x, y, imgWidth, imgHeight):
        """
        Creates an object of the virtual world 
        @param objType : The type of the object. See IMG_PATHS.keys()
            for a list of the available types.
        @param x, y : Coordenates of the object in the virtual world
        @param imgWidth, imgHeight: Width and Height of the object's icon
        """
        
        self.x = x
        self.y = y
        self.img = IMG_PATHS[objType]
        self.pixmap = QPixmap(self.img)
        self.resizePixmap(imgWidth, imgHeight)
        
    def resizePixmap(self, imgWidth, imgHeight):
    
        self.pixmap = self.pixmap.scaled(imgWidth, imgHeight, Qt.KeepAspectRatio)

if __name__ == '__main__':
    
    app = QApplication([])
    ventana = QMainWindow()
    mundo = VirtualWorld(ventana)
    ventana.setCentralWidget(mundo)
    
    ventana.resize(500, 600)
    ventana.setWindowTitle('Virtual World')
    ventana.show()

    screen = QDesktopWidget().screenGeometry()
    size = ventana.geometry()
    ventana.move((screen.width()-size.width())/2, 
        (screen.height()-size.height())/2)
    
    sys.exit(app.exec_())
