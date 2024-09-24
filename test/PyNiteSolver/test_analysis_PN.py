# -*- coding: utf-8 -*-
"""
Created on Sun May 23 01:00:41 2021

@author: Christian

Tests if basic objects are being placed correctly in the beam object.
"""

import planesections as ps
import numpy as np

x = np.array([0,5])
fixities = [np.array([1,1,1], int), np.array([1,1,1], int)]

pointBeam = ps.EulerBeam(x, fixities)
P = np.array([0.,1000.,0.])
pointBeam.addPointLoad(2.5, -P)


q = np.array([0.,-1000.])
q = np.array([0.,-1000.])
distBeam = ps.EulerBeam(x, fixities)
distBeam.addDistLoad(0.,5.,q)
distBeamAnalysis  = ps.PyNiteAnalyzer2D(distBeam)

beam = ps.EulerBeam(x, fixities) 
beam.addDistLoad(0.,5.,q) 
beam.addPointLoad(2.5, -P)
analysis = ps.PyNiteAnalyzer2D(beam)

def test_nodes():
    """
    Tests is nodes are positioned properly.
    """
    pointBeamAnalysis  = ps.PyNiteAnalyzer2D(pointBeam)
    pointBeamAnalysis.initModel()
    pointBeamAnalysis.buildNodes()
    out = pointBeamAnalysis.analysisBeam.nodes['N1'].X 
    out2 = pointBeamAnalysis.analysisBeam.nodes['N3'].X 
    
    assert out == 0
    assert out2 == 5


def test_EulerElements():
    """
    Tests the connectivity of beam elements.
    """
    pointBeamAnalysis  = ps.PyNiteAnalyzer2D(pointBeam)
    pointBeamAnalysis.initModel()
    pointBeamAnalysis.buildNodes()
    pointBeamAnalysis.buildEulerBeams()
    out1 = pointBeamAnalysis.analysisBeam.members['M1'].i_node.name
    out2 = pointBeamAnalysis.analysisBeam.members['M1'].j_node.name
    
    assert out1 == 'N1'
    assert out2 == 'N2'
    
    
def test_node_loads():
    pointBeamAnalysis  = ps.PyNiteAnalyzer2D(pointBeam)
    pointBeamAnalysis.initModel()
    pointBeamAnalysis.buildNodes()
    pointBeamAnalysis.buildEulerBeams()    
    pointBeamAnalysis.buildPointLoads()   
    pointBeamAnalysis.analyze()
    
    Rx = pointBeamAnalysis.analysisBeam.nodes['N3'].RxnFX['Combo 1']
    Ry = pointBeamAnalysis.analysisBeam.nodes['N3'].RxnFY['Combo 1']
    M = pointBeamAnalysis.analysisBeam.nodes['N3'].RxnMZ['Combo 1']
    
    assert abs(Rx - 0) < 0.1
    assert abs(Ry - 500) < 0.1
    assert abs(M - -625) < 0.1

def test_ele_loads():
    
    distBeamAnalysis.initModel()
    distBeamAnalysis.buildNodes()
    distBeamAnalysis.buildEulerBeams()
    distBeamAnalysis.buildEleLoads()   
    distBeamAnalysis.analyze()
    
    Rx  = distBeamAnalysis.analysisBeam.nodes['N2'].RxnFX['Combo 1']
    Ry  = distBeamAnalysis.analysisBeam.nodes['N2'].RxnFY['Combo 1']
    M   = distBeamAnalysis.analysisBeam.nodes['N2'].RxnMZ['Combo 1']
    test = np.array([Rx, Ry,M]) 

    solution = np.array([0,2500,-2083.333333333])
    assert np.sum(np.abs(test - solution)) < 0.001
    
    
def test_full_beam():
    analysis.runAnalysis()
    solution1 = np.array([0,2500,-2083.333333333])
    solution2 = np.array([0,500,-625])
    solution = solution1 + solution2
    
    Rx  = analysis.analysisBeam.nodes['N3'].RxnFX['Combo 1']
    Ry  = analysis.analysisBeam.nodes['N3'].RxnFY['Combo 1']
    M   = analysis.analysisBeam.nodes['N3'].RxnMZ['Combo 1']
    test = np.array([Rx, Ry ,M]) 
    
    assert np.sum(np.abs(test - solution)) < 0.001


def test_record_output():
    analysis.runAnalysis()
    # OutputRecorder(beam)


if __name__ == "__main__":

    test_nodes()
    test_EulerElements()
    test_node_loads()
    test_ele_loads()
    test_full_beam()
    test_record_output()