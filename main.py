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
import getopt
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

from Learning.LearningModels.ClassicModel import ClassicModel
from Learning.LearningModels.OneLevelModel import OneLevelModel
from Learning.LearningModels.FeedbackModel import FeedbackModel

from Learning.ModelParameters import Classic80
from Learning.ModelParameters import OneLevel90
from Learning.ModelParameters import Feedback81

dataSets = {
    'Total': (TotalTrainingSet, TotalTrainingSet),
    'Partial': (PartialTrainingSet, PartialTestSet),
    'Spanish': (SpanishTrainingSet, SpanishTestSet),
    'English': (EnglishTrainingSet, EnglishTestSet)
}
models = {
    'Classic': ClassicModel,
    'OneLevel': OneLevelModel,
    'Feedback': FeedbackModel
}
modelParams = {
    'Classic': Classic80,
    'OneLevel': OneLevel90,
    'Feedback': Feedback81
}

# Assign default values
setsName = 'Total'
enc = 'cce'
modelName = 'OneLevel'
iterations = 30

whether_gui = True
whether_tests = False
whether_save = False

def parse_parameters():
    global dataSets
    global models

    global setsName
    global enc
    global modelName
    global iterations
    global whether_gui
    global whether_tests
    global whether_save

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hd:e:m:i:ts",
            ["help", "dataset=", "encoder=", "model=", "iterations=", "no-gui",
                "tests", "save"]
        )
    except getopt.GetoptError, e:
        print('An error occurred reading command-line args: ', e)

    if len(opts) == 0:
        print('No arguments passed. Using defaults...')

    incorrect_args_str = "Incorrect value for {}. Use -h or --help to show allowed values"

    # Collect and validate command-line args
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print("""
HTM-TEUL Help:
  OPTIONS:
    -h | --help: To show this help
    -d | --dataset: Can be 'Total'*, 'Partial', 'Spanish' or 'English'
    -e | --encoder: Can be 'rle', 'tre' or 'cce'*
    -m | --model: Can be 'Classic', 'OneLevel'* or 'Feedback
    -i | --iterations: Number of times the training data will be passed to the
        model. Must be an integer (default=30).
    -t | --tests: Run the TestSuite.
    -s | --save: Save the trained model. Note that the resulting files can be 
heavy (around 50mb).
    --no-gui: Do not display gui

Test results and saved models will be stored in Reults/ folder.
*=default
""")
            sys.exit()
        elif opt in ("-d", "--dataset"):
            if arg in dataSets.keys():
               setsName = arg
            else:
                print(incorrect_args_str.format('dataset'))
                sys.exit(2)
        elif opt in ("-e", "--encoder"):
            if arg in ('rle', 'tre', 'cce'):
                enc = arg
            else:
                print(incorrect_args_str.format('encoder'))
                sys.exit(2)
        elif opt in ("-m", "--model"):
            if arg in models.keys():
               modelName = arg
            else:
                print(incorrect_args_str.format('model'))
                sys.exit(2)
        elif opt in ("-i", "--iterations"):
            if arg.isdigit():
               iterations = int(arg)
            else:
                print(incorrect_args_str.format('iterations'))
                sys.exit(2)
    opt_names = [opt for opt, arg in opts]
    whether_gui = not "--no-gui" in opt_names
    whether_tests = "-t" in opt_names or "--tests" in opt_names
    whether_save = "-s" in opt_names or "--save" in opt_names

if __name__ == '__main__':

    parse_parameters()

    currentSets = dataSets[setsName]
    CurrentModel = models[modelName]
    BestParameters = modelParams[modelName]

    trainingSet = currentSets[0]
    testSet = currentSets[1]

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
        BestParameters.bestFindings[0])
    modelName = model.__class__.__name__

    print(modelName)
    print(encoderName)
    model.train(iterations, maxTime=-1, verbosity=1)

    fileName = 'Results/'
    # Strips the 'Model' fron the name
    fileName += modelName[:-5] + setsName + '-'
    # Appends only the Capital letters
    fileName += ''.join(cap for cap in encoderName if cap.isupper())
    #fileName += 'OneRegionExp32'

    if whether_tests:
        TestSuite.testModel(model, testSet.trainingData,
            fileName=(fileName + '_Results'))

    if whether_save:
        print("Saving the model...")
        with open((fileName + '.pck'), 'wb') as modelFile:
            cPickle.dump(model, modelFile, -1)
        print("Done!")

    if whether_gui:
        app = QApplication([])
        window = MainWindow(model)
        sys.exit(app.exec_())
