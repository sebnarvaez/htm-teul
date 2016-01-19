#!python2
#  -*- coding: utf-8 -*-
#  PramsFinder.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2016-01-16
#  Fecha última modificación: 2016-01-18
#  Versión: 1.0

from __future__ import print_function
import sys
import random
import copy
import time

class Parameter:
    """
    Defines a Parameter to use in the ParamsFinder module.
    """
    
    VALID_CONT_DATATYPES = ('int', 'float')
    VALID_DATATYPES = ('int', 'float', 'bool')
    
    def __init__(self, name, dataType, value=None, minVal=0,
            maxVal=sys.maxint, maxChange=sys.maxint):
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
        """
        
        # Validations:
        if value is None:
            value = {
                'int': random.randint(minVal, maxVal),
                'float': random.triangular(minVal, maxVal),
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

class ParametersFinder:
    """
    Implements an evolutionary algorithm (greedy for this version) to
    find good parameters for python functions.
    """
    
    def __init__(self, n, maxMutations=2):
        """
        @oaram n: Population size.
        @param maxMutations=2: The maximum number of mutations (parameter
            values changed) allowed.
        """
        self.n = n
        self.maxMutations = maxMutations
        
    def _createIndividual(self, baseIndividual, verbosity=0):
        """
        Creates a new individual by making mutations to the
        baseIndividual. An individual is a list of Parameters.
        
        @param baseIndividual
        """
        
        newIndividual = copy.deepcopy(baseIndividual)
        numMutations = random.randint(0, self.maxMutations)
        
        for _ in xrange(numMutations):
            param = random.choice(newIndividual)
            
            newValue = {
                'int': param.value + random.randint(-param.maxChange,
                        param.maxChange),
                'float': param.value + random.triangular(-param.maxChange,
                        param.maxChange),
                'bool': not param.value
            }[param.dataType]
            
            if param.dataType in Parameter.VALID_CONT_DATATYPES:
                
                if newValue > param.maxVal:
                    newValue = param.maxVal
                    
                elif newValue < param.minVal:
                    newValue = param.minVal
            
            param.value = newValue
        
        if verbosity > 1:
            print("New Individual created")
            for param in newIndividual:
                print("{0} = {1}".format(param.name, param.value))
        return newIndividual
    
    def _initPopulation(self, baseIndividuals, verbosity=0):
        """
        Creates a new population of n individuals by making mutations
        to the baseIndividuals. Each base individual will have roughly
        the same amount of children. baseIndividuals are also included. 
        """
        
        self.population = copy.deepcopy(baseIndividuals)
        
        for i in xrange(self.n):
            self.population.append(self._createIndividual(
                    baseIndividuals[i % len(baseIndividuals)]
                ))
    
    def findParams(self, evalFunc, paramsDefinition, nonOptimParams={},
            variety=2, maxTime=-1, minScore=-1, maxIterations=200, verbosity=0):
        """
        The algorithm will iterate until maxIterations, maxTime or
        minScore is reached.
        
        @param evalFunc: A function that takes the parameters,
            evaluates them and return a score (float) indicating how
            they performed. A higher score is assumed to be better.
            The score should always be positive.
        @params *paramsDefinition: An iterable containing the Parameter
            objects corresponding to the evalFunc parameters.
        @param nonOptimParams: A dictionary for all the parameters
            of the evalFunc that won't be taking into account for
            the optimization.
        @param variety=2: The number of individuals that will be taken
            as base for the next generation.
        @param maxIterations=50: The maximum number of Iterations the
            function will make. -1 is infinite.
        @param maxTime=-1: The maximum time (in minutes) that the
            algorithm will iterate. The time is checked after each
            iteration, so it won't interrupt any. -1 is infinite.
        @param minScore=-1: The minimum score that the algorithm must
            reach until it stops. Note that the algorithm may never
            reach a very high score, so it is recommended to always set
            at least one of the other two options (maxIterations and
            maxTime).
        @param verbosity=0: How much verbose about the procedure.
            0 doesn't print anything.
        
        @returns A dictionary with the parameter names as keys and the
            best suited values found.
        """
        #print("Params definition: {0}".format(paramsDefinition))
        
        iterationCount = 0
        # This is a tuple containing (bestIndividuals, bestScores)
        bestFindings = ([paramsDefinition], [0])
        startTime = time.time()
        
        while(True):
            
            if verbosity > 0:
                print("--------------------------------------")
                print("Best Findings:")
                for i in xrange(len(bestFindings[0])):
                    print("Individual with score {0}".format(bestFindings[1][i]))
                    for param in bestFindings[0][i]:
                        print("  {0} = {1}".format(param.name, param.value))
                print("--------------------------------------")
            
            self._initPopulation(bestFindings[0])
            
            for individual in self.population:
                indivParams = {}
                
                for param in individual:
                    indivParams[param.name] = param.value
                
                indivParams.update(nonOptimParams)
                score = evalFunc(**indivParams)
                
                if len(bestFindings[0]) < variety:
                    bestFindings[0].append(individual)
                    bestFindings[1].append(score)
                
                else:
                    for idx, storedScore in enumerate(bestFindings[1]):
                        if score > storedScore:
                            bestFindings[0][idx] = individual            
                            bestFindings[1][idx] = score
                            break
                
            iterationCount +=1
            elapsedMinutes = (time.time() - startTime) * (1.0 / 60.0)
            
            if ((maxIterations != -1) and (iterationCount >= maxIterations)) or\
                    ((maxTime != -1) and (elapsedMinutes >= maxTime)) or\
                    ((minScore != -1) and (score >= minScore)):
                break
            
        bestScoreIdx = max(xrange(len(bestFindings[1])), 
                key=bestFindings[1].__getitem__)
        
        bestIndividual = bestFindings[0][bestScoreIdx]
        bestParameters = {}
        
        for param in bestIndividual:
            bestParameters[param.name] = param.value
            
        return bestParameters

# Test the algorithm.
if __name__ == '__main__':
    def evalFunc(a, b):
        return a - b
    
    paramsFinder = ParametersFinder(5)
    bestParameters = paramsFinder.findParams(
            evalFunc,
            (
                Parameter('a', 'int', minVal=0, maxVal=50, maxChange=5),
                Parameter('b', 'int', minVal=0, maxVal=50, maxChange=5)
            ),
            variety=2,
            maxTime=-1,
            maxIterations=-1,
            minScore=50
        )

    print("BEST FOUND:")
    print(bestParameters)
