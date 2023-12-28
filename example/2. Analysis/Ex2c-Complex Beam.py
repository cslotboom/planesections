"""
An example with lots of forces.
"""
import planesections as ps
from planesections.units.metric import m, kN
import numpy as np

"""
When creating a new beam, the dimension can be set to '3D' using the 
dimension attribute.
"""
L = 5*m
x = np.linspace(0,L,80)
beam = ps.EulerBeam(x)

"""
Define the node fixities. The fixity is a list for each DOF, where 1 represents
fixed, and 0 represents free in this case two pin constraints are applied to the
beam. Here we use fixity objects, but we could use lists instead.
"""
pinned = ps.FixityTypes2D.getPinned() # could replace with [1,1,0]
fixed  = ps.FixityTypes2D.getFixed()
beam.setFixity(0.4, pinned, label = 'A')
beam.setFixity(L, fixed, label = 'B')

"""
Define the beam loads. Note that forces will get their own lables seperate from
Nodes. If we want force labels to also be assigned to nodes, you have can set 
the flag "labelNode" to True.
"""
P = -2*kN
M = 5*kN*m
q = np.array([0.,-kN/m])
beam.addVerticalLoad(0, P,label = 'C', labelNode=True) 
beam.addVerticalLoad(2.5, P,label = 'D')
beam.addVerticalLoad(4, -P,label = 'E')

beam.addMoment(3, M)

beam.addDistLoad(0, 3, q) 
beam.addDistLoad(0.2,0.5, q*2) 
beam.addDistLoad(0.5,3, q*4) 
beam.addDistLoad(4, 4.8, -q*4) 
beam.addDistLoad(3.2, 4.8, q*2) 

"""
Create the beam diagram 
"""
ps.plotBeamDiagram(beam)

"""
Run the Analysis
"""
analysis = ps.PyNiteAnalyzer2D(beam)
analysis.runAnalysis()
ps.plotShear(beam, scale = 1/kN, yunit = 'kN')
ps.plotMoment(beam, scale = -1/kN, yunit = 'kNm')

