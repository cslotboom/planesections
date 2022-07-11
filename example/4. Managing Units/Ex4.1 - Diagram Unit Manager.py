"""
The following is a more realist example that uses user defined section 
propreties for the beam.

"""

import planesections as ps
import numpy as np

"""
Start by defining the units for the problem, the outputs need to be in a consistent
unit base for FEM.
"""
from planesections.units.metric import m, mm, kN, GPa

E = 9*GPa
d = 300*mm
w = 265*mm
section = ps.SectionRectangle(E, d, w)

L = 10*m
Loffset = 0.5*m
beam = ps.EulerBeam2D(section = section)
x       = np.linspace(0, L, 80)
beam.addNodes(x)

pin   = np.array([1, 1, 0])
beam.setFixity(Loffset, pin)
beam.setFixity(L - Loffset, pin)


q = np.array([0.,-1*kN])
beam.addVerticalLoad(0, -5*kN)
beam.addVerticalLoad(L *0.7, -5*kN)
beam.addVerticalLoad(L, -5*kN)
beam.addDistLoad(0, L, q) 
ps.plotBeamDiagram(beam)


analysis = ps.OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()

ps.plotDisp2D(beam, scale=1000, yunit = 'mm')
ps.plotRotation2D(beam, scale=1000, yunit = 'mrad')


