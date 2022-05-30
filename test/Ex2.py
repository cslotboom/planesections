# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian
"""

from planesections import EulerBeam2D, OpenSeesAnalyzer2D, OutputRecorder2D, plotMoment2D,plotShear2D, plotDisp2D, plotRotation2D
# from planesections import EulerBeam
import numpy as np

import openseespy.opensees as op


x1 = 0
x2 = 5
offset = 0.2

x = np.linspace(0,5,80)
fixed = np.array([1,1,0.])
fixed = [1,1,0.]

P = np.array([0.,1000.,0.])
q = np.array([0.,-1000.])

beam = EulerBeam2D(x)
beam.setFixity(x1 + offset, fixed)
beam.setFixity(x2 - offset, fixed)
beam.setFixity(x2 - offset*2, fixed)

beam.addVerticalLoad(0, -1000.)
beam.addVerticalLoad(2.5, -1000.)
beam.addVerticalLoad(5, -1000.)
beam.addDistLoad(0,5,q) 
beam.plot()
beam.addNode(0, label='A') 
# beam.addNode(0.) 


analysis = OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()

plotMoment2D(beam)
plotShear2D(beam)
plotDisp2D(beam)
plotRotation2D(beam)

# Mmin, Mmax = beam.Mmax
# print(beam.Mmax)
# print(beam.reactions)

# print(beam.nodes[3].Fint)

