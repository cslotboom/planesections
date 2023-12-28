# -*- coding: utf-8 -*-
"""
Created on Sun May 23 01:00:41 2021

@author: Christian
Tests if node labels are being set and re-ordered correctly.
"""

# import planesections as ps
from planesections.diagram.diagram import EleLoadBox, _setForceVectorLengthEle
import numpy as np


def getPosBoxes():

    bottomBox1  = EleLoadBox([0, 3], [0, 10], [1, 1])
    middleBox1  = EleLoadBox([1, 3], [0, 20], [1, 0], 0.5)
    TopBox1     = EleLoadBox([1, 2], [0, 10], [1, 1])
    boxes       = [bottomBox1, middleBox1, TopBox1]
    return boxes



def getPosBoxes_inclined(factor = 1):

    bottomBox1  = EleLoadBox([0, 3], [0, 10], [1, 0.5])
    middleBox1  = EleLoadBox([1, 3], [0, 20], [1, 0.5], 0.5)
    TopBox1     = EleLoadBox([1, 2], [0, 10], [1, 0])
    boxes       = [bottomBox1, middleBox1, TopBox1]
    return boxes


def getPosBoxes_inclined_neg(factor = 1):

    bottomBox1  = EleLoadBox([0, 3], [-10, 0], [1, 0.5]) # linearly distributed
    middleBox1  = EleLoadBox([1, 3], [-20, 0], [1, 0.5], 0.5) # Lienarly distributed
    TopBox1     = EleLoadBox([1, 2], [-10, 0], [1, 0]) # linearly distributed
    boxes       = [bottomBox1, middleBox1, TopBox1]
    return boxes




def getNegBoxes_1():

    bottomBox1  = EleLoadBox([0, 3], [-10, 0], [0, 0])
    middleBox1  = EleLoadBox([1, 3], [-20, 0], [0, 0])
    TopBox1     = EleLoadBox([1, 2], [-10, 0], [0, 0])
    boxes       = [bottomBox1, middleBox1, TopBox1]
    return boxes



def getNegBoxes_2():

    bottomBox1  = EleLoadBox([0, 3], [-1, 0], [0, 0])
    middleBox1  = EleLoadBox([1, 3], [-1, 0], [1, 0], 0.5)
    TopBox1     = EleLoadBox([1, 2], [-1, 0], [0, 0])
    boxes       = [bottomBox1, middleBox1, TopBox1]
    return boxes

def getNegBoxes_3():

    negBox1  = EleLoadBox([0, 3], [-1, 0], [0, 0])
    linBox1  = EleLoadBox([1, 3], [-1, 0], [1, 0], 0.5)
    negBox2  = EleLoadBox([1, 2], [-1, 0], [0, 0])
    posBox1  = EleLoadBox([0, 3], [-1, 0], [0, 0])
    boxes       = [negBox1, linBox1, negBox2, posBox1]
    return boxes


def test_normalize_pos1():
    boxes = getPosBoxes()
    boxesNew = _setForceVectorLengthEle(boxes)
    assert np.all(np.array(boxesNew[0].y) == np.array([0, 0.5]))
    assert np.all(np.array(boxesNew[1].y) == np.array([0, 0.7]))
    assert np.all(np.array(boxesNew[2].y) == np.array([0, 0.5]))
    
    assert np.all(np.array(boxesNew[0].fout) == np.array([0.5, 0.5]))
    assert np.all(np.array(boxesNew[1].fout) == np.array([0.7, 0]))
    assert np.all(np.array(boxesNew[2].fout) == np.array([0.5, 0.5]))


def test_normalize_neg1():
    boxes       = getNegBoxes_1()
    boxesNew    = _setForceVectorLengthEle(boxes)
    assert np.all(np.array(boxesNew[0].y) == np.array([-0.5,0]))
    assert np.all(np.array(boxesNew[1].y) == np.array([-0.7,0]))
    assert np.all(np.array(boxesNew[2].y) == np.array([-0.5,0]))
    
    assert np.all(np.array(boxesNew[0].fout) == np.array([-0.5, -0.5]))
    assert np.all(np.array(boxesNew[1].fout) == np.array([-0.7, -0.7]))
    assert np.all(np.array(boxesNew[2].fout) == np.array([-0.5, -0.5]))





def test_normalize_mixed_1():
    """
    Tests the last two problems mixed together.
    """
    boxes = getPosBoxes() + getNegBoxes_1()
    boxesNew = _setForceVectorLengthEle(boxes)
    assert np.all(np.array(boxesNew[0].y) == np.array([0, 0.5]))
    assert np.all(np.array(boxesNew[1].y) == np.array([0, 0.7]))
    assert np.all(np.array(boxesNew[2].y) == np.array([0, 0.5]))
    
    assert np.all(np.array(boxesNew[0].fout) == np.array([0.5, 0.5]))
    assert np.all(np.array(boxesNew[1].fout) == np.array([0.7, 0]))
    assert np.all(np.array(boxesNew[2].fout) == np.array([0.5, 0.5]))

    assert np.all(np.array(boxesNew[3].y) == np.array([-0.5,0]))
    assert np.all(np.array(boxesNew[4].y) == np.array([-0.7,0]))
    assert np.all(np.array(boxesNew[5].y) == np.array([-0.5,0]))
    
    assert np.all(np.array(boxesNew[3].fout) == np.array([-0.5, -0.5]))
    assert np.all(np.array(boxesNew[4].fout) == np.array([-0.7, -0.7]))
    assert np.all(np.array(boxesNew[5].fout) == np.array([-0.5, -0.5]))

def test_normalize_pos_inclined():
    """
    Tests negative inclined boxes
    """
    boxes = getPosBoxes_inclined()
    boxesNew = _setForceVectorLengthEle(boxes)
    fstatic = 0.3
    fdynamic = 0.4
        
    assert np.all(np.array(boxesNew[0].y) == np.array([0, 0.5]))
    assert np.all(np.array(boxesNew[1].y) == np.array([0, 0.7]))
    assert np.all(np.array(boxesNew[2].y) == np.array([0, 0.5]))
    
    assert np.all(np.array(boxesNew[0].fout) == np.array([fstatic + fdynamic/2, fstatic + fdynamic/4]))
    assert np.all(np.array(boxesNew[1].fout) == np.array([fstatic + fdynamic  , fstatic + fdynamic/2]))
    assert np.all(np.array(boxesNew[2].fout) == np.array([fstatic + fdynamic/2, 0.0]))

def test_normalize_neg_inclined():
    """
    Tests the last two problems mixed together.
    """
    boxes = getPosBoxes_inclined_neg()
    boxesNew = _setForceVectorLengthEle(boxes)
    fstatic = -0.3
    fdynamic = -0.4
        
    assert np.all(np.array(boxesNew[0].y) == np.array([-0.5, 0]))
    assert np.all(np.array(boxesNew[1].y) == np.array([-0.7, 0]))
    assert np.all(np.array(boxesNew[2].y) == np.array([-0.5, 0]))
    
    assert np.all(np.array(boxesNew[0].fout) == np.array([0, fstatic + fdynamic/4]))
    assert np.all(np.array(boxesNew[1].fout) == np.array([0, fstatic + fdynamic/2]))
    assert np.all(np.array(boxesNew[2].fout) == np.array([0, fstatic+ fdynamic/2]))    

if __name__ == "__main__":
    pass
    test_normalize_pos1()
    test_normalize_neg1()
    test_normalize_mixed_1()
    test_normalize_pos_inclined()
    test_normalize_neg_inclined()


