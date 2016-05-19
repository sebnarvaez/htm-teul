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
import numpy as np
import operator

operatorMappings = {'>': operator.gt,
                    '<': operator.lt,
                    '>=': operator.ge,
                    '<=': operator.le,
                    '==': operator.eq}


class CommonOverlap:
    """
    Counts the fulfillment of a certain condition across numpy arrays.
    """

    def __init__(self, compOperator, compValue, arrayShape, threshold=0):
        """
        @param compOperator: The operator used to make the comparission
            between each element of an array and the compValue.
            The current supported values are '>', '<', '>=', '<=' and '=='
        @param compValue: The value that each element of the array will
            be compared to.
        @param arrayShape: The shape of the arrays that'll be compared.
        @param threshold: (default=0) If an element has a frequency
            percent greater than the threshold, it's considered common.
        """

        self.__arraysCompared = 0
        self.compOperator = operatorMappings[compOperator]
        self.compValue = compValue
        self.threshold = threshold

        self.absoluteCounts = np.zeros(arrayShape, dtype=np.uint32)
        self.freqPercent = np.zeros(arrayShape, dtype=np.float64)
        self.commonElements = np.zeros(arrayShape, dtype=np.bool)

    def updateCounts(self, array):
        """
        Updates the absolute and relative counts for every element of
        the array fulfilling the condition.

        @param array
        """
        #a = np.array([1, 1, 1, 1], dtype=np.uint8)
        #b = np.array([0, 1, 0, 1], dtype=np.uint8)
        #c = np.copy(a)
        #c.fill(0)
        #c[np.logical_and((a == b), (a > 0))] = 1
        self.__arraysCompared += 1

        self.absoluteCounts[self.compOperator(array, self.compValue)] += 1
        self.freqPercent = self.absoluteCounts / self.__arraysCompared
        self.commonElements = self.freqPercent > self.threshold

if __name__ == "__main__":
    start = CommonOverlap('==', 1, np.zeros([5], dtype=np.uint8).size,
                          threshold=0.5)
    start.updateCounts(np.array([0, 5, 1, 4, 1], dtype=np.uint8))
    start.updateCounts(np.array([0, -1, 1, 0, 1], dtype=np.uint8))
    start.updateCounts(np.array([10, 9, 1, 1, 0], dtype=np.uint8))

    print(start.absoluteCounts)
    print(start.freqPercent)
    print(start.commonElements)
