# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian
"""


from planesections import EulerBeam2D
# import planesections as ps
import numpy as np
import pytest


x = np.array([0,5])
fixities = [np.array([1,1,1])]*2


def test_init():
        
    beam = EulerBeam2D(x, fixities)
    check1 = beam.nodes[0].x = 0
    
    np.all([1,1])
    assert(check1 == 0)
    
def test_addPointLoad_new():
    """
    Also tests the sort feature, because beam nodes need to be sorted correctly.
    """
    beam = EulerBeam2D(x, fixities)
    
    xload = 3
    pointLoad = np.array([1,1,1])
    beam.addPointLoad(xload, pointLoad)
    
    newNode = beam.nodes[1]
   
    
    assert(newNode.x  == 3)

def test_addPointLoad_existing():
    """
    Note that one must be subtracted from the point load ID to get the index.
    IDs start from 1.

    """

    beam = EulerBeam2D(x, fixities)

    # add a node to the existing location.
    xload = 5
    P = np.array([1,1,1])
    beam.addPointLoad(xload, P)
    
    check1 = len(beam.nodes) == 2
    pointLoad  = beam.pointLoads[beam.nodes[1].pointLoadIDs[0] - 1]
    check2 = np.all(pointLoad.P == P) 

    assert(np.all([check1, check2]))




def test_PointLoad_ID_updating1():
    """
    Checks the node gets updated.
    """
    beam = EulerBeam2D(x, fixities)
    xload = 5
    pointLoad = np.array([1,1,1])
    beam.addPointLoad(xload, pointLoad)
    pointLoadID = 1
    
    check1 = pointLoadID ==beam.nodes[1].pointLoadIDs[0]
        
    assert(check1)
    
def test_PointLoad_ID_updating2():
    """
    Checks the load gets added gets updated.
    """    
    
    beam = EulerBeam2D(x, fixities)
    xload = 5
    pointLoad = np.array([1,1,1])
    beam.addPointLoad(xload, pointLoad)
    
    pointNodeID = 2
    outputID = beam.pointLoads[0].nodeID
    
    # check2 = np.all(beam.nodes[1].pointLoad == pointLoad) 
    # print(outputID)
    assert pointNodeID == outputID

# test_PointLoad_ID_updating2()


def makeBeamDist(x1, x2):
    beam = EulerBeam2D(x, fixities)
    
    distLoad = np.array([1.,1.])
    beam.addDistLoad(x1, x2, distLoad)
    return beam

def test_makeBeamDist_new_nodes():

    beam = makeBeamDist(1,4)

    # beam.add(xload, pointLoad)
    
    check1 = len(beam.nodes) == 4
    check2 = beam.nodes[2].x == 4
        
    assert(np.all([check1,check2]))
    
def test_makeBeamDist_new():

    beam = makeBeamDist(1,4)
   
    check1 = len(beam.eleLoads) == 1
    # check1 = True
    check2 = np.all(beam.eleLoads[0].load == np.array([1.,1.]))
    # check2 = True
    # check2 = np.all(beam.nodes[1].distLoad == distLoad) 
        
    assert(np.all([check1,check2]))


def test_makeBeamDist_existing_nodes():

    beam = makeBeamDist(1,5)
    
    check1 = len(beam.nodes) == 3
    check2 = beam.nodes[2].x == 5
    # check2 = np.all(beam.nodes[1].distLoad == distLoad) 
        
    assert(np.all([check1,check2]))
    
def test_makeBeamDist_existing():

    beam = makeBeamDist(1,5)
   
    check1 = len(beam.eleLoads) == 1
    check2 = np.all(beam.eleLoads[0].load  == np.array([1.,1.]))
    # check2 = np.all(beam.nodes[1].distLoad == distLoad) 
        
    assert(np.all([check1,check2]))


def test_setFixity_existing():
    beam = EulerBeam2D(x, fixities)
    
    newFixity = np.array([0,0,0])
    beam.setFixity(0, newFixity)
    
    check  = np.all(newFixity == beam.nodes[0].fixity)
    assert check
    
    
def test_setFixity_new():
    beam = EulerBeam2D(x, fixities)
    
    newFixity = np.array([0,1,0])
    beam.setFixity(10, newFixity)
    
    check  = np.all(newFixity == beam.nodes[2].fixity)
    assert check    
    
def test_setFixity_input_size():
    with pytest.raises(ValueError):
        beam = EulerBeam2D(x, fixities)
        
        newFixity = np.array([0,1])
        assert beam.setFixity(10, newFixity)
 
        
def test_setFixity_input_vals():
    with pytest.raises(ValueError):
        beam = EulerBeam2D(x, fixities)
        
        newFixity = np.array([0,0,10])
        assert beam.setFixity(10, newFixity)

def test_setFixity_int():
    beam = EulerBeam2D(x, fixities)
    
    newFixity = 0
    beam.setFixity(0, newFixity)
    
    check  = np.all(np.array([0,0,0]) == beam.nodes[0].fixity)
    assert check        
 
    #     check  = np.all(newFixity == beam.nodes[2].fixity)
    # assert check    
    
    # raise ValueError('value must be 0 or None')
    
    # beam.
    
    
    # beam = 





# def test_addPointLoad_old():
#     beam = ps.EulerBeam2D(x, fixities)
    
#     xload = 3
#     beam.addPointLoad(x, pointLoad)
#     pass

# test_init()
# test_addPointLoad_new()
# test_addPointLoad_existing()
# test_makeBeamDist_new_nodes()
# test_makeBeamDist_new()
# test_makeBeamDist_existing_nodes()
# test_makeBeamDist_existing()

# test_setFixity_existing()
# test_setFixity_new()
# test_setFixity_int()

