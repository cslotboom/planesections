# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 19:59:09 2022

@author: Christian
"""

from planesections import EulerBeam2D
import numpy as np

x1 = 0
x2 = 5
x3 = x2/2
x4 = x3/2
q = -8000
fixed = np.array([1, 1, 0.])
q = np.array([0., -5000., 0.])

# print('0 Nodes')
beam = EulerBeam2D()
# print('1 Nodes')

beam.setFixity(x1, fixed)
beam.setFixity(x2, fixed)
beam.addPointLoad(x3, q)
# beam.addPointLoad(x3/6, q)
# beam.addPointLoad(x3/2, q/2)
# beam.setFixity(x2/5, fixed)
# beam.setFixity(x2/6, fixed)


def test_ID_matches():
    force = beam.pointLoads[0]
    nodeID = beam.nodes[force.nodeID].ID
    assert nodeID == force.nodeID

for node in beam.nodes:
    print(node.x)
    
def test_ID_updates():
    
    preAdditionID = beam.pointLoads[0].nodeID
    preAdditionSolution = 1
    beam.addPointLoad(x4, q)
    
    postAdditionID = beam.pointLoads[0].nodeID
    postAdditionSolution = 2
    print(postAdditionID)
    
    print(beam.nodes[postAdditionID].x)
    # for load in beam.pointLoads:
    #     print(load.nodeID)
    #     print(beam.nodes[load.nodeID].x)
        
    # assert (preAdditionID == preAdditionSolution) and (postAdditionID == postAdditionSolution)

test_ID_updates()


