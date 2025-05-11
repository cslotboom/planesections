"""
The following is a basic demo of how planesections works
A simply supported beam is created, a diagram of it is made, then the beam is
and analyzed and results are output
"""
import planesections as ps
from planesections.units.metric import kN, m

# Initialize the beam
beam = ps.newSimpleEulerBeam(5*m, q=-2*kN/m)

# Run the analysis
analysis = ps.OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()

ps.plotBeamDiagram(beam)

# Plot the SFD and BMD
ps.plotShear(beam, scale = 0.001, yunit = 'kN')
ps.plotMoment(beam, scale = 0.001, yunit = 'kNm')