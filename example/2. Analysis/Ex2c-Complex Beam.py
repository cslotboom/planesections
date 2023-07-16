"""
An example with lots of forces.
"""
import planesections as ps
from planesections.units.metric import m, kN
import numpy as np

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

beam.addMoment(3, M)

beam.addDistLoad(0, 3, q) 
beam.addDistLoad(0.2,0.5, q*2) 
beam.addDistLoad(0.5,3, q*4) 
beam.addDistLoad(4, 4.8, -q*4) 
beam.addDistLoad(3.2, 4.8, q*2) 

ps.plotBeamDiagram(beam)

analysis = ps.OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()
ps.plotShear(beam, scale = 1/kN, yunit = 'kN')
ps.plotMoment(beam, scale = -1/kN, yunit = 'kNm')

