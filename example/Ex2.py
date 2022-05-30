# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian
"""

import planesections as ps
import numpy as np

"""
Start by defining the units for the problem, then the section dimensions and 
material propreties
"""

GPa = 10**9
m = 1
mm = 0.001
kN = 1000

E = 9*GPa
d = 300*mm
w = 265*mm
L = 5*m
Loffset = 0.5*m

x       = np.linspace(0, L, 80)
fixed   = np.array([1, 1, 0])
q       = np.array([0.,-2*kN])

section = ps.SectionRectangle(E, d, w)
beam = ps.EulerBeam2D(section = section)

beam.addNodes(x)
beam.setFixity(Loffset, fixed)
beam.setFixity(L - Loffset, fixed)
beam.addVerticalLoad(0, -5*kN)
beam.addVerticalLoad(L / 2, -kN)
beam.addVerticalLoad(L, -5*kN)
beam.addDistLoad(0, L, q) 
beam.plot()

analysis = ps.OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()
ps.OutputRecorder2D(beam)
ps.plotDisp2D(beam,scale=1000)


