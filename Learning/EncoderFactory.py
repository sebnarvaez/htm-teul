#  !python2
#  -*- coding: utf-8 -*-
#  EncoderFactory.py
#  Author: Larvasapiens <sebastian.narvaez@correounivalle.edu.co>
#  Created: 2015-11-22
#  Last Modification: 2015-11-22
#  Version: 1.0 [Stable]
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

from __future__ import print_function

import random
import numpy
import string

from nupic.encoders.base import Encoder
from nupic.encoders.category import CategoryEncoder

""" A collection of encoders for use in different Learning Models """

def charToBinary(character, wordLen=8, bitSeparation=0):
    """ 
    Returns: a list of integers containing the binary representation of
    character.
    """
    
    charBits = bin(ord(character))[2:]
    
    if (wordLen < len(charBits)):
        raise ValueError("The wordLen is not big enough to store the binary "\
            "representation of the character '{0}': {1}".format(character, charBits))
    else:
        charBitsList = []
        
        for bit in charBits:
            charBitsList.extend([0] * bitSeparation)
            charBitsList.append(int(bit))
        # Add the missing zeros to complete the wordLen
        word = [0]*((wordLen * (bitSeparation + 1)) - len(charBitsList))
        word.extend(charBitsList)
        return word

class UnifiedCategoryEncoder(CategoryEncoder):

    __doc__ = "docstring inherited from CategoryEncoder:\n" +\
        CategoryEncoder.__doc__
    
    def __init__(self, categories, w=11, forced=True):
        """
        Goes through the training data, exctracts the categories and makes
        one Category Encoder for all of them.
        """
        categoryList = []
        for inputCategories in categories:
            categoryList.extend(list(inputCategories))
            
        super(UnifiedCategoryEncoder, self).__init__(
                w=w,
                categoryList=categoryList,
                forced=forced
            )
            
    def getBucketIndex(self, inputData):
        return self.getBucketIndices(inputData)[0]
        
class CustomEncoder(Encoder):
    """
    Base class that provides some general stuff to use in custom
    encoders. Note that it works only if the child encoder uses an
    alreadyEncoded dict to keep track of the already encoded values.
    """
    
    def getBucketIndices(self, inputData):
    
        encodedData = self.encode(inputData)
        return numpy.where(encodedData > 0)[0]
        
    def getBucketIndex(self, inputData):
    
        if inputData not in self.alreadyEncoded:
            self.encode(inputData)
        
        return self.alreadyEncoded[inputData][1]

class RandomizedLetterEncoder(CustomEncoder):
    """
    Encoder for strings. It encodes each letter into binary and appends
    a random chain of bits at the end.
    """
    
    def __init__(self, width, nRandBits, actBitsPerLetter=1):
        """
        @param width: The size of the encoded list of bits output.
        @param nRandBits: The number of random bits that the output
            will have after the binary representation of the
            string. 0 for a pure string to binary conversion.
        @param actBitsPerLetter: The number of active bits per letter.
        """
        
        if nRandBits > width:
            raise ValueError("nRandBits can't be greater than width.")
        if actBitsPerLetter < 1:
            raise ValueError("There must be at least 1 active bit per letter")
        
        self.width = width
        self.nRandBits = nRandBits
        self.actBitsPerLetter = actBitsPerLetter
        self.alreadyEncoded = dict()

    def getWidth(self):
    
        return self.width
    
    def encode(self, inputData, verbose=0):
        """
        @param inputData
        @param verbose=0
        """
        
        catEnc = CategoryEncoder(self.actBitsPerLetter, list(string.ascii_lowercase),
            forced=True)
        strBinaryLen = len(inputData) * catEnc.getWidth()
        
        if (strBinaryLen + self.nRandBits) > self.width:
            raise ValueError("The string is too long to be encoded with the"\
                "current parameters.")
        strBinary = []
        
        # Encode each char of the string 
        for letter in inputData:
            strBinary.extend(list(catEnc.encode(letter)))
        
        if inputData not in self.alreadyEncoded:
            self.alreadyEncoded[inputData] = (
                [random.randrange(strBinaryLen, self.width) \
                        for _ in xrange(self.nRandBits)],
                (len(self.alreadyEncoded) + 1)
            )
        
        output = numpy.zeros((self.width,), dtype=numpy.uint8)
        output[:strBinaryLen] = strBinary
        output[self.alreadyEncoded[inputData][0]] = 1
        return output

class TotallyRandomEncoder(CustomEncoder):
    """
    Encoder for strings. It encodes each letter into binary and appends
    a random chain of bits at the end.
    """
    
    def __init__(self, width, nActiveBits):
        """
        @param width: The size of the encoded list of bits output.
        @param nActiveBits: The number of active bits. Their possition
            is generated randomly the first time and then retrieved.
        """
        
        if nActiveBits > width:
            raise ValueError("width must be greater than nActiveBits")
        self.width = width
        self.nActiveBits = nActiveBits
        self.alreadyEncoded = dict()

    def getWidth(self):
    
        return self.width
    
    def encode(self, inputData, verbose=0):
        """
        @param inputData
        @param verbose=0
        """
        
        if inputData not in self.alreadyEncoded:
            self.alreadyEncoded[inputData] = (
                numpy.array(
                    [random.randrange(self.width) for _ in xrange(self.nActiveBits)],
                    dtype=numpy.uint8
                ),
                (len(self.alreadyEncoded) + 1)
            )
        
        output = numpy.zeros(self.width, dtype=numpy.uint8)
        output[self.alreadyEncoded[inputData][0]] = 1
            
        return output
