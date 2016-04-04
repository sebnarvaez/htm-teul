#!python2
#-*- coding: utf-8 -*-
#  LoadModel.py
#  Author: Larvasapiens <sebastian.narvaez@correounivalle.edu.co>
#  Created: 2015-11-30
#  Last Modification: 2015-12-01
#  Versión: 1.1 [Stable]
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

import sys
import cPickle
import TestSuite
from PyQt5.QtWidgets import QApplication
from GUI.MainWindow import MainWindow
from Learning import MovementTrainingSet as MTS

if __name__ == '__main__':
    
    print("Loading the model...")
    
    filePath = 'Results/'
    
    #modelName = 'Classic'
    modelName = 'OneLevel'
    encoderName = '-UCE'
    #encoderName = '-RLE'
    #encoderName = '-TRE'
    
    fileName = filePath + modelName + encoderName
    
    with open(fileName + '.pck', 'rb') as modelFile:
        model = cPickle.load(modelFile)
    
    print("Done!")
    #model.train(MTS.trainingData, 5, verbose=0)
    
    #TestSuite.testModel(model, MTS.trainingData,
    #    fileName=(fileName + '_Results'))
    
    #app = QApplication([])
    #window = MainWindow(model)
    #app.exec_()
    #sys.exit(app.exec_())
