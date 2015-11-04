# Recorrer palabra por palabra:
word = "mover"
encoding = wordEncoder.encode("mover")
output = np.zeros(wordSP._columnDimensions)
wordSP.compute(encoding, False, output)
inputTM = set(sorted(np.where(output > 0)[0].flat))
wordTM.compute(inputTM, False)
generalTM.compute(wordTM.activeCells, False)
# Print words stuff
print "SpatialPooler Output = " + str(np.where(output > 0)[0])
print "Active cells = " + str(wordTM.activeCells)
print "Active values = ",
columns = wordTM.mapCellsToColumns(wordTM.activeCells)
for column in columns:
    connected = np.zeros(wordSP.getNumInputs(), dtype="int")
    wordSP.getConnectedSynapses(column, connected)
    print wordEncoder.decode(connected)
predictedColumns = wordTM.mapCellsToColumns(wordTM.predictiveCells).keys()
print "TemporalMemory Prediction = " + str(predictedColumns)
print "Predicted values = ",
for prediction in predictedColumns:
    connected = np.zeros(wordSP.getNumInputs(), dtype="int")
    wordSP.getConnectedSynapses(prediction, connected)
    print wordEncoder.decode(connected)

# Recorrer accion por accion:
action = "mover"
encoding = actionEncoder.encode(action)
output = np.zeros(actionSP._columnDimensions)
actionSP.compute(encoding, False, output)
inputTM = set(sorted(np.where(output > 0)[0].flat))
actionTM.compute(inputTM, False)
generalTM.compute(actionTM.activeCells, False)
# Print actions stuff
print "SpatialPooler Output = " + str(np.where(output > 0)[0])
print "Active cells = " + str(actionTM.activeCells)
print "Active values = ",
columns = actionTM.mapCellsToColumns(actionTM.activeCells)
for column in columns:
    connected = np.zeros(actionSP.getNumInputs(), dtype="int")
    actionSP.getConnectedSynapses(column, connected)
    print actionEncoder.decode(connected)
predictedColumns = actionTM.mapCellsToColumns(actionTM.predictiveCells).keys()
print "TemporalMemory Prediction = " + str(predictedColumns)
print "Predicted values = ",
for prediction in predictedColumns:
    connected = np.zeros(actionSP.getNumInputs(), dtype="int")
    actionSP.getConnectedSynapses(prediction, connected)
    print actionEncoder.decode(connected)

# Print general stuff
print "Active cells = " + str(generalTM.activeCells)
print "Active values = ",
sensorCells = generalTM.mapCellsToColumns(generalTM.activeCells)
columns = actionTM.mapCellsToColumns(sensorCells)
for column in columns:
    connected = np.zeros(actionSP.getNumInputs(), dtype="int")
    actionSP.getConnectedSynapses(column, connected)
    print actionEncoder.decode(connected)
predictedCells = generalTM.mapCellsToColumns(generalTM.predictiveCells).keys()
#print "TemporalMemory Prediction = " + str(predictedColumns)
print "Predicted values = ",
predictedColumns = actionTM.mapCellsToColumns(predictedCells).keys()
for prediction in predictedColumns:
    connected = np.zeros(actionSP.getNumInputs(), dtype="int")
    actionSP.getConnectedSynapses(prediction, connected)
    print actionEncoder.decode(connected)

# Recorrer todas las sequencias 1 vez con verbose al maximo
for sentence, actionSeq in zip(sentencesData, actionsData):
    layer.inputSentence(sentence, actionSeq, 2)
    wordTM.reset()
    actionTM.reset()

# Recorrer una sequencia en particular e imprimir las decodificaciones desde TM
wordTM.reset()
actionTM.reset()
generalTM.reset()
layer.inputSentence(sentencesData[0], actionsData[0], 2)
columns = wordTM.mapCellsToColumns(wordTM.activeCells)
for column in columns:
    connected = np.zeros(wordSP.getNumInputs(), dtype="int")
    wordSP.getConnectedSynapses(column, connected)
    print str(wordEncoder.decode(connected))
print "##### Action #####"
for cell in actionTM.activeCells:
    connected = np.zeros(actionSP.getNumInputs(), dtype="int")
    actionSP.getConnectedSynapses((cell / actionTM.cellsPerColumn), connected)
    print str(actionEncoder.decode(connected))
