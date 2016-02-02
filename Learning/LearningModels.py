#!python2
#-*- coding: utf-8 -*-
#  LearningModels.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-09-30
#  Fecha última modificación: 2015-11-22
#  Versión: 1.2

from __future__ import print_function

import numpy
import time

from nupic.algorithms.CLAClassifier import CLAClassifier
from nupic.encoders.scalar import ScalarEncoder
from nupic.research.spatial_pooler import SpatialPooler
from nupic.research.temporal_memory import TemporalMemory
from Layer import Layer

class LearningModel(object):
    """
    This class is intended as a guide for Learning Structure classes.
    It doesn't do anything by itself.
    """
    
    def __init__(self):
        """
        Initialize the module objects, the modules and the structure
        dicts, the layer and any other object you'll need for your
        learning structure.
        
        self.initModules()
        self.structure = dict()
        self.modules = dict()
        """
        
        self.iterationsTrained = 0
        self.spSeed = 42
        self.tmSeed = 42
        
    def initModules(self):
    
        pass
    
    def inputSentence(self, sentence, verbosity=1, learn=False):
    
        pass
    
    def train(self, numIterations, maxTime=-1, verbosity=0):
        """
        @param numIterations
        @param maxTime: Training stops if maxTime (in minutes) is
            exceeded. Note that this may interrupt an ongoing train 
            ireration. -1 is no time restrictions.
        @param verbosity: How much verbose about the process. 0 doesn't
            print anything.
        """
        
        startTime = time.time()
        maxTimeReached = False
        
        for iteration in xrange(numIterations):
            print("Iteration " + str(iteration))
            
            for sentence, actionSeq in self.trainingData:
                inputData = [
                    ('wordInput', sentence),
                    ('actionInput', actionSeq)
                ]
                self.layer.processInput(inputData, verbosity)
                self.reset()
                
                if (maxTime > 0):
                    elapsedMinutes = (time.time() - startTime) * (1.0 / 60.0)
                    
                    if (elapsedMinutes > maxTime):
                        maxTimeReached = True
                        print("maxTime reached, training stoped at iteration "\
                            "{}!".format(self.iterationsTrained))
                        break
            
            if maxTimeReached:
                break
            
            self.iterationsTrained += 1
    
    def reset(self):
        """
        Resets all the components of the structure to receive a new
        sequence
        """
        
        for modName in self.modules:
            if modName.endswith('TM'):
                self.modules[modName].reset()
    
    def spParametersStr(self):
        params = ""
        
        for modName in self.modules:
            if modName.endswith('SP'):
                params += "{0}Args = {{\n".format(modName)
                params += "\t'inputDimensions': {0},\n".format(
                    self.modules[modName]._inputDimensions)
                params += "\t'columnDimensions': {0},\n".format(
                    self.modules[modName]._columnDimensions)
                params += "\t'potentialRadius': {0},\n".format(
                    self.modules[modName]._potentialRadius)
                params += "\t'potentialPct': {0},\n".format(
                    self.modules[modName]._potentialPct)
                params += "\t'globalInhibition': {0},\n".format(
                    self.modules[modName]._globalInhibition)
                params += "\t'localAreaDensity': {0},\n".format(
                    self.modules[modName]._localAreaDensity)
                params += "\t'numActiveColumnsPerInhArea': {0},\n".format(
                    self.modules[modName]._numActiveColumnsPerInhArea)
                params += "\t'stimulusThreshold': {0},\n".format(
                    self.modules[modName]._stimulusThreshold)
                params += "\t'synPermInactiveDec': {0},\n".format(
                    self.modules[modName]._synPermInactiveDec)
                params += "\t'synPermActiveInc': {0},\n".format(
                    self.modules[modName]._synPermActiveInc)
                params += "\t'synPermConnected': {0},\n".format(
                    self.modules[modName]._synPermConnected)
                params += "\t'minPctOverlapDutyCycle': {0},\n".format(
                    self.modules[modName]._minPctOverlapDutyCycles)
                params += "\t'minPctActiveDutyCycle': {0},\n".format(
                    self.modules[modName]._minPctActiveDutyCycles)
                params += "\t'dutyCyclePeriod': {0},\n".format(
                    self.modules[modName]._dutyCyclePeriod)
                params += "\t'maxBoost': {0},\n".format(
                    self.modules[modName]._maxBoost)
                params += "\t'seed': {0},\n".format(
                    self.spSeed)
                params += "\t'spVerbosity': {0},\n".format(
                    self.modules[modName]._spVerbosity)
                params += "\t'wrapAround': {0}\n".format(
                    self.modules[modName]._wrapAround)
                params += "}"
                
        return params
    
    def tmParametersStr(self):
        params = ""
        
        for modName in self.modules:
            if modName.endswith('TM'):
                params += "{0}Args = {{\n".format(modName)
                params += "\t'columnDimensions': {0},\n".format(
                    self.modules[modName].columnDimensions)
                params += "\t'cellsPerColumn': {0},\n".format(
                    self.modules[modName].cellsPerColumn)
                params += "\t'activationThreshold': {0},\n".format(
                    self.modules[modName].activationThreshold)
                params += "\t'initialPermanence': {0},\n".format(
                    self.modules[modName].initialPermanence)
                params += "\t'connectedPermanence': {0},\n".format(
                    self.modules[modName].connectedPermanence)
                params += "\t'minThreshold': {0},\n".format(
                    self.modules[modName].minThreshold)
                params += "\t'maxNewSynapseCount': {0},\n".format(
                    self.modules[modName].maxNewSynapseCount)
                params += "\t'permanenceIncrement': {0},\n".format(
                    self.modules[modName].permanenceIncrement)
                params += "\t'permanenceDecrement': {0},\n".format(
                    self.modules[modName].permanenceDecrement)
                params += "\t'predictedSegmentDecrement': {0},\n".format(
                    self.modules[modName].predictedSegmentDecrement)
                params += "\t'seed': {0}\n".format(self.tmSeed)
                params += "}"
        
        return params
        

class ClassicModel(LearningModel):
    """
     Structure:
       WordEncoder -> WordsSP -> SentencesTM
       ActionEncoder -> ActionsSP -> ActionsSeqTM
           SentencesTM + ActionsSeqTM -> generalTM
    """

    def __init__(self, wordEncoder, actionEncoder, trainingSet):
        """
        @param wordEncoder
        @param actionEncoder
        @param dataSet: A module containing the trainingData, all of
            its categories and the inputIdx dict that maps each index
            in categories to an input name.
        """
        
        super(ClassicModel, self).__init__()
        
        self.wordEncoder = wordEncoder
        self.actionEncoder = actionEncoder
        self.trainingData = trainingSet.trainingData
        
        self.initModules(trainingSet.categories, trainingSet.inputIdx)
        
        self.structure = {
            'wordInput' : 'wordEnc',
            'wordEnc' : 'wordSP',
            'wordSP' : 'wordTM',
            'wordTM' : 'generalSP',
            ###
            'actionInput' : 'actionEnc',
            'actionEnc' : 'actionSP',
            'actionSP' : 'actionTM',
            'actionTM' : 'generalSP',
            ###
            'generalSP' : 'generalTM',
            'generalTM' : None
        }
        self.modules = {
            'generalTM' : self.generalTM,
            'generalSP' : self.generalSP,
            'wordTM' : self.wordTM,
            'wordSP' : self.wordSP,
            'wordEnc' : self.wordEncoder, 
            'actionTM' : self.actionTM,
            'actionSP' : self.actionSP,
            'actionEnc' : self.actionEncoder
        }
        
        self.layer = Layer(self.structure, self.modules,
            self.classifier)

    def initModules(self, categories, inputIdx):
        
        nWords = len(categories[inputIdx['wordInput']])
        nActions = len(categories[inputIdx['actionInput']])
        
        self.wordSP = SpatialPooler(
            inputDimensions=(self.wordEncoder.getWidth()),
            columnDimensions=(nWords * 3),
            potentialRadius=12,
            potentialPct=0.5,
            globalInhibition=True,
            localAreaDensity=-1.0,
            numActiveColumnsPerInhArea=5.0,
            stimulusThreshold=0,
            synPermInactiveDec=0.1,
            synPermActiveInc=0.1,
            synPermConnected=0.1,
            minPctOverlapDutyCycle=0.1,
            minPctActiveDutyCycle=0.1,
            dutyCyclePeriod=10, 
            maxBoost=3,
            seed=42,
            spVerbosity=0
        )
        
        self.wordTM = TemporalMemory(
            columnDimensions=(nWords * 3,),
            initialPermanence=0.4,
            connectedPermanence=0.5,
            minThreshold=4,
            maxNewSynapseCount=4,
            permanenceDecrement=0.05,
            permanenceIncrement=0.05,
            activationThreshold=4,
            seed=self.tmSeed
        )
        
        self.actionSP = SpatialPooler(
            inputDimensions=self.actionEncoder.getWidth(),
            columnDimensions=(nActions * 3),
            potentialRadius=12,
            potentialPct=0.5,
            globalInhibition=True,
            localAreaDensity=-1.0,
            numActiveColumnsPerInhArea=5.0,
            stimulusThreshold=0,
            synPermInactiveDec=0.1,
            synPermActiveInc=0.1,
            synPermConnected=0.1,
            minPctOverlapDutyCycle=0.1,
            minPctActiveDutyCycle=0.1,
            dutyCyclePeriod=10, 
            maxBoost=3,
            seed=42,
            spVerbosity=0
        )
        
        self.actionTM = TemporalMemory(
            columnDimensions=(nActions * 3,),
            initialPermanence=0.4,
            connectedPermanence=0.5,
            minThreshold=4,
            maxNewSynapseCount=4,
            permanenceDecrement=0.05,
            permanenceIncrement=0.05,
            activationThreshold=4,
            seed=self.tmSeed
        )
        
        generalInputDimensions = max(
                self.wordTM.numberOfCells() + 1,
                self.actionTM.numberOfCells() + 1
            )
        
        self.generalSP = SpatialPooler(
            inputDimensions=generalInputDimensions,
            columnDimensions=(len(self.trainingData) * 3,),
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
            columnDimensions=(len(self.trainingData) * 3,),
            initialPermanence=0.4,
            connectedPermanence=0.5,
            minThreshold=4,
            maxNewSynapseCount=4,
            permanenceDecrement=0.05,
            permanenceIncrement=0.05,
            activationThreshold=4,
            seed=self.tmSeed
        )
        
        self.classifier = CLAClassifier(
            steps=[1, 2, 3],
            alpha=0.1,
            actValueAlpha=0.3,
            verbosity=0
        )
    
    def inputSentence(self, sentence, verbosity=1, learn=False):
    
        inputData = [('wordInput', sentence)]
        
        return self.layer.processInput(inputData, verbosity, learn)

class OneLevelModel(LearningModel):
    """
     Structure:
       WordEncoder, ActionEncoder -> GeneralSP -> GeneralTM
    """
    
    def __init__(self, wordEncoder, actionEncoder, trainingSet):
        """
        @param wordEncoder
        @param actionEncoder
        @param dataSet: A module containing the trainingData, all of
            its categories and the inputIdx dict that maps each index
            in categories to an input name.
        """
        super(OneLevelModel, self).__init__()
        
        self.wordEncoder = wordEncoder
        self.actionEncoder = actionEncoder
        self.trainingData = trainingSet.trainingData
        
        self.initModules(trainingSet.categories, trainingSet.inputIdx)
        
        self.structure = {
            'wordInput' : 'wordEnc',
            'wordEnc' : 'generalSP',
            ###
            'actionInput' : 'actionEnc',
            'actionEnc' : 'generalSP',
            ###
            'generalSP' : 'generalTM',
            'generalTM' : None
        }
        self.modules = {
            'generalTM' : self.generalTM,
            'generalSP' : self.generalSP,
            'wordEnc' : self.wordEncoder, 
            'actionEnc' : self.actionEncoder
        }
        
        self.layer = Layer(self.structure, self.modules, self.classifier)

    def initModules(self, categories, inputIdx):
        
        nWords = len(categories[inputIdx['wordInput']])
        nActions = len(categories[inputIdx['actionInput']])
        
        inputDimensions = max(
                self.wordEncoder.getWidth(),
                self.actionEncoder.getWidth()
            )
            
        columnDimensions = 2 * max((nWords + nActions),
                len(self.trainingData))
        
        self.generalSP = SpatialPooler(
            inputDimensions=inputDimensions,
            columnDimensions=(columnDimensions,),
            potentialRadius=28,
            potentialPct=0.5,
            globalInhibition=True,
            localAreaDensity=-1.0,
            numActiveColumnsPerInhArea=5.0,
            stimulusThreshold=0,
            synPermInactiveDec=0.1,
            synPermActiveInc=0.1,
            synPermConnected=0.1,
            minPctOverlapDutyCycle=0.1,
            minPctActiveDutyCycle=0.1,
            dutyCyclePeriod=10, 
            maxBoost=3,
            seed=42,
            spVerbosity=0
        ) 
        
        self.generalTM = TemporalMemory(
            columnDimensions=(columnDimensions,),
            initialPermanence=0.4,
            connectedPermanence=0.5,
            minThreshold=4,
            maxNewSynapseCount=4,
            permanenceDecrement=0.05,
            permanenceIncrement=0.05,
            activationThreshold=4,
            #seed=self.tmSeed
        )
        
        self.classifier = CLAClassifier(
            steps=[1, 2, 3],
            alpha=0.1,
            actValueAlpha=0.3,
            verbosity=0
        )
    
    def inputSentence(self, sentence, verbosity=1, learn=False):
    
        inputData = [('wordInput', sentence)]
        
        return self.layer.processInput(inputData, verbosity, learn)

class OneLevelExpModel(LearningModel):
    """
     Structure:
       WordEncoder, ActionEncoder -> GeneralSP -> GeneralTM
    """
    
    def __init__(self, wordEncoder, actionEncoder, trainingSet):
        """
        @param wordEncoder
        @param actionEncoder
        @param dataSet: A module containing the trainingData, all of
            its categories and the inputIdx dict that maps each index
            in categories to an input name.
        """
        
        super(OneLevelExpModel, self).__init__()
        
        self.wordEncoder = wordEncoder
        self.actionEncoder = actionEncoder
        self.trainingData = trainingSet.trainingData
        
        self.initModules(trainingSet.categories, trainingSet.inputIdx)
        
        self.structure = {
            'wordInput' : 'wordEnc',
            'wordEnc' : 'generalSP',
            ###
            'actionInput' : 'actionEnc',
            'actionEnc' : 'generalSP',
            ###
            'generalSP' : 'generalTM',
            'generalTM' : None
        }
        self.modules = {
            'generalTM' : self.generalTM,
            'generalSP' : self.generalSP,
            'wordEnc' : self.wordEncoder, 
            'actionEnc' : self.actionEncoder
        }
        
        self.layer = Layer(self.structure, self.modules, self.classifier)

    def initModules(self, categories, inputIdx):
        
        nWords = len(categories[inputIdx['wordInput']])
        nActions = len(categories[inputIdx['actionInput']])
        
        inputDimensions = max(
            self.wordEncoder.getWidth(),
            self.actionEncoder.getWidth()
        )
            
        columnDimensions = 4 * max((nWords + nActions),
                len(self.trainingData))
        
        self.generalSP = SpatialPooler(
            inputDimensions=inputDimensions,
            #UCE: (nWords + nActions) * 3, RLE: 
            columnDimensions=(columnDimensions,),
            #UCE: 11, RLE:1
            potentialRadius=297,
            #UCE: 11, RLE:1
            potentialPct=0.726248028695,
            globalInhibition=True,
            localAreaDensity=-1.0,
            #4, 4.5 -> 86%
            numActiveColumnsPerInhArea=4.0,
            stimulusThreshold=0,
            synPermInactiveDec=0.121754178434,
            synPermActiveInc=0.1,
            #0.15 -> 86%
            synPermConnected=0.107148493503,
            minPctOverlapDutyCycle=0.137190887797,
            minPctActiveDutyCycle=0.1,
            #20
            dutyCyclePeriod=15, 
            #3
            maxBoost=1.0,
            seed=self.spSeed,
            spVerbosity=0,
            wrapAround=False
        ) 
        
        self.generalTM = TemporalMemory(
            columnDimensions=(columnDimensions,),
            cellsPerColumn=64,
            # 4
            activationThreshold=1,
            # 0.3
            initialPermanence=0.22382208699,
            connectedPermanence=0.674714438958,
            minThreshold=4,
            maxNewSynapseCount=4,
            permanenceIncrement=0.117671359444,
            permanenceDecrement=0.52118115778,
            predictedSegmentDecrement=0.0,
            seed=self.tmSeed
        )
        
        #self.generalSP = SpatialPooler(
            #inputDimensions=inputDimensions,
            ##UCE: (nWords + nActions) * 3, RLE: 
            #columnDimensions=(columnDimensions,),
            ##UCE: 11, RLE:1
            #potentialRadius=inputDimensions,
            ##UCE: 11, RLE:1
            #potentialPct=0.5,
            #globalInhibition=True,
            #localAreaDensity=-1.0,
            ##4, 4.5 -> 86%
            #numActiveColumnsPerInhArea=4,
            #stimulusThreshold=0,
            #synPermInactiveDec=0.1,
            #synPermActiveInc=0.1,
            ##0.15 -> 86%
            #synPermConnected=0.15,
            #minPctOverlapDutyCycle=0.1,
            #minPctActiveDutyCycle=0.1,
            ##20
            #dutyCyclePeriod=16, 
            ##3
            #maxBoost=3,
            #seed=self.spSeed,
            #spVerbosity=0,
            #wrapAround=True
        #) 
        
        #self.generalTM = TemporalMemory(
            #columnDimensions=(columnDimensions,),
            #cellsPerColumn=80,
            ## 4
            #activationThreshold=4,
            ## 0.3
            #initialPermanence=0.3,
            #connectedPermanence=0.575611110106,
            #minThreshold=4,
            #maxNewSynapseCount=4,
            #permanenceIncrement=0.05,
            #permanenceDecrement=0.143945674364,
            #predictedSegmentDecrement=0.0,
            #seed=self.tmSeed
        #)
        
        #generalSPArgs = {
            #'inputDimensions': [297],
            #'columnDimensions': [1440],
            #'potentialRadius': 33,
            #'potentialPct': 0.878502103883,
            #'globalInhibition': False,
            #'localAreaDensity': -1.0,
            #'numActiveColumnsPerInhArea': 282,
            #'stimulusThreshold': 3,
            #'synPermInactiveDec': 0.628325572745,
            #'synPermActiveInc': 0.252328979379,
            #'synPermConnected': 0.674231628955,
            #'minPctOverlapDutyCycle': 0.727506713123,
            #'minPctActiveDutyCycle': 0.61502196691,
            #'dutyCyclePeriod': 85,
            #'maxBoost': 22.7589495827,
            #'seed': 42,
            #'spVerbosity': 0,
            #'wrapAround': False
        #}
        #generalTMArgs = {
            #'columnDimensions': (1440,),
            #'cellsPerColumn': 296,
            #'activationThreshold': 3,
            #'initialPermanence': 0.973159425903,
            #'connectedPermanence': 0.0356029114278,
            #'minThreshold': 35,
            #'maxNewSynapseCount': 20,
            #'permanenceIncrement': 0.768559889207,
            #'permanenceDecrement': 0.932179170176,
            #'predictedSegmentDecrement': 0.358265258558,
            #'seed': 42
        #}

        
        #self.generalSP = SpatialPooler(**generalSPArgs)
        
        #self.generalTM = TemporalMemory(**generalTMArgs)
        
        self.classifier = CLAClassifier(
            steps=[1, 2, 3],
            alpha=0.1,
            actValueAlpha=0.3,
            verbosity=0
        )
    
    def inputSentence(self, sentence, verbosity=1, learn=False):
    
        inputData = [('wordInput', sentence)]
        
        return self.layer.processInput(inputData, verbosity, learn)


class JoinedInputsModel(LearningModel):
    """
    Joins all the words in the sentence in one SDR and tries to predict
    the sequence of actions.
    Structure:
       WordEncoder, ActionEncoder -> GeneralSP -> GeneralTM
    """
    
    def __init__(self, wordEncoder, actionEncoder, trainingSet):
        """
        @param wordEncoder
        @param actionEncoder
        @param dataSet: A module containing the trainingData, all of
            its categories and the inputIdx dict that maps each index
            in categories to an input name.
        """
        
        super(self, JoinedInputsModel).__init__()
        
        self.buckets = dict()
        self.iterationsTrained = 0
        self.wordEncoder = wordEncoder
        self.actionEncoder = actionEncoder
        self.trainingData = trainingSet.trainingData
        
        self.initModules(trainingSet.categories, trainingSet.inputIdx)
        
        self.structure = {
            'wordInput' : 'wordEnc',
            'wordEnc' : 'generalSP',
            ###
            'actionInput' : 'actionEnc',
            'actionEnc' : 'generalSP',
            ###
            'generalSP' : 'generalTM',
            'generalTM' : None
        }
        self.modules = {
            'generalTM' : self.generalTM,
            'generalSP' : self.generalSP,
            'wordEnc' : self.wordEncoder, 
            'actionEnc' : self.actionEncoder
        }
        
        self.layer = Layer(self.structure, self.modules, self.classifier)
    
    def initModules(self, categories, inputIdx):
        
        nWords = len(categories[inputIdx['wordInput']])
        nActions = len(categories[inputIdx['actionInput']])
        
        inputDimensions = max(
                self.wordEncoder.getWidth(),
                self.actionEncoder.getWidth()
            )
            
        columnDimensions = max((nWords + nActions), len(self.trainingData)) * 2
        
        self.generalSP = SpatialPooler(
            inputDimensions=inputDimensions,
            columnDimensions=(columnDimensions,),
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
            columnDimensions=(columnDimensions,),
            initialPermanence=0.4,
            connectedPermanence=0.5,
            minThreshold=4,
            maxNewSynapseCount=4,
            permanenceDecrement=0.05,
            permanenceIncrement=0.05,
            activationThreshold=4,
            seed=self.tmSeed
        )
        
        self.classifier = CLAClassifier(
            steps=[1, 2],
            alpha=0.1,
            actValueAlpha=0.3,
            verbosity=0
        )
    
    def train(self, numIterations, verbosity=0, learn=True):
        
        for iteration in xrange(numIterations):
            if verbosity > 0:
                print("Iteration "  + str(iteration))
            
            recordNum = 0
            
            for sentence, actionSeq in self.trainingData:
                self.inputSentence(sentence, verbosity, learn)
                recordNum += 1
                
                for action in actionSeq:
                    inputData = ('actionInput', action)
                    self.processInput(inputData, recordNum, verbosity, learn)
                    recordNum += 1
                
                self.reset()
            
            self.iterationsTrained += 1
    
    def processInput(self, inputData, recordNum, verbosity=0, learn=False):
        
        inputName = inputData[0]
        actualValue = inputData[1]
        
        if verbosity > 1:
            print("===== " + inputName + ": " + str(actualValue) + " =====")
        
        if inputName == 'wordInput':
            encodedValue = numpy.zeros(
                self.wordEncoder.getWidth(), 
                dtype=numpy.uint8
            )
            
            for word in actualValue:
                encodedValue[self.wordEncoder.getBucketIndices(word)] = 1
            
            actualValue = ' '.join(actualValue)
                    
        elif(inputName == 'actionInput'):
            encodedValue = self.actionEncoder.encode(actualValue)
            
        if actualValue not in self.buckets:
            self.buckets[actualValue] = len(self.buckets)
        
        bucketIndex = self.buckets[actualValue]
        
        if verbosity > 1:
            print("Encoded Value: {0}\n"\
                "Bucket Index: {1}\n".format(encodedValue, bucketIndex))
        
        spOutput = numpy.zeros(self.generalSP.getColumnDimensions(),
                    dtype=numpy.uint8)
        self.generalSP.compute(encodedValue, learn, spOutput)
        
        tmInput = numpy.where(spOutput > 0)[0]
        self.generalTM.compute(set(tmInput), learn)
        
        retVal = self.classifier.compute(
                recordNum=recordNum,
                patternNZ=self.generalTM.activeCells,
                classification={
                    'bucketIdx': self.buckets[actualValue], 
                    'actValue': actualValue
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
        
        if verbosity > 2 :
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
            
        return bestPredictions
    
    def inputSentence(self, sentence, verbosity=0, learn=False):
        
        inputData = ('wordInput', sentence)
        bestPredictions = self.processInput(inputData, 0, verbosity, learn)
        
        if verbosity > 1:
            print('Best Predictions: ' + str(bestPredictions))
        
        return bestPredictions

