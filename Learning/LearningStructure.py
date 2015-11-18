#!python2
#-*- coding: utf-8 -*-
#  LearningStructure.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-09-30
#  Fecha última modificación: 2015-10-27
#  Versión: 1.01

"""
 Encodings:
   Word & Action-> Category
 Structure:
   WordCategory -> WordsSP -> SentencesTM
   ActionCategory -> ActionsSP -> ActionsSeqTM
       SentencesTM + ActionsSeqTM -> generalTM
"""
import numpy

from LearningStructureFactory import *
from TrainingData import trainingData

from nupic.encoders.category import CategoryEncoder
from nupic.algorithms.CLAClassifier import CLAClassifier
from nupic.encoders.scalar import ScalarEncoder
from nupic.research.spatial_pooler import SpatialPooler
from nupic.research.temporal_memory import TemporalMemory

class Layer():
    
    """ Layer opera con los Spatial Pooler y Temporal Memories """
    
    def __init__(self, wordEncoder, actionEncoder, wordSP, wordTM, actionSP, 
                 actionTM, generalSP, generalTM, classifier):
        
        self.wordEncoder = wordEncoder
        self.actionEncoder = actionEncoder
        self.wordSP = wordSP
        self.wordTM = wordTM
        self.actionSP = actionSP
        self.actionTM = actionTM
        self.generalSP = generalSP
        self.generalTM = generalTM
        self.classifier = classifier
    
    def inputSentence(self, sentence, actionSeq, verbosity, learn = True):
        """ Procesar las secuencias en la estructura """
        
        if verbosity > 0 : print "===== " + str(sentence) + " - " + str(actionSeq) + " ====="
        #wordTMActiveCells = []
        #actionTMActiveCells = []
        recordNum = 0
        retVal = None
        
        for word in sentence:
            output = numpy.zeros(self.wordSP.getColumnDimensions())
            
            # Input through encoder
            if verbosity > 1 : print "Word Input = " + str(word)
            encoding = self.wordEncoder.encode(word)
            bucketIdx = self.wordEncoder.getBucketIndices(word)[0]
            
            # Input through wordSPatial pooler
            self.wordSP.compute(encoding, learn, output)
            if verbosity > 1 : print "SpatialPooler Output = " + str(numpy.where(output > 0)[0])
            
            # Input through temporal memory
            input = set(sorted(numpy.where(output > 0)[0].flat))
            self.wordTM.compute(input, learn)  
            #wordTMActiveCells.append(self.wordTM.activeCells)
            
            # Input trough the general TM
            self.generalTM.compute(self.wordTM.activeCells, learn)
            predictedColumns = self.generalTM.mapCellsToColumns(self.generalTM.predictiveCells).keys()
            
            if verbosity > 1 :
                predictedColumns = self.wordTM.mapCellsToColumns(self.wordTM.predictiveCells).keys()
                print "WordTM Prediction = " + str(predictedColumns)
                predictedValues = ""
                connected = numpy.zeros(self.wordSP.getNumInputs(), dtype="int")
                for prediction in predictedColumns:
                    self.wordSP.getConnectedSynapses(prediction, connected)
                    predictedValues += str(self.wordEncoder.decode(connected)) + "\n"
                print "Predicted values = " + str(predictedValues)
            if verbosity > 2 :
                activeCellsStr = ""
                columns = self.wordTM.mapCellsToColumns(self.wordTM.activeCells)
                for column in columns:
                    connected = numpy.zeros(self.wordSP.getNumInputs(), dtype="int")
                    self.wordSP.getConnectedSynapses(column, connected)
                    activeCellsStr += str(self.wordEncoder.decode(connected)) + '\n'
                print "Active cells = " + str(self.wordTM.activeCells)
                print "Active values = " + activeCellsStr
            # Input into classifier
            patternNZ = self.generalTM.mapCellsToColumns(self.generalTM.activeCells).keys()
            print(patternNZ)
            retVal = self.classifier.compute (
                recordNum = recordNum,
                #patternNZ = predictedColumns,
                patternNZ = patternNZ,
                classification = {'bucketIdx': bucketIdx, 'actValue': word},
                learn = learn,
                infer = True
            )
            #print(retVal)
            recordNum += 1
        #Print predictions from the general TM
        #predictedCells1 = generalTM.mapCellsToColumns(generalTM.predictiveCells).keys()
        #predictedCells2 = generalTM.mapCellsToColumns(
        #generalTM.computePredictiveCells(predictedCells1, generalTM.connections).keys()
        #print "Predicted values = ",
        #predictedColumns = actionTM.mapCellsToColumns(predictedCells).keys()
        #for prediction in predictedColumns:
            #connected = numpy.zeros(actionSP.getNumInputs(), dtype="int")
            #actionSP.getConnectedSynapses(prediction, connected)
            #print actionEncoder.decode(connected)
        bestPredictions = []
        for step in retVal:
            if step == 'actualValues': continue
            bestPredictions.append(retVal['actualValues'][retVal[step].tolist().index(max(retVal[step].tolist()))])
        
        if verbosity > 0 :
            #print "  |  CLAClassifier 1 step prob = " + str(retVal[1])
            #print "  |  CLAClassifier 2 step prob = " + str(retVal[2])
            #print "  |  CLAClassifier actual val. = " + str(retVal['actualValues']) 
            #print ""
            print 'Best Predictions: ' + str(bestPredictions)
            print "  |  CLAClassifier best predictions for step1: "
            top = sorted(retVal[1].tolist(), reverse = True)[:3]
            for prob in top:
                print str(retVal['actualValues'][retVal[1].tolist().index(prob)]) +\
                    " - " + str(prob)
            print "  |  CLAClassifier best predictions for step2: "
            top = sorted(retVal[2].tolist(), reverse = True)[:3]
            for prob in top:
                print str(retVal['actualValues'][retVal[2].tolist().index(prob)]) +\
                    " - " + str(prob)
            print ""
            print "--------------------------------------------------------"
            print ""
        
        if verbosity > 1 : print "\n### Pasando a Action ###\n"
        
        for action in actionSeq:
            output = numpy.zeros(self.actionSP._columnDimensions)
            
            # Input through encoder
            if verbosity > 1 : print "Action Input = " + str(action)
            encoding = self.actionEncoder.encode(action)
            bucketIdx = self.actionEncoder.getBucketIndices(action)[0]
            
            # Input through wordSPatial pooler
            self.actionSP.compute(encoding, learn, output)
            if verbosity > 1 : print "SpatialPooler Output = " + str(numpy.where(output > 0)[0])
            
            # Input through temporal memory
            input = set(sorted(numpy.where(output > 0)[0].flat))
            self.actionTM.compute(input, learn)
            #actionTMActiveCells.append(self.actionTM.activeCells)
            
            # Input trough the general TM
            self.generalTM.compute(self.actionTM.activeCells, learn)
            predictedColumns = self.generalTM.mapCellsToColumns(self.generalTM.predictiveCells).keys()
            
            if verbosity > 1 :
                predictedColumns = self.actionTM.mapCellsToColumns(self.actionTM.predictiveCells).keys()
                print "TemporalMemory Prediction = " + str(predictedColumns)
                predictedValues = ""
                connected = numpy.zeros(self.actionSP.getNumInputs(), dtype="int")
                for prediction in predictedColumns:
                    self.actionSP.getConnectedSynapses(prediction, connected)
                    predictedValues += str(self.actionEncoder.decode(connected)) + "\n"
                print "Predicted values = " + str(predictedValues)
                print ""
            if verbosity > 2 :
                activeCellsStr = ""
                for cell in self.actionTM.activeCells:
                    connected = numpy.zeros(self.actionSP.getNumInputs(), dtype="int")
                    self.actionSP.getConnectedSynapses((cell / self.actionTM.cellsPerColumn), connected)
                    activeCellsStr += str(self.actionEncoder.decode(connected)) + '\n'
                print "Active cells = " + str(self.actionTM.activeCells)
                print "Active values = " + activeCellsStr
            # Input into classifier
            retVal = self.classifier.compute(recordNum = recordNum,
                patternNZ = predictedColumns,
                classification= {'bucketIdx': bucketIdx, 'actValue': action},
                learn = learn,
                infer = False
            )
            recordNum += 1        
        return bestPredictions

class LearningStructure():
    
    words = []
    actions = []
    
    def __init__(self):
        self.extractCategories(trainingData)
        self.encoder = CategoryEncoder(w = 5, categoryList = self.words + self.actions, forced = True)
        self.wordEncoder = self.actionEncoder = self.encoder
        #self.wordEncoder = CategoryEncoder(w = 5, categoryList = words, forced = True)
        #self.actionEncoder = CategoryEncoder(w = 5, categoryList = actions, forced = True)
        
        self.wordSP = SpatialPooler(
            inputDimensions = (self.wordEncoder.getWidth()),
            columnDimensions = (self.wordEncoder.ncategories * 3),
            potentialRadius = 12,
            potentialPct = 0.5,
            globalInhibition = True,
            localAreaDensity = -1.0,
            numActiveColumnsPerInhArea = 5.0,
            stimulusThreshold = 0,
            synPermInactiveDec = 0.1,
            synPermActiveInc = 0.1,
            synPermConnected = 0.1,
            minPctOverlapDutyCycle = 0.1,
            minPctActiveDutyCycle = 0.1,
            dutyCyclePeriod = 10, 
            maxBoost = 3,
            seed = 42,
            spVerbosity = 0
        )
        
        self.wordTM = TemporalMemory(
            columnDimensions = (self.wordEncoder.ncategories * 3,),
            initialPermanence = 0.4,
            connectedPermanence = 0.5,
            minThreshold = 4,
            maxNewSynapseCount = 4,
            permanenceDecrement = 0.05,
            permanenceIncrement = 0.05,
            activationThreshold = 4
        )
        
        self.actionSP = SpatialPooler(
            inputDimensions = self.actionEncoder.getWidth(),
            columnDimensions = (self.actionEncoder.ncategories * 3),
            potentialRadius = 12,
            potentialPct = 0.5,
            globalInhibition = True,
            localAreaDensity = -1.0,
            numActiveColumnsPerInhArea = 5.0,
            stimulusThreshold = 0,
            synPermInactiveDec = 0.1,
            synPermActiveInc = 0.1,
            synPermConnected = 0.1,
            minPctOverlapDutyCycle = 0.1,
            minPctActiveDutyCycle = 0.1,
            dutyCyclePeriod = 10, 
            maxBoost = 3,
            seed = 42,
            spVerbosity = 0
        )
        
        self.actionTM = TemporalMemory(
            columnDimensions = (self.actionEncoder.ncategories * 3,),
            initialPermanence = 0.4,
            connectedPermanence = 0.5,
            minThreshold = 4,
            maxNewSynapseCount = 4,
            permanenceDecrement = 0.05,
            permanenceIncrement = 0.05,
            activationThreshold = 4
        )
        
        generalInputDim = self.wordTM.numberOfCells() + self.actionTM.numberOfCells()
        
        generalEncoder = ScalarEncoder(
            w = 21,
            minval = 0,
            maxval = self.wordTM.numberOfCells(),
            radius = 32,
            clipInput = True
        )
        
        self.generalSP = SpatialPooler(
            inputDimensions = generalEncoder.getWidth(),
            columnDimensions = (len(trainingData) * 3),
            potentialRadius = 28,
            potentialPct = 0.5,
            globalInhibition = True,
            localAreaDensity = -1.0,
            numActiveColumnsPerInhArea = 5.0,
            stimulusThreshold = 0,
            synPermInactiveDec = 0.1,
            synPermActiveInc = 0.1,
            synPermConnected = 0.1,
            minPctOverlapDutyCycle = 0.1,
            minPctActiveDutyCycle = 0.1,
            dutyCyclePeriod = 10, 
            maxBoost = 3,
            seed = 42,
            spVerbosity = 0
        ) 
        
        self.generalTM = TemporalMemory(
            columnDimensions = (max(self.wordTM.numberOfCells(), self.actionTM.numberOfCells()),),
            initialPermanence = 0.4,
            connectedPermanence = 0.5,
            minThreshold = 4,
            maxNewSynapseCount = 4,
            permanenceDecrement = 0.05,
            permanenceIncrement = 0.05,
            activationThreshold = 4
        )
        
        self.classifier = CLAClassifier(
            steps = [1, 2, 3],
            alpha = 0.1,
            actValueAlpha = 0.3,
            verbosity = 0
        )
        
        self.classicStructure = {
            'wordInput'     :   'wordEnc',
            'wordEnc'       :   'wordSP',
            'wordSP'        :   'wordTM',
            'wordTM'        :   'generalTM',
            ###
            'actionInput'   :   'actionEnc',
            'actionEnc'     :   'actionSP',
            'actionSP'      :   'actionTM',
            'actionTM'      :   'generalTM',
            ###
            'generalTM'     :   None
        }

        self.modules = {
            'generalTM'     :   self.generalTM,
            'wordTM'        :   self.wordTM,
            'wordSP'        :   self.wordSP,
            'wordEnc'       :   self.wordEncoder, 
            'actionTM'      :   self.actionTM,
            'actionSP'      :   self.actionSP,
            'actionEnc'     :   self.actionEncoder,
        }
        
        self.wordSP.printParameters()
        print ""
        
        #self.layer = Layer(self.wordEncoder, self.actionEncoder, self.wordSP, self.wordTM, self.actionSP, self.actionTM, self.generalSP, self.generalTM, self.classifier)
        self.layer = LSF(self.classicStructure, self.modules, self.classifier)
    
    def extractCategories(self, trainingData):
        for sentence, actionSeq in trainingData:
            for word in sentence:
                if word not in self.words:
                    self.words.append(word)
            for action in actionSeq:
                if action not in self.actions:
                    self.actions.append(action)
    
    def train(self, numIterations, verbose = 0):
        
        for iteration in range(numIterations):
            print "Iteration #{iter}".format(iter = iteration)
            for sentence, actionSeq in trainingData:
                self.layer.inputSentence(sentence, actionSeq, verbose)
                self.wordTM.reset()
                self.actionTM.reset()
                self.generalTM.reset()

if __name__ == '__main__':
    structure = LearningStructure()
    structure.train(50)
