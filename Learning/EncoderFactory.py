#  !python2
#  -*- coding: utf-8 -*-
#  EncoderFactory.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-11-22
#  Fecha última modificación: 2015-11-22
#  Versión: 1.0 [Stable]

from __future__ import print_function

import random
import numpy

from nupic.encoders.category import CategoryEncoder
from nupic.encoders.base import Encoder

""" A collection of encoders for use in different Learning Models """

def unifiedCategoryEnc(categories, w=11):
    """
    Goes through the training data, exctracts the categories and makes
    one Category Encoder for all of them.
    """
    categoryList = []
    for inputCats in categories:
        categoryList.extend(list(inputCats))
        
    return CategoryEncoder(
            w=w,
            categoryList=categoryList,
            forced=True
        )
        
def intToBinary(num, wordLen):
    """ 
    Returns: a list of integers containing the binary representation of
    num.
    """
    if (wordLen <= 0) or (2 ** wordLen <= num):
        raise ValueError("The wordLen must be big enough to store the binary "\
            "representation of the num. Try (2 ** wordLen > num)")
    else:
        binaryNum = []
        
        for bit in bin(num)[2:]:
            binaryNum.append(int(bit))
        # Add the missing zeros to complete the wordLen
        word = [0]*(wordLen - len(binaryNum))
        word.extend(binaryNum)
        return word
        
class RandomizedLetterEncoder(Encoder):
    """
    Encoder for strings. It encodes each letter into binary and appends
    a random chain of bits at the end.
    """

    def __init__(self, width, minRandBits):
        """
        @param width: The size of the encoded list of bits output.
        @param minRandBits: The minimum number of random bits that the
            output will have after the binary representation of the
            string. 0 for a pure string to binary conversion.
        """
        
        self.width = width
        self.minRandBits = minRandBits
        self.alreadyEncoded = dict()

    def getWidth(self):
    
        return self.width
    
    def encode(self, inputData, verbose=0):
        """
        @param inputData
        @param verbose=0
        """
        
        bitsPerChar = 8
        strBinaryLen = len(inputData) * bitsPerChar
        
        if (strBinaryLen + self.minRandBits) > self.width:
            raise ValueError("The string is too long to be encoded with the"\
                "current width and minRandBits parameters.")
        output = []
        
        # Encode each char of the string 
        for letter in inputData:
            output.extend(intToBinary(ord(letter), bitsPerChar))
        
        if inputData in self.alreadyEncoded:
            output.extend(self.alreadyEncoded[inputData])
            return numpy.array(output, dtype='uint8')
        
        numRandomBits = self.width - strBinaryLen
        randomBits = intToBinary(random.randint(0, 2 ** numRandomBits),
            numRandomBits)
            
        self.alreadyEncoded[inputData] = randomBits
            
        output.extend(randomBits)
        return numpy.array(output, dtype='uint8')
        
    def getBucketIndices(self, inputData):
    
        encodedData = self.encode(inputData)
        return numpy.where(encodedData > 0)[0]
        
