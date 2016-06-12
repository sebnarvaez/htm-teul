
nWords = len(categories[inputIdx['wordInput']])
nActions = len(categories[inputIdx['actionInput']])

inputDimensions = max(
    self.wordEncoder.getWidth(),
    self.actionEncoder.getWidth()
)

columnDimensions = max((nWords + nActions), len(self.trainingData)) * 2

self.generalSP = SpatialPooler(
    inputDimensions=inputDimensions,
    columnDimensions=(columnDimensions,),
    potentialRadius=28,
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

self.generalTM = TemporalMemory(
    columnDimensions=(columnDimensions,),
    initialPermanence=0.4,
    connectedPermanence=0.5,
    minThreshold=4,
    maxNewSynapseCount=4,
    permanenceDecrement=0.05,
    permanenceIncrement=0.05,
    activationThreshold=4,
    seed=self.tmSeed
)
