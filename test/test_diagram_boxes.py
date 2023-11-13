# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian
Tests if node labels are being set and re-ordered correctly.
"""

# import planesections as ps
from planesections.diagram import EleLoadBox, checkBoxesForOverlap


baseBox = EleLoadBox([1, 2], [1, 2])
outsideBox1 = EleLoadBox([0, 0.5], [0.25, 0.5])
outsideBox2 = EleLoadBox([1.2, 1.3], [3, 4])

insideBox1 = EleLoadBox([1, 2], [0, 1])
insideBox2 = EleLoadBox([1.25, 1.5], [1.25, 1.5])


def test_inside_sameBox():
    assert checkBoxesForOverlap(baseBox, baseBox)

def test_inside_1():
    assert checkBoxesForOverlap(baseBox, insideBox2)

def test_outside_1():
    assert not checkBoxesForOverlap(baseBox, outsideBox1)

def test_outside_2():
    assert not checkBoxesForOverlap(baseBox, outsideBox2)



if __name__ == "__main__":
    test_inside_sameBox()
    test_inside_1()
    test_outside_1()
    test_outside_2()

