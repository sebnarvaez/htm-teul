#  !python2
#  -*- coding: utf-8 -*-
#  TestSuite.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-12-03
#  Fecha última modificación: 2015-12-03
#  Versión: 0.1

def testModel(model, testData, fileName='log'):
    """ Creates a report about the success of a trained model """
    
    fileName += '.txt'
    nSuccess = 0
    nHalf = 0
    nFailures = 0
    
    modelName = model.__class__.__name__
    encoderName = model.wordEncoder.__class__.__name__
    
    description = "{0}\n{1}\n{2}\n{3}".format(modelName,
        model.__doc__, encoderName, model.wordEncoder.__doc__)
    
    print('Begining tests')
    
    with open(fileName, 'wb') as logFile:
        logFile.write('')
        logFile.write(description)
        logFile.write('\n\n')
        logFile.write('Model trained {0} iterations'.format(model.iterationsTrained))
        logFile.write('\n'*8) # Leave space for the execution Results
    
        for sentence, actionSeq in testData:
            logFile.write('\n\n-----------------------------\n\n')
            predictions = model.inputSentence(sentence, verbose=0, 
                learn=False)
            
            if predictions[:2] == actionSeq:
                nSuccess += 1
            
            elif (predictions[0] == actionSeq[0]) or\
                    (predictions[1] == actionSeq[1]):
                nHalf += 1
                
            else:
                nFailures += 1
                
            logFile.write('Input Sentence: {0}\n'.format(" ".join(sentence)))
            logFile.write('Expected Action: {0}\n'.format(" ".join(actionSeq)))
            logFile.write('Obtained Action: {0}\n'.format(" ".join(predictions)))
        
        # Write the Results before the details of the run
        logFile.seek(len(description))
        logFile.write('\n\n')
        logFile.write('Results:\n\n')
        logFile.write('\tNumber of Success     : {0}\n'.format(nSuccess))
        logFile.write('\tNumber of Half Success: {0}\n'.format(nHalf))
        logFile.write('\tNumber of Failures    : {0}\n'.format(nFailures))
        
    print("Results written to {0}!".format(fileName))
