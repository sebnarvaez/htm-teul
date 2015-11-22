#  !python2
#  -*- coding: utf-8 -*-
#  EncoderFactory.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-11-22
#  Fecha última modificación: 2015-11-22
#  Versión: 0.1

from nupic.encoders.category import CategoryEncoder

""" A collection of encoders for use in different Learning Models """

def unifiedCategoryEnc(trainingData, w=11):
    """
    Goes through the training data, exctracts the categories and makes
    one Category Encoder for all of them.
    """
    
    words = []
    actions = []
    
    for sentence, actionSeq in trainingData:
        for word in sentence:
            if word not in words:
                words.append(word)
                
        for action in actionSeq:
            if action not in actions:
                actions.append(action)
    
    return CategoryEncoder(
            w=w,
            categoryList=(words + actions),
            forced=True
        )
