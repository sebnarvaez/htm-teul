#!python2
#  -*- coding: utf-8 -*-
#  PramsFinder.py
#  Author: Larvasapiens <sebasnr95@gmail.com>
#  Creation Date: 2016-01-16
#  Last Modification: 2016-01-22
#  Version: 1.2

from __future__ import print_function
from multiprocessing import Pool
import copy
import itertools
import os
import operator
import random
import sys
import time
import traceback

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
    score = 0
    try:
        score = evalFunc(**methodParams)
    except:
        print("\nAN ERROR OCURRED when evaluating function, the score for "\
            "these parameters will be set to zero:\n{}\n".format(methodParams))
        traceback.print_exc()
    return score

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
    score = 0
    try:
        score = getattr(instance, methodName)(**methodParams)
    except:
        print("\nAN ERROR OCURRED when evaluating function, the score for "\
            "these parameters will be set to zero:\n{}\n".format(methodParams))
        traceback.print_exc()
    return score

class Parameter:
    """
    Defines a Parameter to use in the PyramsFinder module.
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
        @param value: Set it if you have an idea of what could be a 
            good value for this parameter. It will be set randomly if
            not defined.
        @param minVal=0: The minimum possible value that the parameter
            can take. Only works with numbers.
        @param maxVal=sys.maxint: The maximum possible value that the
            parameter can take. Only works with numbers.
        @param maxChange=None: A mutation will not alter the
            Parameter's value for more than maxChange. Mutations that
            exceeds maxVal will be trimmed to maxVal. If no maxChange
            is specified, mutations can be arbitrarily large. Tiny 
            values can lead to a very slow convergence.
        @param mutationProb=1.0: The probability of actually mutate the
            parameter if it is choosen for mutation. This will allow 
            you to have extra control on what parameters should be more
            stable. It's useful for discrete dataTypes like bool.
        """
        
        # Validations:
        if value is None:
            if dataType == 'int':
                value = random.randint(minVal, maxVal)
                
            elif dataType == 'float':
                value = random.uniform(minVal, maxVal)
                
            elif dataType == 'bool':
                value = random.choice((True, False))
        
        if value in Parameter.VALID_CONT_DATATYPES:
        
            if maxVal <= minVal:
                raise ValueError("maxVal must be greater than minVal")
            
            if (value < minVal) or (value > maxVal):
                raise ValueError("value must range from minVal to maxVal")
            
            if abs(maxChange) > (abs(maxVal) - abs(minVal)):
                raise ValueError("maxChange should not exceed the difference "\
                    "between minVal and maxVal")
        
        self.name = name
        self.dataType = dataType
        self.value = value
        self.minVal = minVal
        self.maxVal = maxVal
        self.maxChange = maxChange
        self.mutationProb = mutationProb
    
    def __repr__(self):
        
        return "\nParameter(\n    name='{}',\n    dataType='{}',\n    value={},"\
            "\n    minVal={},\n    maxVal={},\n    maxChange={},\n    "\
            "mutationProb={}\n)".format(self.name,
                self.dataType, self.value, self.minVal, self.maxVal,
                self.maxChange, self.mutationProb)

class Individual:
    
    def __init__(self, parameters, score=0, aptitude=0.0):
        """
        A simple class to hold the properties of an Individual.
        
        @param parameters
        @param score=0
        @param aptitude=0.0
        """
        self.parameters = parameters
        self.score = score
        self.aptitude = aptitude
    
    def getParamsDict(self, nonOptimParams):
        indivParams = {}
        
        for param in self.parameters:
            indivParams[param.name] = param.value
        
        indivParams.update(nonOptimParams)
        
        return indivParams

class ParametersFinder:
    """
    Implements an evolutionary algorithm to find good parameters for
    python functions.
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
            methods. BEWARE of methods that change the object's
            attributes, as it can lead to unexpected results.
        """
        
        self.evalFunc = evalFunc
        self.paramsDefinition = paramsDefinition
        self.nonOptimParams = nonOptimParams
        self.isInstanceMethod = isInstanceMethod
    
    def _createPopulation(self, populationSize, parents, elite, maxMutations,
            verbosity=0):
        """
        @param populationSize
        @param parents: A list of Individual objects.
        @param elite: The best individuals that will remain in the new
            population.
        @param maxMutations: The maximum number of mutations that will
            be done to each parent when creating one of its children.
        @param verbosity=1
        """
        
        population = []
        
        for i in xrange(populationSize):
            population.append(self._createIndividual(
                    parents[i % len(parents)],
                    maxMutations,
                    verbosity
                ))
        
        population.extend(elite)
        
        return population
    
    def _createIndividual(self, baseIndividual, maxMutations, verbosity=0):
        """
        Creates a new individual from baseIndividual and applies at max
        maxMutations. An individual is a list of Parameters.
        
        @param baseIndividual
        @param maxMutations
        @param verbosity=0
        """
        
        newIndividual = copy.deepcopy(baseIndividual)
        # There's at least 1 mutation per individual.
        numMutations = random.randint(1, maxMutations)
        
        for _ in xrange(numMutations):
            choosenParam = random.choice(newIndividual.parameters)
            self._mutateParam(choosenParam, verbosity)
        
        return newIndividual
    
    def _mutateParam(self, param, verbosity=0):
        """ 
        Mutates a given parameter
        
        @param param
        @param verbosity=0
        """
        
        if random.random() < param.mutationProb:
            
            if verbosity > 2:
                print("--- New Individual ---")
                print("Choosen for mutation: {}".format(param.name))
            
            if param.dataType == 'int':
                newValue = param.value + (random.choice((-1, 1)) * 
                    random.randint(1, param.maxChange))
                    
            elif param.dataType == 'float':
                newValue = param.value + random.uniform(-param.maxChange,
                    param.maxChange)
                    
            elif param.dataType == 'bool':
                newValue = not param.value
            
            if param.dataType in Parameter.VALID_CONT_DATATYPES:
                
                if newValue > param.maxVal:
                    newValue = param.maxVal
                    
                elif newValue < param.minVal:
                    newValue = param.minVal
            
            if verbosity > 2:
                print("Before: {}, After: {}".format(param.value, newValue))
            
            param.value = newValue
    
    def _evaluatePopulation(self, population, topScore, nParallelEvals,
            verbosity=0):
        """
        Evaluates the population, giving the score and aptitude to each
        individual.
        
        @param population
        @param topScore: This will be used as a reference to normalize
            the scores.
        @param nParallelEvals: Number of concurrent evaluations. See
            ParametersFinder.findParams docstring for more info.
        @param verbosity=0
        """
        
        if nParallelEvals > 1:
            pool = Pool(nParallelEvals)
            
            paramsList = [
                individual.getParamsDict(self.nonOptimParams)
                for individual in population
            ]
            
            #print(population)
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
            
            pool.close()
        
        else:
            scores = []
            
            for individual in population:
                indivParams = individual.getParamsDict(self.nonOptimParams)
                scores.append(_applyParams((self.evalFunc, indivParams)))
        
        if verbosity > 0:
            print("Scores obtained: {}".format(scores))
        
        for indvIndex, score in enumerate(scores):
            population[indvIndex].score = score
            population[indvIndex].aptitude = float(score) / topScore
            
            if verbosity > 2:
                print("Individual evaluated with score {}".format(score))
                for param in population[indvIndex].parameters:
                    print("{} = {}".format(param.name, param.value))
    
    def _selectParents(self, population, variety, technique, verbosity=0):
        """
        @param population: The current population.
        @param variety: How many parents to select.
        @param technique: The selection technique used. Read more in
            the ParametersFinder.findParams docstring.
        @param verbosity
        """
        
        selectedParents = []
        
        for _ in xrange(variety):
            
            if technique == 'RouletteWheel':
                selectedParents.append(self._selectByRoulette(population, 
                        verbosity))
            
            elif technique == 'StochasticUniversalSampling':
                pass
            
            elif technique == 'Tournament':
                pass
        
        return selectedParents
    
    def _selectByRoulette(self, population, verbosity=0):
        """
        @param population
        @param verbosity=0
        """
    
        totalAptitude = sum([individual.aptitude for individual in population])
        luckyNumber = random.uniform(0, 1) * totalAptitude
                
        for individual in population:
            luckyNumber -= individual.aptitude
            
            if luckyNumber <= 0:
                return individual
        
        return population[-1]
    
    def findParams(self, populationSize, maxMutations=2, variety=2, 
            elitism=1, selectionTechnique='RouletteWheel',
            randomizeFirstGen=False, maxIterations=200, maxTime=-1, minScore=-1,
            nParallelEvals=1, savingFrequency=-1, verbosity=0):
        """
        The algorithm will iterate until maxIterations, maxTime or
        minScore is reached.
        
        @param populationSize: The size of the population for each
            generation.
        @param maxMutations=2: The maximum number a mutations that is
            allowed to be done to an individual.
        @param variety=2: The number of individuals that will be taken
            as base for the next generation.
        @param elitism=1: The number of 'elite' individuals (i.e. those
            with the best score so far) that will be included in the
            population for the next generation. If 0 the new population
            will consist of freshly generated individuals only.
        @param selectionTechnique='RouletteWheel': Can be one of the
            following:
            
            'RouletteWheel'
            'StochasticUniversalSampling'--> NOT YET IMPLEMENTED
            'Tournament' --> NOT YET IMPLEMENTED
        @param randomizeFirstGen=False: Whether to create totally 
            random individuals as parents for the first generation
            until variety is reached, or stay with the paramsDefinition
            as the only parent. This can provide diversity but may lead
            the search far away from the default values provided in
            paramsDefinition (if any default values were provided).
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
        @params nParallelEvals=1: With this you can evaluate multiple
            individuals from the population at the same time. If > 1,
            the python's multiprocessing module is used. This is useful
            when evalFunc is heavy load. A recommended value would be
            the number of cores of your CPU.
        @param savingFrequency=-1: How often (in generations) the best
            parameters found so far will be saved to a file. Files will
            be saved on {function's-name}_Optim/Iteration_{}.py
        @param verbosity=0: How much verbose about the procedure.
            0 doesn't print anything.
        
        @returns A dictionary with the parameter names as keys and the
            best suited values found.
        """
        
        iterationCount = 0
        elite = [Individual(self.paramsDefinition)]
        startTime = time.time()
        
        parents = [Individual(self.paramsDefinition)]
        
        if randomizeFirstGen:
            
            for _ in xrange(variety - 1):
                newParams = []
                for param in self.paramsDefinition:
                     newParams.append(Parameter(
                            name=param.name,
                            dataType=param.dataType,
                            value=None,
                            minVal=param.minVal,
                            maxVal=param.maxVal,
                            maxChange=param.maxChange,
                            mutationProb=param.mutationProb
                        ))
                parents.append(Individual(newParams))
        
        while(True):
            
            population = self._createPopulation(populationSize, parents, elite,
                maxMutations, verbosity)
            
            self._evaluatePopulation(population, minScore, nParallelEvals,
                verbosity)
            # Population is sorted from best to worst score.
            population.sort(
                key=operator.attrgetter('score'),
                reverse=True
            )
            
            elite = population[:elitism]
            
            parents = self._selectParents(population, variety, 
                selectionTechnique, verbosity)
            
            iterationCount +=1
            elapsedMinutes = (time.time() - startTime) * (1.0 / 60.0)
            
            if (savingFrequency > 0) and (iterationCount % savingFrequency == 0):
                
                if self.isInstanceMethod:
                    savingPath = self.evalFunc.im_func.func_name + '_Optim/'
                else:
                    savingPath = self.evalFunc.func_name + '_Optim/'
                
                if not os.path.exists(savingPath):
                    os.mkdir(savingPath)
                
                fileName = savingPath + 'Iteration{}.py'.format(iterationCount)
                
                with open(fileName, 'wb') as savingFile:
                    savingFile.write(
                        'nonOptimParams = {}\n'.format(self.nonOptimParams)
                    )
                    savingFile.write("Best Scores: {}".format(
                            [individual.score for individual in population[:3]
                        )
                    for individual in population[:3]:
                    savingFile.write('bestFindings:\n')
                    for individual in population[:3]:
                        savingFile.write('{}\n'.format(individual.parameters))
            
            if verbosity > 0:
                print("--------------------------------------")
                print("Best Individual with score {}:".format(
                        population[0].score))
                for param in population[0].parameters:
                    print("  {} = {}".format(param.name, param.value))
                print("--------------------------------------")
                print("Selected Individuals:")
                for parent in parents:
                    print("Individual with score {}:\n".format(parent.score))
                    
                    for param in parent.parameters:
                        print("  {} = {}".format(param.name, param.value))
                print("--------------------------------------")
            
            if ((maxIterations != -1) and (iterationCount >= maxIterations)) or\
                    ((maxTime != -1) and (elapsedMinutes >= maxTime)) or\
                    ((minScore != -1) and (population[0].score >= minScore)):
                print("iterationCount: {}".format(iterationCount))
                print("elapsedMinutes: {}".format(elapsedMinutes))
                break
        
        return population[0].getParamsDict(self.nonOptimParams)
