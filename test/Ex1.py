# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian
"""

from planesections import EulerBeam2D, OpenSeesAnalyzer2D, plotMoment2D, plotShear2D

# from planesections import EulerBeam
import numpy as np
from planesections.core import plotBeamDiagram


"""
Goal: Normalize drawing beam size.
"""

x1 = 0
x2 = 1
offset = x2/20

x      = np.linspace(0, x2, 80)
fixed  = np.array([1, 1, 0])
roller = np.array([0, 1, 0])

P = np.array([0., 1000.,0.])
q = np.array([0.,-1000.])

beam = EulerBeam2D(x)
beam.setFixity(x1, fixed)
beam.setFixity(x2, fixed)
beam.setFixity(x2/3, roller)

beam.addVerticalLoad(offset, -1000.)
beam.addVerticalLoad(x2/2, -1000.)
beam.addVerticalLoad(x2 - offset, -1000.)
beam.addDistLoad(0,x2,q) 
beam.addLabel(0, label='A') 
beam.addLabel(x2, label='B') 

analysis = OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()

plotShear2D(beam)
plotMoment2D(beam)

plotBeamDiagram(beam)

