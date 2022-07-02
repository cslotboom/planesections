.. Hysteresis documentation master file, created by
   sphinx-quickstart on Thu Dec 31 18:57:31 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PlaneSections Documentation
======================================
PlaneSections is a easy to use beam bending libary.

Install using:

.. code :: python

	pip install planesections

A simple script is shown below:

.. code :: python

	import planesections as ps
	import numpy as np

	# Define node locations, and support conditions
	L = 5
	beam = ps.newEulerBeam2D(L)

	# Define beam and fixities
	pinned = [1,1,0]
	beam.setFixity(L*0.1, pinned, label = '1')
	beam.setFixity(L*0.9, pinned)

	# Define loads
	Pz = -1
	beam.addVerticalLoad(0, Pz, label = 'A')
	beam.addVerticalLoad(L*0.5, 2*Pz, label = 'B')
	beam.addVerticalLoad(L, Pz, label = 'C')
	beam.addDistLoadVertical(0, L, Pz)
	beam.addDistLoadVertical(1, L*0.3, 5*Pz)

	# Plot the beam diagram
	ps.plotBeamDiagram(beam)

	# Run the analysis
	analysis = ps.OpenSeesAnalyzer2D(beam)
	analysis.runAnalysis()

	# Plot the SFD and BMD
	ps.plotShear2D(beam)
	ps.plotMoment2D(beam)


.. toctree::
   :maxdepth: 3
   :numbered:
   
   rst/builder
   rst/analysis
   rst/diagram
   rst/postprocess

=============
 Developed by
=============

*Christian Slotboom* `<https://github.com/cslotboom/planesections>`_.

| M.A.Sc. Structural Engineering
| Engineer in Training 

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
