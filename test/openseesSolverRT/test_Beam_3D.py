# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian
"""

import planesections as ps
import numpy as np

# import opensees.openseespy as op
from planesections.builder import Node3D

beam = ps.Beam()

# def test_setbeam
def test_activeNode():
    beam._initDimensionVariables('3D')
    check = beam._activeNodeType is Node3D
    assert check

def test_ndf():

    beam._initDimensionVariables('3D')
    check = beam._ndf == 6
    assert check


def test_addLoad():
    beam._initDimensionVariables('3D')
    beam._initArrays()
    P = np.array([0.,1000.,0.,0.,0.,0.])
    beam.addPointLoad(2.5, P)


    addedForces = beam.pointLoads[0].P
    check = np.all(addedForces== P)

    assert check


def test_addNode_Fixity():
    beam._initDimensionVariables('3D')
    beam._initArrays()
    fixity1 = np.array([1,1,1,0.,0.,0.])
    fixity2 = np.array([1,1,1,0.,1.,1.])
    beam.addNode(0, fixity1)
    beam.addNode(10, fixity2)

    check = np.all(beam.nodes[1].fixity.fixityValues == fixity2)

    assert check

if __name__ == "__main__":
    test_addNode_Fixity()
