# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian
"""

from planesections import EulerBeam, OpenSeesAnalyzer, RecordOutput, plotMoment,plotShear
import numpy as np
import openseespy.opensees as op

x = np.linspace(0,5,80)
fixed = np.array([1,1,0.])

P = np.array([0.,1000.,0.])
q = np.array([0.,-1000.])

beam = EulerBeam()
beam.addNodes(x)
beam.setFixity(.4, fixed)
beam.setFixity(4.60, fixed)

beam.addVerticalLoad(0, -1000.)
beam.addVerticalLoad(2.5, -1000.)
beam.addVerticalLoad(5, -1000.)
beam.addDistLoad(0,5, q) 

beam.plot()
analysis = OpenSeesAnalyzer(beam)
analysis.runAnalysis()
RecordOutput(beam)

plotMoment(beam)
plotShear(beam)
