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

"""
A standalone tool for generating the Movement data for all directions
from a single csv file
"""

INDENT = "    "
#outputFilePath = 'MovementTrainingSet.py'
outputFilePath = 'TotalTrainingSet.py'
categories = []
inputIdx = {}

def addMovementData(inputFilePaths, outputFile):
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

                formatArgs = {
                    'direccion': 'la derecha',
                    'argumento': 'derecha'
                }
                writeDataUnit(row, formatArgs, outputFile)

                formatArgs = {
                    'direccion': 'el este',
                    'argumento': 'derecha'
                }
                writeDataUnit(row, formatArgs, outputFile)

                formatArgs = {
                    'direccion': 'la izquierda',
                    'argumento': 'izquierda'
                }
                writeDataUnit(row, formatArgs, outputFile)

                formatArgs = {
                    'direccion': 'el oeste',
                    'argumento': 'izquierda'
                }
                writeDataUnit(row, formatArgs, outputFile)

                formatArgs = {
                    'direccion': 'arriba',
                    'argumento': 'arriba'
                }
                writeDataUnit(row, formatArgs, outputFile)

                formatArgs = {
                    'direccion': 'el norte',
                    'argumento': 'arriba'
                }
                writeDataUnit(row, formatArgs, outputFile)

                formatArgs = {
                    'direccion': 'abajo',
                    'argumento': 'abajo'
                }
                writeDataUnit(row, formatArgs, outputFile)

                formatArgs = {
                    'direccion': 'el sur',
                    'argumento': 'abajo'
                }
                writeDataUnit(row, formatArgs, outputFile)

def addPickData(inputFilePaths, outputFile):
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

                formatArgs = {
                    'favor-opc1': '',
                    'objeto': 'el sombrero',
                    'favor-opc2': ''
                }
                writeDataUnit(row, formatArgs, outputFile)

                formatArgs = {
                    'favor-opc1': 'por favor',
                    'objeto': 'el sombrero',
                    'favor-opc2': ''
                }
                writeDataUnit(row, formatArgs, outputFile)

                formatArgs = {
                    'favor-opc1': '',
                    'objeto': 'el sombrero',
                    'favor-opc2': 'por favor'
                }
                writeDataUnit(row, formatArgs, outputFile)

                formatArgs = {
                    'favor-opc1': '',
                    'objeto': 'el objeto',
                    'favor-opc2': ''
                }
                writeDataUnit(row, formatArgs, outputFile)

                formatArgs = {
                    'favor-opc1': 'por favor',
                    'objeto': 'el objeto',
                    'favor-opc2': ''
                }
                writeDataUnit(row, formatArgs, outputFile)

                formatArgs = {
                    'favor-opc1': '',
                    'objeto': 'el objeto',
                    'favor-opc2': 'por favor'
                }
                writeDataUnit(row, formatArgs, outputFile)

                formatArgs = {
                    'favor-opc1': '',
                    'objeto': 'la cachucha',
                    'favor-opc2': ''
                }
                writeDataUnit(row, formatArgs, outputFile)
                formatArgs = {
                    'favor-opc1': 'por favor',
                    'objeto': 'la cachucha',
                    'favor-opc2': ''
                }
                writeDataUnit(row, formatArgs, outputFile)
                formatArgs = {
                    'favor-opc1': '',
                    'objeto': 'la cachucha',
                    'favor-opc2': 'por favor'
                }
                writeDataUnit(row, formatArgs, outputFile)

                formatArgs = {
                    'favor-opc1': '',
                    'objeto': 'lo que esta ahi',
                    'favor-opc2': ''
                }
                writeDataUnit(row, formatArgs, outputFile)

                formatArgs = {
                    'favor-opc1': 'por favor',
                    'objeto': 'lo que esta ahi',
                    'favor-opc2': ''
                }
                writeDataUnit(row, formatArgs, outputFile)

                formatArgs = {
                    'favor-opc1': '',
                    'objeto': 'lo que esta ahi',
                    'favor-opc2': 'por favor'
                }
                writeDataUnit(row, formatArgs, outputFile)

def addDanceData(inputFilePaths, outputFile):
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
                writeDataUnit(row, {}, outputFile)

def writeDataUnit(columns, formatArgs, outputFile):

    outputFile.write(INDENT + '(')
    global categories

    for columnIdx, dataUnit in enumerate(columns):
        dataUnit = dataUnit.format(**formatArgs).split()
        outputFile.write(str(dataUnit) + ', ')
        categories[columnIdx].update(dataUnit)


    outputFile.seek(-2, 2)
    outputFile.write('),\n')

if __name__ == '__main__':
    #addData('Dropbox/Tesis/htm-teul/Learning/Data/Movimiento.csv')
    with open(outputFilePath, 'wb') as outputFile:
        outputFile.write('"""\n')
        outputFile.write('Automatically generated Training Data Set\n')
        outputFile.write('"""\n')
        outputFile.write('\n')
        outputFile.write('trainingData = (\n')

        addMovementData(
            [
                'Data/MovimientoPerfecto.csv'#,
                #'Data/MovimientoImperfectoReordenado2.csv'
            ],
            outputFile
        )
        addDanceData(
            [
                'Data/DanzaPerfecto.csv'
            ],
            outputFile
        )
        addPickData(
            [
                'Data/RecogerPerfecto.csv'
            ],
            outputFile
        )

        outputFile.write('\n)\n')
        outputFile.write('inputIdx = {0}\n'.format(inputIdx))
        outputFile.write('categories = {0}'.format(categories))

        print("Data was written to {0}.".format(outputFilePath))
        #for filePath in glob.glob('Data/*.csv'):
            #addData(filePath)
