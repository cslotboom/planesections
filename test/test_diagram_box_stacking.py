# -*- coding: utf-8 -*-
"""
Created on Sun May 23 01:00:41 2021

@author: Christian
Tests if node labels are being set and re-ordered correctly.
"""

# import planesections as ps
from planesections.diagram import EleLoadBox, checkBoxesForOverlap, Boxstacker
import numpy as np



def getPosBoxes():

    bottomBox1  = EleLoadBox([0, 3], [0, 1], [1, 1])
    middleBox1  = EleLoadBox([1, 3], [0, 1], [1, 0], 0.5)
    TopBox1     = EleLoadBox([1, 2], [0, 1], [1, 1])
    boxes       = [bottomBox1, middleBox1, TopBox1]
    return boxes


def getNegBoxes_1():

    bottomBox1  = EleLoadBox([0, 3], [-1, 0], [0, 0])
    middleBox1  = EleLoadBox([1, 3], [-1, 0], [0, 0])
    TopBox1     = EleLoadBox([1, 2], [-1, 0], [0, 0])
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

def test_pos_stack_positions():
    boxes = getPosBoxes()
    stacker = Boxstacker(boxes)
    _ = stacker.setStackedDatums()

    # middleBox1
    # assert checkBoxesForOverlap(baseBox, baseBox) == True
    assert np.all(np.array(boxes[0].y) == np.array([0, 1]))
    assert np.all(np.array(boxes[1].y) == np.array([1, 2]))
    assert np.all(np.array(boxes[2].y) == np.array([2, 3]))



def test_neg_stack_positions_1():
    boxes = getNegBoxes_1()
    stacker = Boxstacker(boxes)
    _ = stacker.setStackedDatums()

    assert np.all(np.array(boxes[0].y) == np.array([-1, 0]))
    assert np.all(np.array(boxes[1].y) == np.array([-2, -1]))
    assert np.all(np.array(boxes[2].y) == np.array([-3, -2]))

def test_neg_stack_positions_2():
    boxes = getNegBoxes_2()
    stacker = Boxstacker(boxes)
    _ = stacker.setStackedDatums()

    # middleBox1
    # assert checkBoxesForOverlap(baseBox, baseBox) == True
    assert np.all(np.array(boxes[0].y) == np.array([-1, 0]))
    assert np.all(np.array(boxes[1].y) == np.array([0, 1]))
    assert np.all(np.array(boxes[2].y) == np.array([-2, -1]))



def test_mixed_stack_positions_1():
    negBox1  = EleLoadBox([0, 3], [-1, 0], [0, 0])
    negBox2  = EleLoadBox([1, 2], [-1, 0], [0, 0])
    
    posBox1  = EleLoadBox([0, 3], [0, 1], [1, 1])
    linBox1  = EleLoadBox([1, 3], [-1, 0], [1, 0], 0.5)
    linBox2  = EleLoadBox([2, 3], [-1, 0], [1, 0], 0.5)
    boxes       = [negBox1, negBox2, posBox1, linBox1, linBox2]
    
    stacker     = Boxstacker(boxes)
    _           = stacker.setStackedDatums()

    # middleBox1
    # assert checkBoxesForOverlap(baseBox, baseBox) == True
    assert np.all(np.array(boxes[0].y) == np.array([-1, 0]))
    assert np.all(np.array(boxes[1].y) == np.array([-2, -1]))

    assert np.all(np.array(boxes[2].y) == np.array([0, 1]))
    assert np.all(np.array(boxes[3].y) == np.array([1, 2]))
    assert np.all(np.array(boxes[4].y) == np.array([2, 3]))


if __name__ == "__main__":
    # pass
    test_pos_stack_positions()
    test_neg_stack_positions_1()
    test_neg_stack_positions_2()
    test_mixed_stack_positions_1()


