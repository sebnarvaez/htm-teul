bestScores = [0.0]
bestFindings = [
    {
        'generalTM': {
            'columnDimensions': (2, 6048),
            'cellsPerColumn': 32,
            'initialPermanence': 0.4,
            'connectedPermanence': 0.5,
            'minThreshold': 4,
            'maxNewSynapseCount': 4,
            'permanenceDecrement': 0.05,
            'permanenceIncrement': 0.05,
            'predictedSegmentDecrement': 0.0,
            'activationThreshold': 4,
            'seed': 42
        },
        'generalSP': {
            'columnDimensions': (24,),
            'inputDimensions': (264,),
            'potentialRadius': 28,
            'potentialPct': 0.5,
            'globalInhibition': True,
            'localAreaDensity': 0.02,
            'numActiveColumnsPerInhArea': -1.0,
            'stimulusThreshold': 0,
            'synPermInactiveDec': 0.1,
            'synPermActiveInc': 0.1,
            'synPermConnected': 0.1,
            'minPctOverlapDutyCycle': 0.1,
            'minPctActiveDutyCycle': 0.1,
            'dutyCyclePeriod': 10,
            'maxBoost': 3,
            'seed': 42,
            'spVerbosity': 0,
            'wrapAround': True
        }
    }
]
