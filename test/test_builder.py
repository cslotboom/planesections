# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian
"""


from planesections import EulerBeam
# import planesections as ps
import numpy as np

x = np.array([0,5])
fixities = [np.array([1,1,1]), np.array([1,1,1])]

# class Test:
#     count = 1
#     def __init__(self):
#         self.count+=1
# # ps.EulerBeam(1, 2)
# t1 = Test()
# t2 = Test()
# print(t2.count)

def test_init():
    
    beam = EulerBeam(x, fixities)
    check1 = beam.nodes[0].x = 0
    
    np.all([1,1])
    assert(check1 == 0)
    
def test_addPointLoad_new():
    """
    Also tests the sort feature, because beam nodes need to be sorted correctly.
    """
    beam = EulerBeam(x, fixities)
    
    xload = 3
    pointLoad = np.array([1,1,1])
    beam.addPointLoads(xload, pointLoad)
    
    newNode = beam.nodes[1]
    
    # newNode.x = 3
    
    assert(newNode.x  == 3)

def test_addPointLoad_existing():

    beam = EulerBeam(x, fixities)
    
    xload = 5
    pointLoad = np.array([1,1,1])
    beam.addPointLoads(xload, pointLoad)
    
    check1 = len(beam.nodes) == 2
    check2 = np.all(beam.nodes[1].pointLoad == pointLoad) 
        
    assert(np.all([check1,check2]))



def addDistLoad(x1, x2):
    beam = EulerBeam(x, fixities)
    
    distLoad = np.array([1.,1.])
    beam.addDistLoad(x1, x2, distLoad)
    return beam

def test_addDistLoad_new_nodes():

    beam = addDistLoad(1,4)

    # beam.add(xload, pointLoad)
    
    check1 = len(beam.nodes) == 4
    check2 = beam.nodes[2].x == 4
        
    assert(np.all([check1,check2]))
    
def test_addDistLoad_new():

    beam = addDistLoad(1,4)
   
    check1 = len(beam.eleLoads) == 1
    # check1 = True
    check2 = np.all(beam.eleLoads[0].load == np.array([1.,1.]))
    # check2 = True
    # check2 = np.all(beam.nodes[1].distLoad == distLoad) 
        
    assert(np.all([check1,check2]))


def test_addDistLoad_existing_nodes():

    beam = addDistLoad(1,5)
    
    check1 = len(beam.nodes) == 3
    check2 = beam.nodes[2].x == 5
    # check2 = np.all(beam.nodes[1].distLoad == distLoad) 
        
    assert(np.all([check1,check2]))
    
def test_addDistLoad_existing():

    beam = addDistLoad(1,5)
   
    check1 = len(beam.eleLoads) == 1
    check2 = np.all(beam.eleLoads[0].load  == np.array([1.,1.]))
    # check2 = np.all(beam.nodes[1].distLoad == distLoad) 
        
    assert(np.all([check1,check2]))



# def test_addPointLoad_old():
#     beam = ps.EulerBeam(x, fixities)
    
#     xload = 3
#     beam.addPointLoad(x, pointLoad)
#     pass

test_init()
test_addPointLoad_new()
test_addPointLoad_existing()
test_addDistLoad_new_nodes()
test_addDistLoad_new()
test_addDistLoad_existing_nodes()
test_addDistLoad_existing()