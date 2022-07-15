"""
The diagram unit manager can be used to set the 

"""

import planesections as ps
import numpy as np

"""
Start by defining the units for the problem, the outputs need to be in a consistent
unit base for FEM.
"""
from planesections.units.metric import m, mm, kN, GPa


L = 10*m
P = -1.*kN
beam = ps.newSimpleEulerBeam2D(L)
beam.addVerticalLoad(L/2, P, 'A')
beam.addVerticalLoad(L/3, P/2, 'B')
beam.addMoment(2*L/3, P/2, 'C')

ps.plotBeamDiagram(beam, plotLabel=True, labelForce=False)





