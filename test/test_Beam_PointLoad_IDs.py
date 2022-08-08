# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 19:59:09 2022

@author: Christian
"""

import planesections as ps
import numpy as np

x1 = 0
x2 = 5
x3 = x2/2
x4 = x3/2
q = -8000
fixed = np.array([1, 1, 0.])
q = np.array([0., -5000., 0.])

# print('0 Nodes')
beam = ps.EulerBeam()
# print('1 Nodes')

beam.setFixity(x1, fixed)
beam.setFixity(x2, fixed)
beam.addPointLoad(x3, q)

def test_ID_matches():
    """
    Tests if the ID of a node matches the ID of the force applied
    """
    force = beam.pointLoads[0]
    nodeID = beam.nodes[force.nodeID - 1].ID
    assert nodeID == force.nodeID

for node in beam.nodes:
    print(node.x)
    
def test_ID_updates():
    """
    Checks if the node ID is updating correctly when a point load is added.
    """
    
    
    preAdditionID = beam.pointLoads[0].nodeID
    preAdditionSolution = 2
    
    # Add a point load at half the distance.
    beam.addPointLoad(x4, q)
    
    postAdditionID = beam.pointLoads[0].nodeID
    postAdditionSolution = 3

    assert (preAdditionID == preAdditionSolution) and (postAdditionID == postAdditionSolution)
# test_ID_matches()
# test_ID_updates()


# preAdditionID = beam.pointLoads[0].nodeID