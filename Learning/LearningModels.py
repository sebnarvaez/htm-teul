#!python2
#-*- coding: utf-8 -*-
#  LearningModels.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-09-30
#  Fecha última modificación: 2015-11-22
#  Versión: 1.2

from __future__ import print_function

from Layer import Layer

from nupic.algorithms.CLAClassifier import CLAClassifier
from nupic.encoders.scalar import ScalarEncoder
from nupic.research.spatial_pooler import SpatialPooler
from nupic.research.temporal_memory import TemporalMemory

class LearningModel():
    """
    This class is intended as a guide for Learning Structure classes.
    It doesn't do anything by itself.
    """
    
    def __init__(self):
        """
        Initialize the module objects, the modules and the structure
        dicts, the layer and any other object you'll need for your
        learning structure
        """
        
        self.iterationsTrained = 0
        self.initModules()
        self.structure = dict()
        self.modules = dict()
        
    def initModules(self):
    
        pass
    
    def inputSentence(self, sentence, verbose=1, learn=False):
    
        pass
    
    def train(self, numIterations, verbose=0):
    
        for iteration in xrange(numIterations):
            print("Iteration "  + str(iteration))
            
            for sentence, actionSeq in self.trainingData:
                inputData = [('wordInput', sentence), ('actionInput', actionSeq)]
                self.layer.processInput(inputData, verbose)
               
                self.reset()
            
            self.iterationsTrained += 1

        
    def reset(self):
		"""
		Resets all the components of the structure to receive a new
		sequence
		"""
		
		for modName in self.modules:
			if modName.endswith('TM'):
				self.modules[modName].reset()

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
        
        self.iterationsTrained = 0
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
        
        self.layer = Layer(self.structure, self.modules, self.classifier)

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
            activationThreshold=4
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
            activationThreshold=4
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
            activationThreshold=4
        )
        
        self.classifier = CLAClassifier(
            steps=[1, 2, 3],
            alpha=0.1,
            actValueAlpha=0.3,
            verbosity=0
        )
    
    def inputSentence(self, sentence, verbose=1, learn=False):
    
        inputData = [('wordInput', sentence)]
        
        return self.layer.processInput(inputData, verbose, learn)


class OneRegionModel(LearningModel):
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
            activationThreshold=4
        )
        
        self.classifier = CLAClassifier(
            steps=[1, 2, 3],
            alpha=0.1,
            actValueAlpha=0.3,
            verbosity=0
        )
    
    def inputSentence(self, sentence, verbose=1, learn=False):
    
        inputData = [('wordInput', sentence)]
        
        return self.layer.processInput(inputData, verbose, learn)

