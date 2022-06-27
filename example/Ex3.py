# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian
"""

from planesections import EulerBeam2D, OpenSeesAnalyzer2D, plotMoment2D, plotShear2D
from planesections.diagram import plotBeamDiagram
import numpy as np

kN = 1000

# Initialize beam variables
x1 = 0
x2 = 1
offset = x2/20
x      = np.linspace(0, x2, 80)
fixed  = np.array([1, 1, 0])
roller = np.array([0, 1, 0])

q = np.array([0.,-1*kN])  # element Distributed load

# Set up the beam 
beam = EulerBeam2D(x)
beam.setFixity(x1, fixed)
beam.setFixity(x2, fixed)
beam.setFixity(x2/3, roller)

# apply forces
beam.addVerticalLoad(offset, -2*kN, 'A')
beam.addVerticalLoad(x2/2, -2*kN, 'B')
beam.addVerticalLoad(x2 - offset, -2*kN, 'C')
beam.addDistLoad(0, x2, q) 
plotBeamDiagram(beam)

# run analysis
analysis = OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()

plotShear2D(beam)
plotMoment2D(beam)


