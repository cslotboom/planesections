"""
The following is a basic demo of how planesections works
A simply supported beam is created, a diagram of it is made, then the beam is
and analyzed and results are output
"""
import planesections as ps

# Define node locations, and support conditions
L = 5
beam = ps.newEulerBeam(L)

# Define beam and fixities
pinned = [1,1,0]
beam.setFixity(L*0.1, pinned, label = 'A')
beam.setFixity(L*0.9, pinned, label = 'B')

# Define point Loads
Pz = -1000
beam.addVerticalLoad(0, Pz, label = 'C')
beam.addVerticalLoad(L*0.5, 2*Pz, label = 'D')
beam.addVerticalLoad(L, Pz, label = 'E')

# Define distributed Loads
beam.addDistLoadVertical(0, L, Pz)
beam.addDistLoadVertical(1, L*0.3, 5*Pz)

# Plot the beam diagram
ps.plotBeamDiagram(beam)

# Run the analysis
analysis = ps.OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()

# Plot the SFD and BMD
ps.plotShear(beam, scale = 0.001, yunit = 'kN',labelPOI=True)
ps.plotMoment(beam, scale = 0.001, yunit = 'kNm',labelPOI=True)