# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian

Repeats the test for a 2D beam, but in 3D instaed
"""

import planesections as ps
import numpy as np
import openseespy.opensees as op

x = np.array([0,5])
fixities2D = [np.array([1,1,1], int), np.array([1,1,1], int)]
fixities3D = [np.array([1,1,1,1,1,1], int), np.array([1,1,1,1,1,1], int)]

pointBeam3D = ps.EulerBeam(x, fixities3D, dimension='3D')
P3D = np.array([0.,1000.,0.,0.,0.,0.])
pointBeam3D.addPointLoad(2.5, -P3D)

q3D = np.array([0.,-1000., 0.])
distBeam3D = ps.EulerBeam(x, fixities3D, dimension='3D')
distBeam3D.addDistLoad(0.,5.,q3D)
distBeamAnalysis3D  = ps.OpenSeesAnalyzer3D(distBeam3D)

beam3D = ps.EulerBeam(x, fixities3D, dimension='3D') 
beam3D.addDistLoadVertical(0.,5., -1000)
beam3D.addVerticalLoad(2.5, -1000)
analysis3D = ps.OpenSeesAnalyzer3D(beam3D)



P3D_2 = np.array([0.,0.,1000.,0.,0.,0.])
pointBeam3D_2 = ps.EulerBeam(x, fixities3D, dimension='3D')
pointBeam3D_2.addPointLoad(2.5, -P3D_2)
analysis3D_2  = ps.OpenSeesAnalyzer3D(pointBeam3D_2)

def test_nodes_3D():
    pointBeamAnalysis  = ps.OpenSeesAnalyzer3D(pointBeam3D)
    pointBeamAnalysis.initModel()
    pointBeamAnalysis.buildNodes()
    out = op.nodeCoord(1)[0]
    
    assert out == 0


def test_EulerElements_3D():
    pointBeamAnalysis  = ps.OpenSeesAnalyzer3D(pointBeam3D)
    pointBeamAnalysis.initModel()
    pointBeamAnalysis.buildNodes()
    pointBeamAnalysis.buildEulerBeams()
    out = op.eleNodes(1)
    
    assert out == [1,2]
    
    
def test_node_loads_3D():
    pointBeamAnalysis  = ps.OpenSeesAnalyzer3D(pointBeam3D)
    pointBeamAnalysis.initModel()
    pointBeamAnalysis.buildNodes()
    pointBeamAnalysis.buildEulerBeams()    
    
    pointBeamAnalysis.buildPointLoads()   
    pointBeamAnalysis.buildAnalysisPropreties()
    pointBeamAnalysis.analyze()
    
    assert np.sum(np.abs(op.nodeReaction(3) - np.array([0,500,0,0,0,-625]))) < 0.001
    # assert op.nodeReaction(3) == [0,500,0,0,0,-625]

def test_node_loads_3D_2():
    """
    Out of plane nodal loads.

    Returns
    -------
    None.

    """
    
    analysis3D_2.runAnalysis()
    # assert op.nodeReaction(3) == [0,0,500,0,-625,0]
    # print(op.nodeReaction(3))
    assert np.sum(np.abs(op.nodeReaction(1) - np.array([0,0,500,0,-625,0]))) < 0.001
    

def test_ele_loads_3D():
    
    distBeamAnalysis3D.initModel()
    distBeamAnalysis3D.buildNodes()
    distBeamAnalysis3D.buildEulerBeams()
    distBeamAnalysis3D.buildEleLoads()   
    # op.eleLoad('-ele', 1, '-type', '-beamUniform', 1., 1.)
    # op.eleLoad('-ele', 1, '-type', '-beamUniform',1000.,1000.)

    distBeamAnalysis3D.buildAnalysisPropreties()
    distBeamAnalysis3D.analyze()
    # print(op.nodeReaction(2))
    solution = np.array([0,2500,0,0,0,-2083.333333333])
    assert np.sum(np.abs(op.nodeReaction(2) - solution)) < 0.001


def test_full_beam_3D():
    analysis3D.runAnalysis()
    solution1 = np.array([0,2500,0,0,0,-2083.333333333])
    solution2 = np.array([0,500, 0,0,0, -625])
    solution = solution1 + solution2
    assert np.sum(np.abs(op.nodeReaction(3) - solution)) < 0.001


