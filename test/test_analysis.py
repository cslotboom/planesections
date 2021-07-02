# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian
"""

from planesections import EulerBeam, OpenSeesAnalyzer, RecordOutput
# from planesections import EulerBeam
import numpy as np

import openseespy.opensees as op

x = np.array([0,5])
fixities = [np.array([1,1,1], int), np.array([1,1,1], int)]

pointBeam = EulerBeam(x, fixities)
P = np.array([0.,1000.,0.])
pointBeam.addPointLoad(2.5, -P)


q = np.array([0.,-1000.])
q = np.array([0.,-1000.])
distBeam = EulerBeam(x, fixities)
distBeam.addDistLoad(0.,5.,q)
distBeamAnalysis  = OpenSeesAnalyzer(distBeam)

beam = EulerBeam(x, fixities) 
beam.addDistLoad(0.,5.,q) 
beam.addPointLoad(2.5, -P)
analysis = OpenSeesAnalyzer(beam)

def test_nodes():
    pointBeamAnalysis  = OpenSeesAnalyzer(pointBeam)
    pointBeamAnalysis.initModel()
    pointBeamAnalysis.buildNodes()
    out = op.nodeCoord(1)[0]
    
    assert out == 0



def test_EulerElements():
    pointBeamAnalysis  = OpenSeesAnalyzer(pointBeam)
    pointBeamAnalysis.initModel()
    pointBeamAnalysis.buildNodes()
    pointBeamAnalysis.buildEulerBeams()
    out = op.eleNodes(1)
    
    assert out == [1,2]
    
    
def test_node_loads():
    pointBeamAnalysis  = OpenSeesAnalyzer(pointBeam)
    pointBeamAnalysis.initModel()
    pointBeamAnalysis.buildNodes()
    pointBeamAnalysis.buildEulerBeams()    
    pointBeamAnalysis.buildPointLoads()   
    pointBeamAnalysis.buildAnalysisPropreties()
    pointBeamAnalysis.analyze()

    assert op.nodeReaction(3) == [0,500,-625]

def test_ele_loads():
    
    distBeamAnalysis.initModel()
    distBeamAnalysis.buildNodes()
    distBeamAnalysis.buildEulerBeams()
    distBeamAnalysis.buildEleLoads()   
    # op.eleLoad('-ele', 1, '-type', '-beamUniform', 1., 1.)
    # op.eleLoad('-ele', 1, '-type', '-beamUniform',1000.,1000.)

    distBeamAnalysis.buildAnalysisPropreties()
    distBeamAnalysis.analyze()
    # print(op.nodeReaction(2))
    solution = np.array([0,2500,-2083.333333333])
    assert np.sum(np.abs(op.nodeReaction(2) - solution)) < 0.001
    
    
def test_full_beam():
    analysis.runAnalysis()
    solution1 = np.array([0,2500,-2083.333333333])
    solution2 = np.array([0,500,-625])
    solution = solution1 + solution2
    assert np.sum(np.abs(op.nodeReaction(3) - solution)) < 0.001


def test_record_output():
    analysis.runAnalysis()
    RecordOutput(beam)


test_nodes()
test_EulerElements()
test_node_loads()
test_ele_loads()
test_full_beam()
test_record_output()