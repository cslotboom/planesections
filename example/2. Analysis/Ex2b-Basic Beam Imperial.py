"""
The following is a more realist example that uses user defined section 
propreties for the beam. Units are in imperial.

"""

import planesections as ps
import numpy as np

"""
Start by defining the units for the problem, the outputs need to be in a consistent
unit base for FEM. In this case, lb and ft are used.
"""
psf = 1
psi = 144*psf
ksi = 1000*psi
ft = 1
inch = ft / 12
kip = 1000

"""
Define the material properties then make the rectangular section.
"""
E = 1305*ksi
d = 12*inch
w = 10*inch
section = ps.SectionRectangle(E, d, w)

"""
Define the beam. In this example we will define the node coordinants directly,
then add those to the beam. By manually defining the node coordinants, it 
is possible to place them anywhere in the beam desired.
"""
L = 30*ft
Loffset = 1.5*ft
x       = np.linspace(0, L, 80)
beam = ps.EulerBeam(section = section)
beam.addNodes(x)

"""
Define the node fixities. The fixity is a list for each DOF, where 1 represents
fixed, and 0 represents free in this case two pin constraints are applied to the
beam. Lists or Numpy arrays can be used for fixities.
"""
fixed = np.array([1, 1, 0])
beam.setFixity(Loffset, fixed)
beam.setFixity(L - Loffset, fixed)

"""
Define the beam nodes loads
"""
q = np.array([0.,-1*kip/ft])
beam.addVerticalLoad(0, -5*kip)
beam.addVerticalLoad(L *0.7, -5*kip)
beam.addVerticalLoad(L, -5*kip)
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
ps.plotDisp(beam, scale=1/inch, yunit = 'in', xunit = 'ft')


