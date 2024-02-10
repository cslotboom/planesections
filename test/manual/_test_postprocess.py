# -*- coding: utf-8 -*-
"""

@author: Christian

Tests if teh post-processor functions are correctly returning values.
"""


import planesections as ps
import numpy as np
import textalloc as ta
import matplotlib.pyplot as plt


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
# beam.setFixity(x2/3, roller)
beam.addPointLoad(x2/2, [-1000.,-1000,0])


beam.addVerticalLoad(offset, -1000.)
# beam.addVerticalLoad(x2/2, -1000.)
beam.addVerticalLoad(x2 - offset,-1000.)
beam.addVerticalLoad(x2 - offset, -1000.)
beam.addDistLoad(0,x2,q) 

analysis = ps.OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()

ps.plotBeamDiagram(beam)


# =============================================================================
# 
# =============================================================================  


POIOptions = {'showLabels':True}
ps.plotInternalForce(beam,2,scale = 0.001, labelPOI=True, POIOptions = POIOptions, yunit='kNm')
ps.plotInternalForce(beam,0,scale = 0.001, labelPOI=True, POIOptions = POIOptions)

# # ps.plotMoment(beam,labelPOI=True, POIOptions = POIOptions)
ps.plotShear(beam,labelPOI=True, POIOptions = POIOptions)


# ps.plotDisp(beam,labelPOI=True)








