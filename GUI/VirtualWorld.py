#!python2
#-*- coding: utf-8 -*-
#  VirtualWorld.py
#  Author: Larvasapiens <sebastian.narvaez@correounivalle.edu.co>
#  Created: 2015-10-22
#  Last Modification: 2015-10-22
#  Version: 1.1 [Stable]
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

"""
This code is partly based on ZetCode PyQt5 tutorial, by Jan Bodnar
website: zetcode.com 
"""

import sys, random
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication,\
    QLabel, QGridLayout
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QSize, QPoint
from PyQt5.QtGui import QPainter, QColor, QImage, QPixmap, QIcon

RESOURCES_PATH = 'Resources/'
IMG_PATHS = {
    'Ectatomma' : RESOURCES_PATH + 'Ectatomma.png',
    'Ectatomma-Hat-Hunter' : RESOURCES_PATH + 'Ectatomma-Hunter.png',
    'Ectatomma-Hat-Nurse' : RESOURCES_PATH + 'Ectatomma-Nurse.png',
    'Hat-Hunter' : RESOURCES_PATH + 'Hat-Hunter.png',
    'Hat-Nurse' : RESOURCES_PATH + 'Hat-Nurse.png'
}

class VirtualWorld(QFrame):
    
    def __init__(self, parent, numColumns=5, numRows=5):
    
        super(VirtualWorld, self).__init__(parent)
        
        self.numColumns = numColumns
        self.numRows = numRows
        
        self._objects = dict()
        self._objsCount = dict()
        self._totalObjs = 0
        
        self.initVirtualWorld()
        
    def initVirtualWorld(self):     
        
        self.worldGrid = []
        
        self.resize(500, 600)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setLineWidth(1)
        Cell.CELL_WIDTH = self.width() // self.numColumns
        Cell.CELL_HEIGHT = self.height() // self.numRows

        grid = QGridLayout()
        self.setLayout(grid)
        
        for row in xrange(self.numRows):
            self.worldGrid.append([])
            
            for column in xrange(self.numColumns):
                self.worldGrid[row].append(Cell(row, column))
                grid.addWidget(self.worldGrid[row][column], row, column)
        
        self.addObj('P1', 'Ectatomma', 3, 3)
        
    def addObj(self, objId, objType, x, y, imgWidth=None, imgHeight=None):
        """ Adds an object to the Virtual World """
        
        self._objects[objId] = WorldObject(objType, x, y)
        self.worldGrid[x][y].objectArrives(objId, self._objects[objId])
        
    def moveObj(self, objId, direction):
        """
        Moves an object in the Virtual World.
        
        @param objId: id of the object. See _objects.keys() for a list
            of the available _objects.
        @param direction: Can be 'izquierda', 'derecha', 'arriba' or
            'abajo'
        """
        
        obj = self._objects[objId]
        
        newX = obj.x
        newY = obj.y
        
        if direction == 'izquierda':
            if obj.x > 0: 
                newX += -1 
        
        elif direction == 'derecha':
            if obj.x < self.numColumns - 1:
                newX += 1 
        
        elif direction == 'arriba':
            if obj.y > 0: 
                newY += -1
            
        elif direction == 'abajo':
            if obj.y < self.numRows - 1: 
                newY += 1
        
        else:
            return '<font color="Orange">'\
                'No se a que direccion moverme'\
                '</font><br>'
        
        self.worldGrid[obj.y][obj.x].objectLeaves(objId)
        self.worldGrid[newY][newX].objectArrives(objId, obj)
        obj.x = newX
        obj.y = newY
        
        return '<font color="Green">'\
            '{obj}: Me he movido hacia {direction}'\
            '</font><br>'.format(
                obj = objId,
                direction = direction
            )
    
    def insertObj(self, objType):
        """
        Inserts an object in a random position of the Virtual World.
        
        @param objType
        """
        
        if self._totalObjs >= ((self.numColumns * self.numRows) - 1):
            return -1
        
        if objType not in self._objsCount:
            self._objsCount[objType] = 1
        
        objId = objType + str(self._objsCount[objType])
        validCoordinate = False
        
        while (not validCoordinate):
            objX = random.randint(0, self.numColumns - 1)
            objY = random.randint(0, self.numRows - 1)
            
            validCoordinate = (len(self.worldGrid[objX][objY].objects) == 0)
        
        self.addObj(objId, objType, objX, objY)
        self._totalObjs += 1
    
    def grabObj(self):
        """
        Make the P1 grab the object that is in the same cell it's in.
        """
        
        p1 = self._objects['P1']
        x = p1.x
        y = p1.y
        
        cell = self.worldGrid[y][x]
        cell.objectLeaves('P1')
        
        for objToGrabId in cell.objects.keys():
            p1.transform(p1.objType + '-' + cell.objects[objToGrabId].objType)
            cell.objectLeaves(objToGrabId)
        
        cell.objectArrives('P1', p1)
        
        return '<font color="Green">'\
            'P1: ¿Que tal me va?'\
            '</font><br>'

class WorldObject:
    
    def __init__(self, objType, x, y):
        """
        Creates an object of the virtual world.
        
        @param objType : The type of the object. See IMG_PATHS.keys()
            for a list of the available types.
        @param x, y : Coordenates of the object in the virtual world
        """
        
        self.x = x
        self.y = y
        self.objType = objType
        self.img = IMG_PATHS[objType]
        self.pixmap = QPixmap(self.img)
        #self.resizePixmap(imgWidth, imgHeight)
        
    def transform(self, objType):
        """
        Change the objType and consecuentially its image.
        """
    
        self.img = IMG_PATHS[objType]
        self.pixmap = QPixmap(self.img)

class Cell(QLabel):
    """
    A Cell is a square representing a coordinate in the Virtual World.
    It inherits from QLabel.
    """
    CELL_WIDTH = 0
    CELL_HEIGHT = 0
    
    def __init__(self, x, y):
        """
        @param x, y : Coordenates of the cell in the virtual world
        """
        
        super(Cell, self).__init__()
        
        self.objects = dict()
        self.x = x
        self.y = y
        
        self.setPixmap(QPixmap())
        self.setStyleSheet("QLabel { background-color : green }")
    
    def objectArrives(self, objId, obj):
        """
        The object is added to this cell's list of objects and is
        painted.
        
        @param objId
        @param obj
        """
        
        self.objects[objId] = obj
        self.paintObjects()
    
    def objectLeaves(self, objId):
        """
        The object is removed from the cell's list of objects and is
        unpainted.
        
        @param objId
        """
        
        self.objects.pop(objId)
        self.paintObjects()
    
    def paintObjects(self):
        """ Paints all the objects from this cell's list of objects. """
        
        pading = 9
        
        combined = QPixmap(Cell.CELL_WIDTH - pading , Cell.CELL_HEIGHT - pading)
        combined.fill(Qt.transparent)
        painter = QPainter(combined)
        
        for obj in self.objects.values():
            painter.drawPixmap(0, 0, obj.pixmap.scaled(Cell.CELL_WIDTH - pading,
                    Cell.CELL_HEIGHT - pading, Qt.KeepAspectRatio))
        
        painter.end()
        
        self.setPixmap(combined)

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
