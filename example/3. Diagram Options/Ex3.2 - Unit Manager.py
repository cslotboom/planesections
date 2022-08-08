"""
The following example shows some of the options for plotting forces.
First a basic beam is defined and loads are applied ot it.

"""

import planesections as ps
import numpy as np
from planesections.units.metric import m, mm, kN, GPa


L = 10*m
P = -5.*kN
beam = ps.newSimpleEulerBeam(L)
beam.addVerticalLoad(L/2, P, 'A')
beam.addVerticalLoad(L/3, P/2.5, 'B')
beam.addVerticalLoad(L/6, P/5, 'C')
beam.addMoment(2*L/3, P/2, 'C')


"""
The units on the forces can be changed by passing in the desired units, or 
changing the global unit environment.
Note that the diagram is incorrect if we were to do this - the unit handler only
changes the diagram units!
"""

ps.diagramUnits.setActiveEnvironment('imperial_ftkip')
ps.diagramUnits.modifyActiveEnvironment('force', [{'unit':'kip', 'scale':0.001, 'Ndecimal':2}])
ps.plotBeamDiagram(beam, plotLabel=True, labelForce=True, plotForceValue=True)

"""
The units can also be managed by selecting the appropriate unit type in the plot function
"""
# ps.plotBeamDiagram(beam, plotLabel=True, labelForce=True, plotForceValue=True, units='imperial_ftlb')
