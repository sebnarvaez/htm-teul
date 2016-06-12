
self.wordSP = SpatialPooler(
    inputdimensions=(self.wordencoder.getwidth()),
    columndimensions=(nwords * 3),
    potentialradius=12,
    potentialpct=0.5,
    globalinhibition=true,
    localareadensity=-1.0,
    numactivecolumnsperinharea=5.0,
    stimulusthreshold=0,
    synperminactivedec=0.1,
    synpermactiveinc=0.1,
    synPermConnected=0.1,
    minPctOverlapDutyCycle=0.1,
    minPctActiveDutyCycle=0.1,
    dutyCyclePeriod=10,
    maxBoost=3,
    seed=42,
    spVerbosity=0
)

self.wordTM = TemporalMemory(
    columnDimensions=(nWords * 3,),
    initialPermanence=0.4,
    connectedPermanence=0.5,
    minThreshold=4,
    maxNewSynapseCount=4,
    permanenceDecrement=0.05,
    permanenceIncrement=0.05,
    activationThreshold=4,
    seed=self.tmSeed
)

self.actionSP = SpatialPooler(
    inputDimensions=self.actionEncoder.getWidth(),
    columnDimensions=(nActions * 3),
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
    columnDimensions=(nActions * 3,),
    initialPermanence=0.4,
    connectedPermanence=0.5,
    minThreshold=4,
    maxNewSynapseCount=4,
    permanenceDecrement=0.05,
    permanenceIncrement=0.05,
    activationThreshold=4,
    seed=self.tmSeed
)

generalInputDimensions = max(
        self.wordTM.numberOfCells() + 1,
        self.actionTM.numberOfCells() + 1
    )

self.generalSP = SpatialPooler(
    inputDimensions=generalInputDimensions,
    columnDimensions=(len(self.trainingData) * 3,),
    potentialRadius = 28,
    potentialPct = 0.5,
    globalInhibition = True,
    localAreaDensity = -1.0,
    numActiveColumnsPerInhArea = 5.0,
    stimulusThreshold = 0,
    synPermInactiveDec = 0.1,
    synPermActiveInc = 0.1,
    synPermConnected = 0.1,
    minPctOverlapDutyCycle = 0.1,
    minPctActiveDutyCycle = 0.1,
    dutyCyclePeriod = 10,
    maxBoost = 3,
    seed = 42,
    spVerbosity = 0
)

self.generalTM = TemporalMemory(
    columnDimensions=(len(self.trainingData) * 3,),
    initialPermanence=0.4,
    connectedPermanence=0.5,
    minThreshold=4,
    maxNewSynapseCount=4,
    permanenceDecrement=0.05,
    permanenceIncrement=0.05,
    activationThreshold=4,
    seed=self.tmSeed
)
