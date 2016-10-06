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

from Learning import TotalTrainingSet
from Learning import PartialTrainingSet
from Learning import PartialTestSet
from Learning import SpanishTrainingSet
from Learning import SpanishTestSet
from Learning import EnglishTrainingSet
from Learning import EnglishTestSet

from Learning.LearningModels.FeedbackModel import FeedbackModel as CurrentModel
import Learning.ModelParameters.Feedback81 as BestResults

if __name__ == '__main__':
    for currentSets in ((TotalTrainingSet, TotalTrainingSet, 'Total'),
                        (PartialTrainingSet, PartialTestSet, 'Partial'),
                        (SpanishTrainingSet, SpanishTestSet, 'Spanish'),
                        (EnglishTrainingSet, EnglishTestSet, 'English')):
        trainingSet = currentSets[0]
        testSet = currentSets[1]
        setsName = currentSets[2]

        for enc in ('rle', 'tre', 'cce'):

            if enc == 'rle':
                abcLength = 26
                bitsPerLetter = 3
                maxWordLength = 20
                randomBits = bitsPerLetter * maxWordLength

                # Mantain sparsity of 10%  in the random bits
                rleWidth = (abcLength * bitsPerLetter * maxWordLength) +\
                        (randomBits * 10)
                wordEncoder = actionEncoder = RandomizedLetterEncoder(rleWidth,
                    randomBits, bitsPerLetter)

            elif enc == 'tre':
                wordEncoder = actionEncoder = TotallyRandomEncoder(1024, 204)

            elif enc == 'cce':
                wordEncoder = CustomCategoryEncoder(
                    21,
                    list(trainingSet.categories[
                            trainingSet.inputIdx['wordInput']
                        ]),
                    nAdditionalCategorySlots=15,
                )
                actionEncoder = CustomCategoryEncoder(
                    21,
                    list(trainingSet.categories[
                            trainingSet.inputIdx['actionInput']
                        ]),
                    nAdditionalCategorySlots=15,
                )

            encoderName = wordEncoder.__class__.__name__

            model = CurrentModel(wordEncoder, actionEncoder, trainingSet,
                BestResults.bestFindings[0])
            modelName = model.__class__.__name__

            print(modelName)
            print(encoderName)
            model.train(30, maxTime=-1, verbosity=1)

            fileName = 'Results/'
            # Strips the 'Model' fron the name
            fileName += modelName[:-5] + setsName + '-'
            # Appends only the Capital letters
            fileName += ''.join(cap for cap in encoderName if cap.isupper())
            #fileName += 'OneRegionExp32'

            TestSuite.testModel(model, testSet.trainingData,
                fileName=(fileName + '_Results'))

            #print("Saving the model...")
            #with open((fileName + '.pck'), 'wb') as modelFile:
            #    cPickle.dump(model, modelFile, -1)
            #print("Done!")

            #app = QApplication([])
            #window = MainWindow(model)
            #app.exec_()
            #sys.exit(app.exec_())
