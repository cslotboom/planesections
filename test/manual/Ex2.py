# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian

Tests a beam with loads close to the end and a pair of pins.
"""

import planesections as ps
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

beam = ps.EulerBeam2D(x)
beam.setFixity(x1 + offset, fixed)
beam.setFixity(x2 - offset, fixed)
beam.setFixity(x2 - offset*2, fixed)

beam.addVerticalLoad(0, -1000.)
beam.addVerticalLoad(2.5, -1000.)
beam.addVerticalLoad(5, -1000.)
beam.addDistLoad(0,5,q) 
beam.addNode(0, label='A') 
# beam.addNode(0.) 

ps.plotBeamDiagram(beam)

analysis = ps.OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()

ps.plotMoment(beam)
ps.plotShear(beam)
ps.plotDisp(beam)
ps.plotRotation(beam)

# Mmin, Mmax = beam.Mmax
# print(beam.Mmax)
# print(beam.reactions)

# print(beam.nodes[3].Fint)

