# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian
Tests if node labels are being set and re-ordered correctly.
"""



import planesections as ps
from planesections.units.metric import m, kN
import numpy as np
# import pytest

x = np.array([0,5])
labels = ['A', 'B']
fixities = [np.array([1,1,1]), np.array([1,1,1])]

L       = 5*m
x       = np.linspace(0, L, 80)
beam    = ps.EulerBeam(x)
diagram = ps.BeamPlotter2D(beam)


def test_stack():
    xcoords = np.array([[0,5],[0,3]])
    fplot = np.array([[0,1],[0,2]])

    stackedCoords = diagram._getStackedPositions(xcoords, fplot)
    
    assert stackedCoords[0] == -1
    assert stackedCoords[1] == -3

def test_stack_2():
    xcoords = np.array([[0,5],[0,3]])
    fplot = np.array([[0,-1],[0,-2]])

    stackedCoords = diagram._getStackedPositions(xcoords, fplot)
    
    assert stackedCoords[0] == 1
    assert stackedCoords[1] == 3


if __name__ == "__main__":
    test_stack()    
    test_stack_2()