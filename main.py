#!python2
#-*- coding: utf-8 -*-
#  main.py
#  Author: Larvasapiens <sebastian.narvaez@correounivalle.edu.co>
#  Created: 2015-11-04
#  Last Modified: 2015-12-01
#  Version: 1.2
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
from Utils import TestSuite
from PyQt5.QtWidgets import QApplication
from GUI.MainWindow import MainWindow
from Learning.EncoderFactory import *
from Utils.CustomCategoryEncoder import CustomCategoryEncoder

#from Learning.LearningModels.ClassicModel import ClassicModel
from Learning.LearningModels.FeedbackModel import FeedbackModel
#from Learning.LearningModels.JoinedInputsModel import JoinedInputsModel
#from Learning.LearningModels.OneLevelExpModel import OneLevelExpModel
#from Learning.LearningModels.OneLevelModel import OneLevelModel

#from Learning import MovementTrainingSet as _TS
from Learning import TotalTrainingSet as TTS

if __name__ == '__main__':
    _TS = TTS

    wordEncoder = CustomCategoryEncoder(
        11,
        list(_TS.categories[_TS.inputIdx['wordInput']]),
        nAdditionalCategorySlots=15,
        forced=True
    )
    actionEncoder = CustomCategoryEncoder(
        11,
        list(_TS.categories[_TS.inputIdx['actionInput']]),
        nAdditionalCategorySlots=15,
        forced=True
    )
    #wordEncoder = actionEncoder = UnifiedCategoryEncoder(_TS.categories,
    #    nAdditionalCategorySlots=15)
    #wordEncoder = actionEncoder = RandomizedLetterEncoder(600, 10)
    #wordEncoder = actionEncoder = TotallyRandomEncoder(50, 10)
    encoderName = wordEncoder.__class__.__name__
    
    #model = ClassicModel(wordEncoder, actionEncoder, _TS)
    #model = OneLevelModel(wordEncoder, actionEncoder, _TS)
    #model = OneLevelExpModel(wordEncoder, actionEncoder, _TS)
    model = FeedbackModel(wordEncoder, actionEncoder, _TS)
    #model = JoinedInputsModel(wordEncoder, actionEncoder, _TS)
    modelName = model.__class__.__name__
    
    print(modelName)
    print(encoderName)
    model.train(10, maxTime=-1, verbosity=1)

    #fileName = 'Results/'
    ## Strips the 'Model' fron the name
    #fileName += modelName[:-5] + '-'
    ## Appends only the Capital letters
    #fileName += ''.join(cap for cap in encoderName if cap.isupper())
    ##fileName += 'OneRegionExp32'

    #TestSuite.testModel(model, _TS.trainingData, fileName=(fileName + '_Results'))

    #print("Saving the model...")
    #with open((fileName + '.pck'), 'wb') as modelFile:
        #cPickle.dump(model, modelFile, -1)
    #print("Done!")

    app = QApplication([])
    window = MainWindow(model)
    app.exec_()
    #sys.exit(app.exec_())
