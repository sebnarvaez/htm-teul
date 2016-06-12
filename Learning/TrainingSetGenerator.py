#!python2
#-*- coding: utf-8 -*-
#  MovementDataGen.py
#  Author: Larvasapiens <sebastian.narvaez@correounivalle.edu.co>
#  Created: 2015-11-22
#  Last Modified: 2015-11-26
#  Version: 1.0 [Stable]
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

import csv
import random

"""
A standalone tool for generating the Movement data for all directions
from a single csv file
"""

INDENT = "    "
#outputFilePath = 'MovementTrainingSet.py'
categories = []
inputIdx = {}


def addEnglMovementData(inputFilePaths, outputFile, probability=1.0,
        altOutputFile=None):
    """
    @param inputFilePaths: A list of paths of the files where the data
        will be formatted and stored from.
    @param outputFile
    """
    global categories
    global inputIdx

    for inputFilePath in inputFilePaths:
        with open(inputFilePath, 'rb') as inputFile:
            csvReader = csv.reader(inputFile)
            headers = csvReader.next()

            # Assumes all files have the same columns
            if len(inputIdx) == 0:
                for index, inputName in enumerate(headers):
                    inputIdx[inputName] = index
            # categories will hold the different data from each column
            if len(categories) == 0:
                categories = [set() for _ in xrange(len(headers))]

            for row in csvReader:
                for preposition in ('to', 'towards'):
                    formatArgs = {
                        'direction': preposition + 'the left',
                        'argumento': 'derecha'
                    }
                    writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

                    formatArgs = {
                        'direction': preposition + 'the east',
                        'argumento': 'derecha'
                    }
                    writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

                    formatArgs = {
                        'direction': preposition + 'the right',
                        'argumento': 'izquierda'
                    }
                    writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

                    formatArgs = {
                        'direction': preposition + 'the west',
                        'argumento': 'izquierda'
                    }
                    writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

                    if not preposition == 'towards':
                        formatArgs = {
                            'direction': preposition + 'upwards',
                            'argumento': 'arriba'
                        }
                        writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

                    formatArgs = {
                        'direction': preposition + 'the north',
                        'argumento': 'arriba'
                    }
                    writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

                    if not preposition == 'towards':
                        formatArgs = {
                            'direction': preposition + 'downwards',
                            'argumento': 'abajo'
                        }
                    writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

                    formatArgs = {
                        'direction': preposition + 'the south',
                        'argumento': 'abajo'
                    }
                    writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

def addMovementData(inputFilePaths, outputFile, probability=1.0,
        altOutputFile=None):
    """
    @param inputFilePaths: A list of paths of the files where the data
        will be formatted and stored from.
    @param outputFile
    """
    global categories
    global inputIdx

    for inputFilePath in inputFilePaths:
        with open(inputFilePath, 'rb') as inputFile:
            csvReader = csv.reader(inputFile)
            headers = csvReader.next()

            # Assumes all files have the same columns
            if len(inputIdx) == 0:
                for index, inputName in enumerate(headers):
                    inputIdx[inputName] = index
            # categories will hold the different data from each column
            if len(categories) == 0:
                categories = [set() for _ in xrange(len(headers))]

            for row in csvReader:
                for preposition in ('a', 'hacia', 'para'):
                    formatArgs = {
                        'direccion': preposition + 'la derecha',
                        'argumento': 'derecha'
                    }
                    writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

                    formatArgs = {
                        'direccion': preposition + 'el este',
                        'argumento': 'derecha'
                    }
                    writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

                    formatArgs = {
                        'direccion': preposition + 'la izquierda',
                        'argumento': 'izquierda'
                    }
                    writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

                    formatArgs = {
                        'direccion': preposition + 'el oeste',
                        'argumento': 'izquierda'
                    }
                    writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

                    formatArgs = {
                        'direccion': preposition + 'arriba',
                        'argumento': 'arriba'
                    }
                    writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

                    formatArgs = {
                        'direccion': preposition + 'el norte',
                        'argumento': 'arriba'
                    }
                    writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

                    formatArgs = {
                        'direccion': preposition + 'abajo',
                        'argumento': 'abajo'
                    }
                    writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

                    formatArgs = {
                        'direccion': preposition + 'el sur',
                        'argumento': 'abajo'
                    }
                    writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)


def addEnglPickData(inputFilePaths, outputFile, probability=1.0,
        altOutputFile=None):
    """
    @param inputFilePaths: A list of paths of the files where the data
        will be formatted and stored from.
    @param outputFile
    """
    global categories
    global inputIdx

    for inputFilePath in inputFilePaths:
        with open(inputFilePath, 'rb') as inputFile:
            csvReader = csv.reader(inputFile)
            headers = csvReader.next()

            # Assumes all files have the same columns
            if len(inputIdx) == 0:
                for index, inputName in enumerate(headers):
                    inputIdx[inputName] = index
            # categories will hold the different data from each column
            if len(categories) == 0:
                categories = [set() for _ in xrange(len(headers))]

            for row in csvReader:

                for please in ('', 'please'):
                    formatArgs = {
                        'please': please,
                        'object': 'the hat',
                    }
                    writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

                    formatArgs = {
                        'please': please,
                        'object': 'that object',
                    }
                    writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

                    formatArgs = {
                        'please': please,
                        'object': 'that thingy',
                    }
                    writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)


def addPickData(inputFilePaths, outputFile, probability=1.0,
        altOutputFile=None):
    """
    @param inputFilePaths: A list of paths of the files where the data
        will be formatted and stored from.
    @param outputFile
    """
    global categories
    global inputIdx

    for inputFilePath in inputFilePaths:
        with open(inputFilePath, 'rb') as inputFile:
            csvReader = csv.reader(inputFile)
            headers = csvReader.next()

            # Assumes all files have the same columns
            if len(inputIdx) == 0:
                for index, inputName in enumerate(headers):
                    inputIdx[inputName] = index
            # categories will hold the different data from each column
            if len(categories) == 0:
                categories = [set() for _ in xrange(len(headers))]

            for row in csvReader:

                for favor1 in ('', 'por favor'):
                    for favor2 in ('', 'por favor'):
                        formatArgs = {
                            'favor-opc1': favor1,
                            'objeto': 'el sombrero',
                            'favor-opc2': favor2
                        }
                        writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

                        formatArgs = {
                            'favor-opc1': favor1,
                            'objeto': 'la cachucha',
                            'favor-opc2': favor2
                        }
                        writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

                        formatArgs = {
                            'favor-opc1': favor1,
                            'objeto': 'el objeto',
                            'favor-opc2': favor2
                        }
                        writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

                        formatArgs = {
                            'favor-opc1': favor1,
                            'objeto': 'lo que esta ahi',
                            'favor-opc2': favor2
                        }
                        writeDataUnit(row, formatArgs, outputFile, probability, altOutputFile)

def addDanceData(inputFilePaths, outputFile, probability=1.0,
        altOutputFile=None):
    """
    @param inputFilePaths: A list of paths of the files where the data
        will be formatted and stored from.
    @param outputFile
    """
    global categories
    global inputIdx

    for inputFilePath in inputFilePaths:
        with open(inputFilePath, 'rb') as inputFile:
            csvReader = csv.reader(inputFile)
            headers = csvReader.next()

            # Assumes all files have the same columns
            if len(inputIdx) == 0:
                for index, inputName in enumerate(headers):
                    inputIdx[inputName] = index
            # categories will hold the different data from each column
            if len(categories) == 0:
                categories = [set() for _ in xrange(len(headers))]

            for row in csvReader:
                writeDataUnit(row, {}, outputFile, probability, altOutputFile)


def writeDataUnit(columns, formatArgs, outputFile, probability=1.0,
        altOutputFile=None):
    """
    Writes a data unit with certain probability so to induce
    incompleteness in the training data. Data not written in
    outputFile is written to altOutputFile.
    """
    choosenFile = outputFile

    if probability < 1.0:
        choice = random.random()

        if choice > probability:
            choosenFile = altOutputFile

    choosenFile.write(INDENT + '(')
    global categories

    for columnIdx, dataUnit in enumerate(columns):
        dataUnit = dataUnit.format(**formatArgs).split()
        choosenFile.write(str(dataUnit) + ', ')
        categories[columnIdx].update(dataUnit)

    choosenFile.seek(-2, 2)
    choosenFile.write('),\n')

if __name__ == '__main__':
    altOutputFilePath = 'SpanishTestSet.py'
    outputFilePath = 'Spanish.py'

    with open(outputFilePath, 'wb') as outputFile, \
            open(altOutputFilePath, 'wb') as altOutputFile:
        probability = 0.8

        outputFile.write('"""\n')
        outputFile.write('Automatically generated Training Data Set\n')
        outputFile.write('"""\n')
        outputFile.write('\n')
        outputFile.write('trainingData = (\n')

        altOutputFile.write('"""\n')
        altOutputFile.write('Automatically generated Test Data Set\n')
        altOutputFile.write('"""\n')
        altOutputFile.write('\n')
        altOutputFile.write('trainingData = (\n')

        addMovementData(
            [
                'Data/MovimientoEspanol.csv'
            ],
            outputFile,
            probability=probability,
            altOutputFile=altOutputFile
        )

        #addEnglMovementData(
        #    [
        #        'Data/MovimientoEnglish.csv'
        #    ],
        #    outputFile,
        #    probability=probability,
        #    altOutputFile=altOutputFile
        #)

        addDanceData(
            [
                'Data/DanzaEspanol.csv'
            ],
            outputFile,
            probability=probability,
            altOutputFile=altOutputFile
        )

        #addDanceData(
        #    [
        #        'Data/DanzaEnglish.csv'
        #    ],
        #    outputFile,
        #    probability=probability,
        #    altOutputFile=altOutputFile
        #)

        addPickData(
            [
                'Data/RecogerEspanol.csv'
            ],
            outputFile,
            probability=probability,
            altOutputFile=altOutputFile
        )

        #addEnglPickData(
        #    [
        #        'Data/RecogerEnglish.csv'
        #    ],
        #    outputFile,
        #    probability=probability,
        #    altOutputFile=altOutputFile
        #)

        outputFile.write('\n)\n')
        outputFile.write('inputIdx = {0}\n'.format(inputIdx))
        outputFile.write('categories = {0}'.format(categories))

        altOutputFile.write('\n)\n')
        altOutputFile.write('inputIdx = {0}\n'.format(inputIdx))
        altOutputFile.write('categories = {0}'.format(categories))

        print("Data was written to {0} and {1}.".format(outputFilePath, 
            altOutputFilePath))
#        for filePath in glob.glob('Data/*.csv'):
#            addData(filePath)
