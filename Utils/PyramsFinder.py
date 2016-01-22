#!python2
#  -*- coding: utf-8 -*-
#  PramsFinder.py
#  Author: Larvasapiens <sebasnr95@gmail.com>
#  Creation Date: 2016-01-16
#  Last Modification: 2016-01-21
#  Version: 1.1

from __future__ import print_function
from multiprocessing import Pool
import itertools
import sys
import random
import copy
import time

# Functions defined at the module level because of conflicts with the
# python's multiprocessing module.
def _applyParams(params):
    """
    @param params: A tuple such that
        params[0] is the function to be evaluated.
        params[1] is a dict of the function's parameters.
    """
    
    evalFunc = params[0]
    methodParams = params[1]
    #print(indivParams)
    return evalFunc(**methodParams)

def _applyParamsToInstanceMethod(params):
    """
    @param params: A tuple such that
        params[0] is the instance of the method.
        params[1] is the name of the method.
        params[2] is a dict of the function's parameters.
    """
    
    instance = params[0]
    methodName = params[1]
    methodParams = params[2]
    #print(indivParams)
    return getattr(instance, methodName)(**methodParams)

class Parameter:
    """
    Defines a Parameter to use in the ParamsFinder module.
    """
    
    VALID_CONT_DATATYPES = ('int', 'float')
    VALID_DATATYPES = ('int', 'float', 'bool')
    
    def __init__(self, name, dataType, value=None, minVal=0,
            maxVal=sys.maxint, maxChange=sys.maxint, mutationProb=1.0):
        """
        Check VALID_DATATYPES and VALID_CONT_DATATYPES for info on what
        kind of Parameters work with this module. value
        
        @param name: Must be the real name of the parameter/argumment
            that's going to be passed to the function you want to
            optimize.
        @param dataType: Should be in VALID_DATATYPES. minVal, maxVal
            and maxChange will only take effect for VALID_CONT_DATATYPES.
        @param value: The value the parameter will start with. It will
            be set randomly if not defined.
        @param minVal=0: The minimum possible value that the parameter
            can take. Only works with numbers.
        @param maxVal=sys.maxint: The maximum possible value that the
            parameter can take. Only works with numbers.
        @param maxChange=None: A mutation will not alter the
            Parameter's value for more than maxChange. Mutations that
            exceeds maxVal will be trimmed to maxVal. If no maxChange
            is specified, mutations can be arbitrarily large.
        @param mutationProb=1.0: The probability of actually mutate the
            parameter if it is choosen for mutation. This will allow 
            you to have extra control on what parameters should be more
            stable. It's useful for discrete dataTypes like bool.
        """
        
        # Validations:
        if value is None:
            value = {
                'int': random.randint(minVal, maxVal),
                'float': random.uniform(minVal, maxVal),
                'bool': random.choice((True, False))
            }[dataType]
        
        if maxVal <= minVal:
            raise ValueError("maxVal must be greater than minVal")
        
        if (value < minVal) or (value > maxVal):    
            raise ValueError("value must range from minVal to maxVal")
        
        if abs(maxChange) > (abs(maxVal) - abs(minVal)):
            raise ValueError("maxChange must not exceed the difference between"\
                "minVal and maxVal")
        
        self.name = name
        self.dataType = dataType
        self.value = value
        self.minVal = minVal
        self.maxVal = maxVal
        self.maxChange = maxChange
        self.mutationProb = mutationProb

class ParametersFinder:
    """
    Implements an evolutionary algorithm (greedy for this version) to
    find good parameters for python functions.
    """
    
    def __init__(self, evalFunc, paramsDefinition, nonOptimParams={},
            isInstanceMethod=False):
        """
        @param evalFunc: A function that takes the parameters,
            evaluates them and return a score (float) indicating how
            they performed. A higher score is assumed to be better.
            The score should always be positive.
        @param paramsDefinition: An iterable containing the Parameter
            objects corresponding to the evalFunc parameters.
        @param nonOptimParams: A dictionary for all the parameters
            of the evalFunc that won't be taken into account for
            the optimization.
        @param isInstanceMethod=False: Set to True if evalFunc is a
            method of a class. This is used to perform a workaround for
            the multiprocessing's inability to work with instance
            methods.
        """
        
        self.evalFunc = evalFunc
        self.paramsDefinition = paramsDefinition
        self.nonOptimParams = nonOptimParams
        self.isInstanceMethod = isInstanceMethod
    
    def _createIndividual(self, baseIndividual, maxMutations, verbosity=0):
        """
        Creates a new individual by making at max maxMutations to the
        baseIndividual. An individual is a list of Parameters.
        
        @param baseIndividual
        @param maxMutations
        """
        
        newIndividual = copy.deepcopy(baseIndividual)
        # As baseIndividuals are always included, there should be at
        # least 1 mutation per individual.
        numMutations = random.randint(1, maxMutations)
        
        for _ in xrange(numMutations):
            param = random.choice(newIndividual)
            
            if random.random() < param.mutationProb:
                newValue = {
                    'int': param.value + (random.choice((-1, 1)) * 
                        random.randint(1, param.maxChange)),
                    'float': param.value + random.uniform(-param.maxChange,
                            param.maxChange),
                    'bool': not param.value
                }[param.dataType]
                
                if param.dataType in Parameter.VALID_CONT_DATATYPES:
                    
                    if newValue > param.maxVal:
                        newValue = param.maxVal
                        
                    elif newValue < param.minVal:
                        newValue = param.minVal
                
                param.value = newValue
        
        return newIndividual
    
    def _initPopulation(self, populationSize, baseIndividuals, maxMutations,
            verbosity=0):
        """
        Creates a new population of populationSize individuals by making
        mutations to the baseIndividuals. Each base individual will have
        roughly the same amount of children. baseIndividuals are also
        included. 
        """
        
        self.population = copy.deepcopy(baseIndividuals)
        
        for i in xrange(populationSize):
            self.population.append(self._createIndividual(
                    baseIndividuals[i % len(baseIndividuals)],
                    maxMutations,
                    verbosity
                ))
    
    def _getIndivParamsDict(self, individual, nonOptimParams):
        indivParams = {}
        
        for param in individual:
            indivParams[param.name] = param.value
            indivParams.update(nonOptimParams)
        
        return indivParams
    
    def findParams(self, populationSize, maxMutations=2, variety=2,
            maxIterations=200, maxTime=-1, minScore=-1, parallelization=False,
            nCores=4, savingFrecuency=-1, verbosity=0):
        """
        The algorithm will iterate until maxIterations, maxTime or
        minScore is reached.
        
        @param populationSize: The size of the population for each
            generation.
        @param maxMutations=2: The maximum number a mutations that is
            allowed to be done to an individual.
        @param variety=2: The number of individuals that will be taken
            as base for the next generation.
        @param maxIterations=200: The maximum number of Iterations the
            function will make. Values <= 0 mean no maxIterations.
        @param maxTime=-1: The maximum time (in minutes) that the
            algorithm will iterate. The time is checked after each
            iteration, so it won't interrupt any. Values <= 0 mean no
            maxTime.
        @param minScore=-1: The minimum score that the algorithm must
            reach until it stops. Note that the algorithm may never
            reach a very high score, so it is recommended to always set
            at least one of the other two options (maxIterations and
            maxTime).
        @param parallelization=False: Whether to use parallelization.
            This uses the python's multiprocessing module.
        @params nCores=4: How many cores to use if parallelization is
            On.
        @param savingFrequency=-1: How often (in generations) the best
            parameters found so far will be saved to a file. Files will
            be saved on PyramsFinder/generation{i}.json -NOT YET
            IMPLEMENTED-
        @param verbosity=0: How much verbose about the procedure.
            0 doesn't print anything.
        
        @returns A dictionary with the parameter names as keys and the
            best suited values found.
        """
        
        iterationCount = 0
        # This is a tuple containing (bestIndividuals, bestScores)
        bestFindings = ([self.paramsDefinition], [0])
        startTime = time.time()
        
        if parallelization:
            pool = Pool(nCores)
        
        while(True):
            
            self._initPopulation(populationSize, bestFindings[0], maxMutations,
                verbosity)
            
            if parallelization:
                paramsList = [
                    self._getIndivParamsDict(individual, self.nonOptimParams)
                    for individual in self.population
                ]
                
                #print(self.population)
                
                if self.isInstanceMethod:
                    instance = self.evalFunc.im_self
                    methodName = self.evalFunc.im_func.func_name
                    scores = pool.map(
                        _applyParamsToInstanceMethod,
                        itertools.izip(
                            itertools.repeat(instance),
                            itertools.repeat(methodName),
                            paramsList
                        )
                    )
                    
                else:
                    scores = pool.map(
                        _applyParams, 
                        itertools.izip(
                            itertools.repeat(self.evalFunc),
                            paramsList
                        )
                    )
            
            else:
                scores = []
                
                for individual in self.population:
                    indivParams = self._getIndivParamsDict(
                        individual,
                        self.nonOptimParams
                    )
                    scores.append(_applyParams((self.evalFunc, indivParams)))
            
            print(scores)
            
            for scoreIdx, score in enumerate(scores):
                
                if verbosity > 1:
                    print("Individual evaluated with score {}".format(score))
                    for param in self.population[scoreIdx]:
                        print("{} = {}".format(param.name, param.value))
                
                if len(bestFindings[0]) < variety:
                    bestFindings[0].append(self.population[scoreIdx])
                    bestFindings[1].append(score)
                
                else:
                
                    for idx, storedScore in enumerate(bestFindings[1]):
                    
                        if score > storedScore:
                            bestFindings[0][idx] = self.population[scoreIdx]
                            bestFindings[1][idx] = score
                            break
            
            iterationCount +=1
            elapsedMinutes = (time.time() - startTime) * (1.0 / 60.0)
            bestScore = max(bestFindings[1])
            
            if ((maxIterations != -1) and (iterationCount >= maxIterations)) or\
                    ((maxTime != -1) and (elapsedMinutes >= maxTime)) or\
                    ((minScore != -1) and (bestScore >= minScore)):
                break
            
            if verbosity > 0:
                print("--------------------------------------")
                print("Best Findings:")
                for i in xrange(len(bestFindings[0])):
                    print("Individual with score {}".format(bestFindings[1][i]))
                    for param in bestFindings[0][i]:
                        print("  {} = {}".format(param.name, param.value))
                print("--------------------------------------")
            
        bestScoreIdx = max(xrange(len(bestFindings[1])), 
                key=bestFindings[1].__getitem__)
        
        bestIndividual = bestFindings[0][bestScoreIdx]
        
        return self._getIndivParamsDict(bestIndividual, self.nonOptimParams)

# Test the algorithm.

