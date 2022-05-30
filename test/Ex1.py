# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian
"""

from planesections import EulerBeam2D, OpenSeesAnalyzer2D, plotMoment,plotShear,plotVertDisp, Node2D
# from planesections import EulerBeam
import numpy as np
from planesections.core import BeamPlotter


import openseespy.opensees as op


x1 = 0
x2 = 3
offset = x2/20

x = np.linspace(0,x2,80)
fixed = np.array([1,1,0.])
roller = np.array([0.,1,0.])

P = np.array([0., 1000.,0.])
q = np.array([0.,-1000.])

beam = EulerBeam2D(x, d = 2)
beam.setFixity(x1 + offset, fixed)
beam.setFixity(x2 - offset, fixed)
beam.setFixity(x2/3, roller)

beam.addVerticalLoad(0, -1000.)
beam.addVerticalLoad(x2/2, -1000.)
beam.addVerticalLoad(x2, -1000.)
beam.addDistLoad(0,x2,q) 
# beam.plot()
beam.addNode(0, label='A') 

analysis = OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()

# plotMoment(beam)
# plotShear(beam)

newPlotter = BeamPlotter(beam)

x = beam.getxLims()
# newPlotter.plotSupports()
newPlotter.plot()
