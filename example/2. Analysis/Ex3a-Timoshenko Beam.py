"""
The following example shows how a timoshenko beam can be defined.


Start by defining the units for the problem, the outputs need to be in a 
consistentunit base for FEM. Define the material properties and use a 'basic 
section' object, which has no geometric information.
"""

import planesections as ps
import numpy as np
from planesections.units.metric import m, mm, N, kN, GPa

EI = 1088*N*mm**2*10**9
GA = 7.3*N*10**6

E = 9*GPa
G = E
Iz = EI / E
Avx = GA / G

section = ps.SectionBasic(E, G, Iz = Iz, Avx = Avx)

"""
Define a Euler and Timoshenko beam, and place nodes / fixities.
"""
L = 4*m
Loffset = 0.0*m
beamTimoshenko  = ps.TimoshenkoBeam(section = section)
beamEuler       = ps.EulerBeam(section = section)

x = np.linspace(0, L, 80)
beamTimoshenko.addNodes(x)
beamEuler.addNodes(x)

pin   = ps.FixityTypes2D.getPinned() # could be replaced with pin = [1,1,0]

beamTimoshenko.setFixity(Loffset, pin)
beamTimoshenko.setFixity(L - Loffset, pin)
beamEuler.setFixity(Loffset, pin)
beamEuler.setFixity(L - Loffset, pin)

"""
Define the beam loads for each beam. Timoshenko beams only support uniformly
distributed loads.
"""
q = np.array([0.,-1*kN])
for beam in [beamTimoshenko, beamEuler]:
    beam.addVerticalLoad(0, -5*kN)
    beam.addVerticalLoad(L *0.7, -5*kN)
    beam.addVerticalLoad(L, -5*kN)
    beam.addDistLoad(0, L, q)

"""
Run the analysis.
"""
analysisTim = ps.OpenSeesAnalyzer2D(beamTimoshenko)
analysisTim.runAnalysis(recordOutput=True)

analysisEul = ps.OpenSeesAnalyzer2D(beamEuler)
analysisEul.runAnalysis(recordOutput=True)


"""
Plot results. By default a scale of 1000 in the y axis is used.
"""
fig, ax, line1 = ps.plotDisp(beamEuler)
_, _, _        = ps.plotDisp(beamTimoshenko, fig = fig, ax=ax)
