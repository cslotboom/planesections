"""
The following example shows some of the options for plotting forces.
First a basic beam is defined and loadsare applied ot it.
"""

import planesections as ps
import numpy as np
from planesections.units.metric import m, mm, kN, GPa

L = 10*m
P = -5.*kN
beam = ps.newSimpleEulerBeam2D(L)
beam.addMoment(2*L/3, P/2, 'Am') 
beam.addVerticalLoad(L/2, P, 'B')
beam.addVerticalLoad(L/3, P/2.5)
beam.addVerticalLoad(L/6, P/5, 'C')
beam.addDistLoadVertical(0, L*0.9, P/5, 's')
beam.addNode(L/4, label = 'D') # a point of interst on the beam

"""
The default plotting mode labels the location 
"""
ps.plotBeamDiagram(beam, plotLabel=True)

"""
The forces can also be plotted instead.
"""
ps.plotBeamDiagram(beam, plotLabel=True, labelForce=True)

"""
The values of the force can also be plotted
"""
ps.plotBeamDiagram(beam, plotLabel=True, labelForce=True, plotForceValue=True)
