from Utils.CLAClassifierCond import CLAClassifierCond
from nupic.encoders.category import CategoryEncoder
from nupic.research.spatial_pooler import SpatialPooler
from nupic.research.temporal_memory import TemporalMemory
import numpy

encoder1 = CategoryEncoder(5, ['a', 'b', 'c'], forced=True)
encoder2 = CategoryEncoder(5, ['z', 'x', 'y', 'a'], forced=True)

sp = SpatialPooler(
    inputDimensions=(
        2,
        max(encoder1.getWidth(), encoder2.getWidth())
    ),
    columnDimensions=(2, 20),
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

tm = TemporalMemory(
    columnDimensions=sp.getColumnDimensions(),
    initialPermanence=0.4,
    connectedPermanence=0.5,
    minThreshold=4,
    maxNewSynapseCount=4,
    permanenceDecrement=0.05,
    permanenceIncrement=0.05,
    activationThreshold=4,
)

cla = CLAClassifierCond((1, 2))

spIn = numpy.zeros(sp.getNumInputs(), dtype=numpy.uint8)
spOut = numpy.zeros(sp.getNumColumns(), dtype=numpy.uint8)

trainingData = [
    ['a', 'b', 'c'],
    ['a', 'c', 'b']
]
trainingData2 = [
    (['b', 'c', 'a'], ['z', 'x', 'y'])
]

recordNum = 0

for i in xrange(20):

#    recordNum = 0
#    for dataList in trainingData:
#        print("----------dataList = {}----------".format(dataList))
#
#        for data in dataList:
#            spIn.fill(0)
#            spIn[:sp.getInputDimensions()[1]] = numpy.resize(
#                encoder1.encode(data), sp.getInputDimensions()[1])
#
#            sp.compute(spIn, True, spOut)
#
#            tmIn = set(numpy.where(spOut > 0)[0])
#            tm.compute(tmIn, True)
#
#            retVal = cla.compute(
#                recordNum,
#                tm.activeCells,
#                {
#                    'bucketIdx': encoder1.getBucketIndices(data)[0],
#                    'actValue': data
#                },
#                True,
#                True
#            )
#
#            recordNum += 1
#
#            print("Given: {}, predicted:\n{}".format(data, retVal['actualValues']))
##            print("Given: {}, predicted:\n{}".format(data, retVal))
#            print("Best one: {}".format(
#                retVal['actualValues'][numpy.argmax(retVal[1])]
#            ))

#        tm.reset()
#        recordNum = 0

    for dataList in trainingData2:

        print("----------dataList = {}----------".format(dataList[0]))
        for data in dataList[0]:
            spIn.fill(0)
            spIn[:sp.getInputDimensions()[1]] = numpy.resize(
                encoder1.encode(data), sp.getInputDimensions()[1])

            sp.compute(spIn, True, spOut)

            tmIn = set(numpy.where(spOut > 0)[0])
            tm.compute(tmIn, True)

            retVal = cla.compute(
                recordNum,
                tm.activeCells,
                {
                    'bucketIdx': encoder1.getBucketIndices(data)[0],
                    'actValue': data
                },
                True,
                True,
                lambda x: x.endswith('x') or x.endswith('y') or x.endswith('z')\
                    or x.endswith('a')
            )

            recordNum += 1

            print("Given: {}, predicted:\n{}".format(data, retVal['actualValues']))
            print("Best one: {}".format(
                retVal['actualValues'][numpy.argmax(retVal[1])]
            ))

        #tm.reset()
        #recordNum = 0

        print("----------dataList = {}----------".format(dataList[1]))
        for data in dataList[1]:
            spIn.fill(0)
            spIn[sp.getInputDimensions()[1]:] = numpy.resize(
                encoder2.encode(data), sp.getInputDimensions()[1])

            sp.compute(spIn, True, spOut)

            tmIn = set(numpy.where(spOut > 0)[0])
            tm.compute(tmIn, True)

            retVal = cla.compute(
                recordNum,
                tm.activeCells,
                {
                    'bucketIdx': (encoder1.getWidth() +
                                  encoder2.getBucketIndices(data)[0]),
                    'actValue': data
                },
                True,
                True,
                lambda x: x.endswith('x') or x.endswith('y') or x.endswith('z')
            )

            recordNum += 1

            print("Given: {}, predicted:\n{}".format(data, retVal['actualValues']))
            print("Best one: {}".format(
                retVal['actualValues'][numpy.argmax(retVal[1])]
            ))

        tm.reset()
        #recordNum = 0
