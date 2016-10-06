#  !python2
#  -*- coding: utf-8 -*-
#  TestSuite.py
#  Author: Larvasapiens <sebastian.narvaez@correounivalle.edu.co>
#  Created: 2015-12-03
#  Last Modification: 2015-12-03
#  Version: 0.1
#
#  Copyright (C) {2016}  {Sebastián Narváez Rodríguez}
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import time


def testModel(model, testData, maxTime=-1, saveResults=True, fileName='log'):
    """
    Creates a report about the success of a trained model
    @param model
    @param testData
    @param maxTime: If maxTime (in minutes) is exceeded, the tests
        will end. Note that this won't interrupt an ongoing test.
        The TestSuite will wait until the sequence is passed to
        the model and the corresponding result is processed.
    @param saveResults: (boolean)
    @param fileName
    @return:
    """

    fileName += '.txt'
    nSuccess = 0
    nHalf = 0
    nFails = 0

    if saveResults:
        modelName = model.__class__.__name__
        encoderName = model.wordEncoder.__class__.__name__

        description = "{0}\n{1}\n{2}\n{3}\n{4}\n{5}".format(
            modelName,
            model.__doc__,
            model.spParametersStr(),
            model.tmParametersStr(),
            encoderName,
            model.wordEncoder.__doc__
        )
        description += "\n\nModel trained {0} iterations".format(
            model.iterationsTrained
        )

        logFile = open(fileName, 'wb')
        logFile.write('')
        logFile.write(description)
        logFile.write('.' * 107)  # Leave space for the execution Results

    if maxTime > 0:
        startTime = time.time()

    print('Begining tests')

    for sentence, actionSeq in testData:
        predictions = model.inputSentence(sentence, verbosity=0, learn=False)

        if predictions[:2] == actionSeq:
            nSuccess += 1

        elif (predictions[0] == actionSeq[0]) or\
                (predictions[1] == actionSeq[1]):
            nHalf += 1

            if saveResults:
                logFile.write('\n\n-----------------------------\n\n')
                logFile.write(
                    'Input Sentence: {0}\n'.format(" ".join(sentence))
                )
                logFile.write(
                    'Expected Action: {0}\n'.format(" ".join(actionSeq))
                )
                logFile.write(
                    'Obtained Action: {0}\n'.format(" ".join(predictions))
                )

        else:
            nFails += 1

            if saveResults:
                logFile.write('\n\n-----------------------------\n\n')
                logFile.write(
                    'Input Sentence: {0}\n'.format(" ".join(sentence))
                )
                logFile.write(
                    'Expected Action: {0}\n'.format(" ".join(actionSeq))
                )
                logFile.write(
                    'Obtained Action: {0}\n'.format(" ".join(predictions))
                )

        if maxTime > 0:
            elapsedMinutes = (time.time() - startTime) * (1.0 / 60.0)

            if elapsedMinutes > maxTime:
                print("maxTime reached, tests stoped.")
                break

    # Write the Results before the details of the run
    successPercent = float((nSuccess * 10000) / len(testData)) / 100
    halfPercent = float((nHalf * 10000) / len(testData)) / 100
    failPercent = float((nFails * 10000) / len(testData)) / 100

    if saveResults:
        logFile.seek(len(description))
        logFile.write('\n\n')
        logFile.write('Results:\n\n')
        logFile.write('\tNumber of Success     : {0}%\n'.format(
            successPercent))
        logFile.write('\tNumber of Half Success: {0}%\n'.format(
            halfPercent))
        logFile.write('\tNumber of Failures    : {0}%\n'.format(
            failPercent))

        print("Results written to {0}!".format(fileName))

    return {
        'successPercent': successPercent,
        'halfPercent': halfPercent,
        'failPercent': failPercent
    }
