# -*- coding: utf-8 -*-
"""

@author: Christian

Tests if teh post-processor functions are correctly returning values.
"""

import planesections as ps
import numpy as np

from planesections.postprocess.poi import findBeamForcePOI

x1 = 0
x2 = 7
offset = x2*0.6

x      = np.linspace(0, x2, 80)
fixed  = np.array([1, 1, 0])
roller = np.array([0, 1, 0])

P = np.array([0., 1000.,0.])
q = np.array([0.,-1000.])

beam = ps.EulerBeam2D(x)
beam.setFixity(x1, fixed)
beam.addNode(x2/3, label = 'C')
beam.addNode(2*x2/3, label = 'D')
beam.setFixity(x2, fixed)
beam.addPointLoad(x2/2, [-1000.,-1000,0])


beam.addVerticalLoad(offset, -1000.)
beam.addVerticalLoad(x2 - offset,-1000.)
beam.addVerticalLoad(x2 - offset, -1000.)
beam.addDistLoad(0,x2,q) 

analysis = ps.OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()

ps.plotBeamDiagram(beam)


# =============================================================================
# 
# =============================================================================  

def test_moment():
    POIOptions = {'showLabels':True}
    assert len(findBeamForcePOI(beam, 2, POIOptions)) == 3

def test_moment_labels():
    POIOptions = {'showLabels':False}

    assert len(findBeamForcePOI(beam, 2, POIOptions)) == 1

def test_shear():
    POIOptions = {'showLabels':True}
    assert len(findBeamForcePOI(beam, 1, POIOptions)) == 10

def test_shear_labels():
    POIOptions = {'showLabels':False}
    assert len(findBeamForcePOI(beam, 1, POIOptions)) == 8
 
def test_shear_dis():
    POIOptions = {'showDiscontinutiy':False}
    assert len(findBeamForcePOI(beam, 1, POIOptions)) == 4   

if __name__ == "__main__":
    test_moment()
    test_moment_labels()
   
    test_shear()
    test_shear_labels()
    test_shear_dis()






