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

"""
Define the material properties then make the rectangular section.
"""
E = 9*GPa
d = 300*mm
w = 265*mm
section = ps.SectionRectangle(E, d, w)

"""
Define the beam. In this example we will define the node coordinants directly,
then add those to the beam. By manually defining the node coordinants, it 
is possible to place them anywhere in the beam desired.
"""
L = 10*m
Loffset = 0.5*m
beam = ps.EulerBeam(section = section)
x       = np.linspace(0, L, 80)
beam.addNodes(x)

"""
Define the node fixities. The fixity is a list for each DOF, where 1 represents
fixed, and 0 represents free in this case two pin constraints are applied to the
beam. Lists or Numpy arrays can be used for fixities.
"""
pin   = np.array([1, 1, 0])
beam.setFixity(Loffset, pin)
beam.setFixity(L - Loffset, pin)

"""
Define the beam nodes loads
"""
q = np.array([0.,-1*kN])
beam.addVerticalLoad(0, -5*kN)
beam.addVerticalLoad(L *0.7, -5*kN)
beam.addVerticalLoad(L, -5*kN)
beam.addDistLoad(0, L, q) 
ps.plotBeamDiagram(beam)

"""
Run the analysis
"""
analysis = ps.OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()

"""
Plot results
"""
ps.plotDisp(beam, scale=1000, yunit = 'mm')
ps.plotRotation(beam, scale=1000, yunit = 'mrad')

ps.plotVertDisp(beam)
