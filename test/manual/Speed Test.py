"""
An example with lots of forces.
"""
import planesections as ps
from planesections.units.metric import m, kN
import numpy as np
from time import time


# =============================================================================
# setup
# =============================================================================
L = 5*m
x = np.linspace(0,L,80)
beam = ps.EulerBeam(x)

pinned = ps.FixityTypes2D.getPinned()
fixed  = ps.FixityTypes2D.getFixed()

beam.setFixity(0.4, pinned, label = 'A')
beam.setFixity(L, fixed, label = 'B')

P = -2*kN
M = 5*kN*m
q = np.array([0.,-kN/m])
beam.addVerticalLoad(0, P,label = 'C')
beam.addVerticalLoad(2.5, P,label = 'D')
beam.addVerticalLoad(4, -P,label = 'E')

beam.addMoment(3, M, label = 'F')

beam.addDistLoad(0, 3, q) 

ps.plotBeamDiagram(beam, labelForce=True)

# =============================================================================
# Testing
# =============================================================================

Ntrial = 100
t1 = time()
for ii in range(Ntrial):
    analysis = ps.OpenSeesAnalyzer2D(beam)
    analysis.runAnalysis()

t2 = time()
for ii in range(Ntrial):
    analysis = ps.PyNiteAnalyzer2D(beam)
    analysis.runAnalysis()

t3 = time()

dt_OpenSees = round(t2 - t1,3)
dt_Pynite   = round(t3 - t2,3)

print(f"OpenSees takes {dt_OpenSees}, s")
print(f"Pynite takes {dt_Pynite}, s")

