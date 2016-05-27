#!python2
#-*- coding: utf-8 -*-
#  ArrayCommonOverlap.py
#  Author: Larvasapiens <sebastian.narvaez@correounivalle.edu.co>
#  Created: 2016-05-11
#  Last Modified: 2016-05-11
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

from __future__ import division
from nupic.algorithms.CLAClassifier import _pFormatArray
from nupic.algorithms.CLAClassifier import *
import numpy as np


class CLAClassifierCond (CLAClassifier):
    __doc__ = """
    Extends the CLAClassifier to infer only the outputs that fulfill
    certain condition(s). CLAClassifier docstring:

    {parent_doc}
    """.format(parent_doc=CLAClassifier.__doc__)

    def compute(self, recordNum, patternNZ, classification, learn, infer,
            conditionFunc):
        __doc__ = """
        @param conditionFunc: Only the actualValues that make this
            function return True will be inferred by this classifier.

        ----
        Docstring from the original CLAClassifier:
        ----

        {parent_doc}
        """.format(parent_doc=CLAClassifier.compute.__doc__)

        # Save the offset between recordNum and learnIteration if this is the
        # first compute
        if self._recordNumMinusLearnIteration is None:
            self._recordNumMinusLearnIteration = recordNum - self._learnIteration

        # Update the learn iteration
        self._learnIteration = recordNum - self._recordNumMinusLearnIteration

        if self.verbosity >= 1:
            print "\n%s: compute" % g_debugPrefix
            print "  recordNum:", recordNum
            print "  learnIteration:", self._learnIteration
            print "  patternNZ (%d):" % len(patternNZ), patternNZ
            print "  classificationIn:", classification

        # Store pattern in our history
        self._patternNZHistory.append((self._learnIteration, patternNZ))

        # To allow multi-class classification, we need to be able to run learning
        # without inference being on. So initialize retval outside
        # of the inference block.
        retval = None

        # ------------------------------------------------------------------------
        # Inference:
        # For each active bit in the activationPattern, get the classification
        # votes
        if infer:
            retval = self.infer(patternNZ, classification)

        # Get classification info
        bucketIdx = classification["bucketIdx"]
        actValue = classification["actValue"]

        # ------------------------------------------------------------------------
        # Learning:
        # For each active bit in the activationPattern, store the classification
        # info. If the bucketIdx is None, we can't learn. This can happen when the
        # field is missing in a specific record.
        if learn and (classification["bucketIdx"] is not None) and \
                conditionFunc(actValue):

            # Update maxBucketIndex
            self._maxBucketIdx = max(self._maxBucketIdx, bucketIdx)

            # Update rolling average of actual values if it's a scalar. If it's
            # not, it must be a category, in which case each bucket only ever
            # sees one category so we don't need a running average.
            while self._maxBucketIdx > len(self._actualValues) - 1:
                self._actualValues.append(None)
            if self._actualValues[bucketIdx] is None:
                self._actualValues[bucketIdx] = actValue
            else:
                if isinstance(actValue, int) or isinstance(actValue, float):
                    self._actualValues[bucketIdx] = ((1.0 - self.actValueAlpha)
                                                     * self._actualValues[bucketIdx]
                                                     + self.actValueAlpha * actValue)
                else:
                    self._actualValues[bucketIdx] = actValue

            # Train each pattern that we have in our history that aligns with the
            # steps we have in self.steps
            for nSteps in self.steps:

                # Do we have the pattern that should be assigned to this classification
                # in our pattern history? If not, skip it
                found = False
                for (iteration, learnPatternNZ) in self._patternNZHistory:
                    if iteration == self._learnIteration - nSteps:
                        found = True
                        break
                if not found:
                    continue

                # Store classification info for each active bit from the pattern
                # that we got nSteps time steps ago.
                for bit in learnPatternNZ:

                    # Get the history structure for this bit and step #
                    key = (bit, nSteps)
                    history = self._activeBitHistory.get(key, None)
                    if history is None:
                        history = self._activeBitHistory[key] = BitHistory(self,
                                                                           bitNum=bit,
                                                                           nSteps=nSteps)

                    # Store new sample
                    history.store(iteration=self._learnIteration,
                                  bucketIdx=bucketIdx)

        # ------------------------------------------------------------------------
        # Verbose print
        if infer and self.verbosity >= 1:
            print "  inference: combined bucket likelihoods:"
            print "    actual bucket values:", retval["actualValues"]
            for (nSteps, votes) in retval.items():
                if nSteps == "actualValues":
                    continue
                print "    %d steps: " % (nSteps), \
                    _pFormatArray(votes)
                bestBucketIdx = votes.argmax()
                print ("      most likely bucket idx: "
                       "%d, value: %s" % (bestBucketIdx,
                                          retval["actualValues"][bestBucketIdx]))
            print

        return retval

    def infer(self, patternNZ, classification):
        """
        Return the inference value from one input sample. The actual
        learning happens in compute(). The method customCompute() is here to
        maintain backward compatibility.

        Parameters:
        --------------------------------------------------------------------
        patternNZ:      list of the active indices from the output below
        classification: dict of the classification information:
                        bucketIdx: index of the encoder bucket
                        actValue:  actual value going into the encoder

        retval:     dict containing inference results, one entry for each step in
                    self.steps. The key is the number of steps, the value is an
                    array containing the relative likelihood for each bucketIdx
                    starting from bucketIdx 0.

                    for example:
                      {'actualValues': [0.0, 1.0, 2.0, 3.0]
                        1 : [0.1, 0.3, 0.2, 0.7]
                        4 : [0.2, 0.4, 0.3, 0.5]}
        """

        # Return value dict. For buckets which we don't have an actual value
        # for yet, just plug in any valid actual value. It doesn't matter what
        # we use because that bucket won't have non-zero likelihood anyways.

        # NOTE: If doing 0-step prediction, we shouldn't use any knowledge
        #  of the classification input during inference.
        if self.steps[0] == 0:
            defaultValue = 0
        else:
            defaultValue = classification["actValue"]
        actValues = [x if x is not None else defaultValue
                     for x in self._actualValues]
        retval = {"actualValues": actValues}

        # For each n-step prediction...
        for nSteps in self.steps:

            # Accumulate bucket index votes and actValues into these arrays
            sumVotes = numpy.zeros(self._maxBucketIdx + 1)
            bitVotes = numpy.zeros(self._maxBucketIdx + 1)

            # For each active bit, get the votes
            for bit in patternNZ:
                key = (bit, nSteps)
                history = self._activeBitHistory.get(key, None)
                if history is None:
                    continue

                bitVotes.fill(0)
                history.infer(votes=bitVotes)

                sumVotes += bitVotes

            # Return the votes for each bucket, normalized
            total = sumVotes.sum()
            if total > 0:
                sumVotes /= total
            else:
                # If all buckets have zero probability then simply make all of the
                # buckets equally likely. There is no actual prediction for this
                # timestep so any of the possible predictions are just as good.
                if sumVotes.size > 0:
                    sumVotes = numpy.ones(sumVotes.shape)
                    sumVotes /= sumVotes.size

            retval[nSteps] = sumVotes

        return retval

