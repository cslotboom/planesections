# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian
Tests if node labels are being set and re-ordered correctly.
"""

import planesections as ps
import numpy as np
# import pytest

x = np.array([0,5])
labels = ['A', 'B']
fixities = [np.array([1,1,1]), np.array([1,1,1])]

    
def test_labels_new():
    """
    Also tests the sort feature, because beam nodes need to be sorted correctly.
    """
    beam = ps.EulerBeam2D(x, fixities, labels=labels)
    
    outLabels = []
    for node in beam.nodes:
        outLabels.append(node.label)
    
    check = np.array(outLabels) == np.array(labels) 
    
    assert np.all(check)
    
def test_labels_existing():
    """
    Also tests if new nodes are being integrated with old nodes.
    """
    beam = ps.EulerBeam2D(x, fixities, labels=labels)
    
    beam.addNode(x[0],fixities[0], label = 'C')
    
    expectedlabels = ['C', 'B']
    outLabels = []
    for node in beam.nodes:
        outLabels.append(node.label)
    
    check = np.array(outLabels) == np.array(expectedlabels) 
       
    assert np.all(check)

    
def test_labels_new_node():
    """
    Also tests if new nodes are being integrated with old nodes.
    """
    beam = ps.EulerBeam2D(x, fixities, labels=labels)
    
    beam.addNode(3, label = 'D')
    beam.addNode(6, label = 'C')
    
    expectedlabels = ['A','D','B','C']
    outLabels = []
    for node in beam.nodes:
        outLabels.append(node.label)
    
    check = np.array(outLabels) == np.array(expectedlabels) 
       
    assert np.all(check)

def test_labels_new_Existing():
    """
    Also tests if new nodes are being integrated with old nodes.
    """
    beam = ps.EulerBeam2D(x, fixities, labels=labels)
    
    beam.addNode(3, label = 'D')
    beam.addNode(0, label = 'C')
    
    expectedlabels = ['C','D','B']
    outLabels = []
    for node in beam.nodes:
        outLabels.append(node.label)
    
    check = np.array(outLabels) == np.array(expectedlabels) 
       
    assert np.all(check)

def test_relabel():

    x1 = 0
    x2 = 5
    x = [x1,x2]
    beam = ps.EulerBeam2D(x)
    beam.addNode(0.,label='A') 
    
    check1 = beam.nodes[0].ID == 1
    check2 = beam.nodes[0].label == 'A'
    assert np.all([check1, check2])

# test_labels_new()
# test_labels_existing()
# test_labels_new_node()
# test_labels_new_Existing()
# test_relabel()

