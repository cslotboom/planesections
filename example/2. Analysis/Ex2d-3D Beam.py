"""
A simple example using a 3D beam instead of a 2D beam.
3D beams can have shear forces applied in and out of the page, in addition
to the vertical forces. They also have torsion moments and "weak axis" moments.

"""
import planesections as ps
from planesections.units.metric import m, kN
import numpy as np

"""
When creating a new beam, the dimension can be set to '3D' using the 
dimension attribute.
"""
L = 5*m
beam = ps.newEulerBeam(L, dimension='3D')

"""
Fixities work the same as a 2D beam, except there is now 6DOF! The first three
are translation (ux, uy, uz). The next three are rotation (rx, ry, rz).

If we leave the rx and ry dof free, the beam will actually be unstable - 
that's no good!
"""
pinned = [1,1,1,1,1,0]
beam.setFixity(0.4, pinned, label = 'A')
beam.setFixity(L, pinned, label = 'E')

"""
Similarly, loads work the same, but with 6DOF. The loads are [Fx, Fy, Fz, Mx, My, Mz],
The moments are the moment about the axis in question, i.e. Mz is the moment around
the z axis. The coordinate system has y as "up", and z as out of the page.

Note that "addVertical" and "addMoment" both still work. The moment added will
be in the strong axis, i.e. Mz
 
    y
    ┃
    ┃____x
   ╱
  ╱
 z
 
"""

P = -2*kN
M = 5*kN*m
torsionMoment = [0, 0, 0, 2.5*kN*m, 0, 0]
beam.addVerticalLoad(0, P,label = 'B')
beam.addMoment(2.5, M, label = 'C')
beam.addPointLoad(L/3, torsionMoment, label = 'D')

"""
In the analysis, a 3D needs to be added now.
"""
analysis = ps.OpenSeesAnalyzer3D(beam)
analysis.runAnalysis()

"""
The plotting functions work similarly. To get the torsion, we need to include

"""
ps.plotShear(beam, scale = 1/kN, yunit = 'kN')
ps.plotMoment(beam, scale = -1/kN, yunit = 'kNm')
ps.plotInternalForce(beam, 3, scale = 1/kN, yunit = 'kNm')

