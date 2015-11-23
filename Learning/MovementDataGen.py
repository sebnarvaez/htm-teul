#  !python2
#  -*- coding: utf-8 -*-
#  MovementDataGen.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-11-22
#  Fecha última modificación: 2015-11-22
#  Versión: 0.1

import glob
import csv

"""
A standalone tool for generating the Movement data for all directions
from a single csv file
"""

outputFilePath = 'MovementTrainingSet.py'
INDENT = "    "

def addData(inputFilePath):

    print("Leyendo " + inputFilePath)
    with open(inputFilePath, 'rb') as inputFile,\
            open(outputFilePath, 'wb') as outputFile:
    
        outputFile.write('"""\n')
        outputFile.write('Automatically generated Training Data Set for the '\
            'Movement actions\n')
        outputFile.write('"""\n')
        outputFile.write('\n')
        outputFile.write('movementData = (\n')
        
        csvReader = csv.reader(inputFile)
        # Skip header rows
        csvReader.next()
        
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
        outputFile.write('\n)')
        
def writeDataUnit(columns, formatArgs, outputFile):

    outputFile.write(INDENT + '(')
    
    for element in columns:
        element = element.format(**formatArgs).split()
        outputFile.write(str(element) + ', ')
    
    outputFile.seek(-2, 2)
    outputFile.write('),\n')
    
if __name__ == '__main__':
    #addData('Dropbox/Tesis/htm-teul/Learning/Data/Movimiento.csv')
    addData('Data/Movimiento.csv')
    #for filePath in glob.glob('Data/*.csv'):
        #addData(filePath)
