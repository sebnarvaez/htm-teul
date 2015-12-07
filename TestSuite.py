#  !python2
#  -*- coding: utf-8 -*-
#  TestSuite.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-12-03
#  Fecha última modificación: 2015-12-03
#  Versión: 0.1

def testModel(learningModel, testData, description, fileName='log'):
    """ Creates a report about the success of a trained structure """
    
    fileName += '.txt'
    nSuccess = 0
    nHalf = 0
    nFailures = 0
    runDetails = ""
    
    print('Begining tests')
    
    with open(fileName, 'wb') as logFile:
        logFile.write(description)
    
        for sentence, actionSeq in testData:
            runDetails += '\n\n-----------------------------\n\n'
            predictions = learningModel.inputSentence(sentence, verbose=0, 
                learn=False)
            
            if predictions[:2] == actionSeq:
                nSuccess += 1
            
            elif (predictions[0] == actionSeq[0]) or\
                    (predictions[1] == actionSeq[1]):
                nHalf += 1
                
            else:
                nFailures += 1
                
            runDetails += 'Input Sentence: {0}\n'.format(" ".join(sentence))
            runDetails += 'Expected Action: {0}\n'.format(" ".join(actionSeq))
            runDetails += 'Obtained Action: {0}\n'.format(" ".join(predictions))
        
        # Write the Results before the details of the run
        logFile.seek(len(description))
        logFile.write('\n\n')
        logFile.write('Results:\n\n')
        logFile.write('\tNumber of Success     : {0}\n'.format(nSuccess))
        logFile.write('\tNumber of Half Success: {0}\n'.format(nHalf))
        logFile.write('\tNumber of Failures    : {0}\n'.format(nFailures))
        logFile.write(runDetails)
        
    print("Results written to {0}!".format(fileName))
