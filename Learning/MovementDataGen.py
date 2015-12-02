#  !python2
#  -*- coding: utf-8 -*-
#  MovementDataGen.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-11-22
#  Fecha última modificación: 2015-11-26
#  Versión: 1.0 [Stable]

import glob
import csv

"""
A standalone tool for generating the Movement data for all directions
from a single csv file
"""

INDENT = "    "
outputFilePath = 'MovementTrainingSet.py'
categories = None

def addData(inputFilePath, mode='wb'):
    """
    @param inputFilePath: The path of the file where the data will be
        formatted and stored from.
    @param mode='wb': The mode in which the file will be opened.
        Recommended arguments:
            'wb': Overwrites the data. 
            'ab': Appends the data at the end of the file.
    """

    print("Leyendo " + inputFilePath)
    with open(inputFilePath, 'rb') as inputFile,\
            open(outputFilePath, mode) as outputFile:
    
        outputFile.write('"""\n')
        outputFile.write('Automatically generated Training Data Set for the '\
            'Movement actions\n')
        outputFile.write('"""\n')
        outputFile.write('\n')
        outputFile.write('trainingData = (\n')
        
        csvReader = csv.reader(inputFile)
        # categories will hold the different data from each column
        global categories
        headers = csvReader.next()
        
        categories = [set() for _ in xrange(len(headers))]
        inputIdx = {}
        
        for index, inputName in enumerate(headers):
            inputIdx[inputName] = index
        
        for row in csvReader:
            
            formatArgs = {
                'direccion' : 'la derecha',
                'cardinal' : 'este',
                'argumento' : 'derecha'
            }
            writeDataUnit(row, formatArgs, outputFile)
            
            formatArgs = {
                'direccion' : 'la izquierda',
                'cardinal' : 'oeste',
                'argumento' : 'izquierda'
            }
            writeDataUnit(row, formatArgs, outputFile)
            
            formatArgs = {
                'direccion' : 'arriba',
                'cardinal' : 'norte',
                'argumento' : 'arriba'
            }
            writeDataUnit(row, formatArgs, outputFile)
            
            formatArgs = {
                'direccion' : 'abajo',
                'cardinal' : 'sur',
                'argumento' : 'abajo'
            }
            writeDataUnit(row, formatArgs, outputFile)
        
        outputFile.seek(-2, 2)
        outputFile.write('\n)\n')
        outputFile.write('inputIdx = {0}\n'.format(inputIdx))
        outputFile.write('categories = {0}'.format(categories))
        
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
    addData('Data/Movimiento2.csv', 'wb')
    #for filePath in glob.glob('Data/*.csv'):
        #addData(filePath)
