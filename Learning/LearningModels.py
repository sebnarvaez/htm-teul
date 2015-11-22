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
        
        self.initModules()
        self.structure = dict()
        self.modules = dict()
        
    def initModules(self):
    
        pass
    
    def inputSentence(self, sentence, verbose=1, learn=False):
    
        pass
    
    def train(self, trainingData, numIterations, verbose=0):
        
        pass

class ClassicModel():
    """
     Encodings:
       Word & Action-> Category
     Structure:
       WordCategory -> WordsSP -> SentencesTM
       ActionCategory -> ActionsSP -> ActionsSeqTM
           SentencesTM + ActionsSeqTM -> generalTM
    """

    def __init__(self, wordEncoder, actionEncoder):
    
        self.wordEncoder = wordEncoder
        self.actionEncoder = actionEncoder
        
        self.initModules()
        
        self.classicStructure = {
            'wordInput' : 'wordEnc',
            'wordEnc' : 'wordSP',
            'wordSP' : 'wordTM',
            'wordTM' : 'generalTM',
            ###
            'actionInput' : 'actionEnc',
            'actionEnc' : 'actionSP',
            'actionSP' : 'actionTM',
            'actionTM' : 'generalTM',
            ###
            'generalTM' : None
        }
        self.modules = {
            'generalTM' : self.generalTM,
            'wordTM' : self.wordTM,
            'wordSP' : self.wordSP,
            'wordEnc' : self.wordEncoder, 
            'actionTM' : self.actionTM,
            'actionSP' : self.actionSP,
            'actionEnc' : self.actionEncoder
        }
        
        self.layer = Layer(self.classicStructure, self.modules, self.classifier)

    def initModules(self):
        
        self.wordSP = SpatialPooler(
            inputDimensions=(self.wordEncoder.getWidth()),
            columnDimensions=(self.wordEncoder.ncategories * 3),
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
            columnDimensions=(self.wordEncoder.ncategories * 3,),
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
            columnDimensions=(self.actionEncoder.ncategories * 3),
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
            columnDimensions=(self.actionEncoder.ncategories * 3,),
            initialPermanence=0.4,
            connectedPermanence=0.5,
            minThreshold=4,
            maxNewSynapseCount=4,
            permanenceDecrement=0.05,
            permanenceIncrement=0.05,
            activationThreshold=4
        )
        
        generalInputDimensions = max(
                self.wordTM.numberOfCells(),
                self.actionTM.numberOfCells()
            )
        
        self.generalSP = SpatialPooler(
            inputDimensions=generalInputDimensions,
            columnDimensions=(1000,), # Aprox. size of the training set * 3
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
            columnDimensions=(
                max(self.wordTM.numberOfCells(), self.actionTM.numberOfCells()),
            ),
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

    def train(self, trainingData, numIterations, verbose=0):
    
        for iteration in range(numIterations):
            print("Iteration "  + str(iteration))
            
            for sentence, actionSeq in trainingData:
                inputData = [('wordInput', sentence), ('actionInput', actionSeq)]
                self.layer.processInput(inputData, verbose)
                
                self.wordTM.reset()
                self.actionTM.reset()
                self.generalTM.reset()
