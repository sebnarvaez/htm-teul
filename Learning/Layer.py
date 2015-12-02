#  !python2
#  -*- coding: utf-8 -*-
#  Layer.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-11-21
#  Fecha última modificación: 2015-11-22
#  Versión: 1.1

from __future__ import print_function

import numpy

class Layer():
    """A Layer contains a structure of Nupic modules and executes it."""

    def __init__(self, structure, modules, classifier):
        """
        @param structure: A dictionary containing the module names
            (keys), and their corresponding parent (values).
        @param modules: A dictionary containing the module names (keys)
            and their corresponding object (values). Note that there's
            no need to include Input modules here, since their values
            come from the training set.
        @param classifier
        
        Please use the following format for the moduleName(s):
        
        *TM : For a Temporal Memory Module
        *SP : For a Spatial Pooler Module
        *Enc : For an Encoder Module
        *Input: For an Input Module
        """
        self.structure  = structure
        self.modules    = modules
        self.classifier = classifier

    def applyStructure(self, value, inputName, verbosity=0, recordNum=0, 
            learn=True):
        """
        Applies the Layer structure to a value.

        @param value
        @param inputName: The name of the input module corresponding
            to the value.
        @param verbosity=0
        @param recordNum=0: The position of the current value in the
            sequence, starting from 0.
        @param learn=True: Whether to enable learning.
        
        @return A dictionary containing:
            'lastModType': The type of the last module executed (at the
                highest level of the structure)
            'lastOutput': The output produced by the last module.
            'lastBucketIdx': The bucketIdx from the last encoder used.
        """
        moduleName = self.structure[inputName]
        # prevOutput holds the last output that was generated.
        # It's uptdated each iteration.
        prevOutput = value 
        prevModName = ''
        bucketIdx = 0
        
        if verbosity > 1 :
            print("Value: " + str(value))
        
        while True:
            
            module = self.modules[moduleName]
            if verbosity > 1 :
                print("Current module: " + moduleName)
            
            if moduleName[-3:] == 'Enc':
                encodedValue = module.encode(prevOutput)
                bucketIdx = module.getBucketIndices(prevOutput)[0]
                
                prevOutput = encodedValue
                prevModName = moduleName
            
            elif moduleName[-2:] == 'SP':
                if prevModName[-2:] == 'TM':
                    spInput = numpy.zeros(module.getInputDimensions()[0],
                        dtype=numpy.uint8)
                    spInput[list(prevOutput)] = 1
                    prevOutput = spInput
                
                spOutput = numpy.zeros(module.getColumnDimensions(),
                    dtype=numpy.uint8)
                module.compute(prevOutput, learn, spOutput)
                
                prevOutput = spOutput
                prevModName = moduleName
                
            elif moduleName[-2:] == 'TM':
                if prevModName[-3:] == 'Enc' or prevModName[-2:] == 'SP':
                    prevOutput = sorted(numpy.where(spOutput > 0)[0].flat)
                
                module.compute(set(prevOutput), learn)
                
                if verbosity > 1 :
                
                    predictedColumns = module.mapCellsToColumns(
                        module.predictiveCells).keys()
                    print(moduleName + " columns prediction = " +
                        str(predictedColumns))

                prevOutput = module.activeCells
                prevModName = moduleName
            
            else:
                raise ValueError("Invalid Module Name. See the function's "\
                    "docstring to see the correct usage.")
            
            if verbosity > 1 :
                print(moduleName + " Output = " + str(prevOutput))
            
            if self.structure[moduleName] == None:
                return {
                    'lastModName' : prevModName,
                    'lastOutput' : prevOutput,
                    'lastBucketIdx' : bucketIdx
                }
                
            moduleName = self.structure[moduleName]
            
            
                
    def toPatterNZ(self, lastModName, lastModOutput):
        """ Correctly format the output of a module for the classifier """
        
        if (lastModName[-3:] == 'Enc') or (lastModName[-2:] == 'SP'):
            return numpy.where(lastModOutput > 0)[0]
        
        elif lastModName[-2:] == 'TM':
            module = self.modules[lastModName]
            return module.mapCellsToColumns(lastModOutput).keys()
        
        else:
            raise ValueError("Invalid Module Name. See the function's "\
                "docstring to see the correct usage.")

    def processInput(self, inputData, verbosity=0, learn=True):
        """
        Applies the Layer structure to an input.

        @param inputData: A list of tuples where the first element of
            each tuple is the name of the input module, and the second
            one is its corresponding sequence. Note that the order of
            the list is important.
        @param verbosity = 0
        @param learn = True: Whether to enable learning.
        """
        
        recordNum = 0
        retVal = None
        
        for inputModule in inputData:
            if verbosity > 0 : 
                print("===== " + inputModule[0] + ": " + str(inputModule[1]) +
                    " =====")
        
            for value in inputModule[1]:
                structureOutput = self.applyStructure(value, inputModule[0],
                    verbosity, recordNum, learn)
                patternNZ = self.toPatterNZ(structureOutput['lastModName'], 
                    structureOutput['lastOutput'])
                retVal = self.classifier.compute(
                        recordNum=recordNum,
                        patternNZ=patternNZ,
                        classification={
                            'bucketIdx': structureOutput['lastBucketIdx'], 
                            'actValue': value
                        },
                        learn=learn,
                        infer=True
                    )
                
                bestPredictions = []
            
                for step in retVal:
                    if step == 'actualValues':
                        continue
                    higherProbIndex = retVal[step].tolist().index(
                                    max(retVal[step].tolist()))
                    bestPredictions.append(
                        retVal['actualValues'][higherProbIndex]
                    )
                
                if verbosity > 0 :
                    print('Best Predictions: ' + str(bestPredictions))
                
                if verbosity > 1 :
                    print("  |  CLAClassifier best predictions for step1: ")
                    top = sorted(retVal[1].tolist(), reverse=True)[:3]
                    
                    for prob in top:
                        probIndex = retVal[1].tolist().index(prob)
                        print(str(retVal['actualValues'][probIndex]) +
                            " - " + str(prob))
                    
                    print("  |  CLAClassifier best predictions for step2: ")
                    top = sorted(retVal[2].tolist(), reverse=True)[:3]
                    
                    for prob in top:
                        probIndex = retVal[2].tolist().index(prob)
                        print(str(retVal['actualValues'][probIndex]) +
                            " - " + str(prob))
                    
                    print("")
                    print("---------------------------------------------------")
                    print("")
                
                recordNum += 1
                
        return bestPredictions
