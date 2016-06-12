inputDimensions = max(
    self.wordEncoder.getWidth(),
    self.actionEncoder.getWidth()
)

columnDimensions = 4 * max((nWords + nActions),
        len(self.trainingData))

self.generalSP = SpatialPooler(
    inputDimensions=inputDimensions,
    #UCE: (nWords + nActions) * 3, RLE:
    columnDimensions=(columnDimensions,),
    #UCE: 11, RLE:1
    potentialRadius=297,
    #UCE: 11, RLE:1
    potentialPct=0.726248028695,
    globalInhibition=True,
    localAreaDensity=-1.0,
    #4, 4.5 -> 86%
    numActiveColumnsPerInhArea=4.0,
    stimulusThreshold=2,
    synPermInactiveDec=0.165088154764,
    synPermActiveInc=0.1,
    #0.15 -> 86%
    synPermConnected=0.236217765977,
    minPctOverlapDutyCycle=0.302204519404,
    minPctActiveDutyCycle=0.0,
    #20
    dutyCyclePeriod=9,
    #3
    maxBoost=1.0,
    seed=self.spSeed,
    spVerbosity=0,
    wrapAround=True
)

self.generalTM = TemporalMemory(
    columnDimensions=(columnDimensions,),
    cellsPerColumn=64,
    # 4
    activationThreshold=1,
    # 0.3
    initialPermanence=0.263488191214,
    connectedPermanence=0.674714438958,
    minThreshold=4,
    maxNewSynapseCount=4,
    permanenceIncrement=0.117671359444,
    permanenceDecrement=1.0,
    predictedSegmentDecrement=0.0,
    seed=self.tmSeed
)

