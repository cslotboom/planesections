# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian

Tests propreties of boxes are working correctly, notably
- if the box internal datum and external datum is being set properly.
- if the box internal force has constant value or not.


"""

from planesections.diagram import EleLoadBox
import numpy as np

baseBox     = EleLoadBox([1, 2],      [0, 2],  [1, 1])
distBox1    = EleLoadBox([0, 0.5],    [-1, 0], [0, 0])
linBox1     = EleLoadBox([1, 2],      [0, 1],  [1, 0.5])
linBox2     = EleLoadBox([1.25, 1.5], [-1, 1], [0, 1])

distbox     = EleLoadBox([1.25, 1.5], [1.25, 1.5])
  


def test_Linear_datum():
    assert baseBox.datum == 0
    assert distBox1.datum == 0
    assert linBox1.datum == 0
    assert linBox2.datum == 0
 
def test_Linear_intdatum():
    assert baseBox.intDatum == 0
    assert distBox1.intDatum == 1
    assert linBox1.intDatum == 0
    assert linBox2.intDatum == 0.5
    
def test_Linear_fout():
    assert np.all(np.array(baseBox.fout) == np.array([2, 2]))
    assert np.all(np.array(distBox1.fout) == np.array([-1, -1]))    
    assert np.all(np.array(linBox1.fout) == np.array([1, 0.5]))
    assert np.all(np.array(linBox2.fout) == np.array((-1, 1)))
    
def test_setDatum():
    # avoid side affects by making a new box
    linBox2     = EleLoadBox([1.25, 1.5], [-1, 1], [0, 1])
    linBox2.setDatum(1)
        
    assert linBox2.intDatum == 0.5
    assert linBox2.datum == 1
    assert np.all(np.array(linBox2.y) == np.array((0, 2)))
    assert np.all(np.array(linBox2.fout) == np.array((0, 2)))

    
def test_isConstant():
    
    # linBox2.setDatum(1)
        
    assert linBox2.isConstant == False
    assert linBox2.isConstant == False
    assert baseBox.isConstant == True
    assert distBox1.isConstant == True

    
def test_shiftdatum():
    baseBox     = EleLoadBox([1, 2],      [0, 2],  [1, 1])
    baseBox.shiftDatum(1)
    
    assert np.all(np.array(baseBox.y) == np.array([1, 3]))
    assert np.all(np.array(baseBox.fout) == np.array([3, 3]))
    assert baseBox.datum == 1
    
def test_shiftdatum_neg():
    baseBox     = EleLoadBox([1, 2],      [0, 2],  [1, 1])
    baseBox.shiftDatum(-2)
    
    assert np.all(np.array(baseBox.y) == np.array([-2, 0]))
    assert np.all(np.array(baseBox.fout) == np.array([0, 0]))
    assert baseBox.datum == -2


if __name__ == "__main__":
    test_Linear_datum()
    test_Linear_intdatum()
    test_Linear_fout()
    test_setDatum()
    test_isConstant()
    test_shiftdatum()
    test_shiftdatum_neg()

