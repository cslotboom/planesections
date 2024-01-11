.. Hysteresis documentation master file, created by
   sphinx-quickstart on Thu Dec 31 18:57:31 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PlaneSections Documentation
======================================
PlaneSections is a lightweight finite element beam bending library built on libraries like `PyNite <https://github.com/JWock82/PyNite>`_ or `OpenSeesPy <https://github.com/zhuminjie/OpenSeesPy>`_.
The goal of PlaneSections is to quickly run beam anayses, and create outputs to document structural calculations.
**Note, results are only stored at nodes specified by the user - all intermediate values in plots are linearly interpolated**

The following website documents all classes and functions the user can access in PlaneSections.
The core of the program is the beam class in the builder module. This classes will encapuslate all of the contains all information for loading serve as interfaces for class is the beam, 
and the user interacts with this class to run their analysis.

The Builder module is used to create the beam and objects that interact with the beam (nodes, loads, etc.).
The Analysis module is used to analyze the beam using PyNite or OpenSeesPy and document the results.
The Diagram module is used to plot representations of the beam.
The Postprocess module is used to plot outputs of the analysis, including force diagrams and deflections

Note that the core classes and API are complete, but development is still in progress. Expect some sytax changes before final release, however deprication warnings
will be given for breaking changes.

Install using:

.. code :: python

	pip -m install planesections

Install with optional dependancies for opensees solver using:

.. code :: python

	pip -m install planesections[opensees]	


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
	analysis = ps.PyNiteAnalyzer2D(beam)
	analysis.runAnalysis()

	# Plot the SFD and BMD
	ps.plotShear(beam)
	ps.plotMoment(beam)


.. toctree::
   :maxdepth: 3
   :numbered:
   
   rst/builder
   rst/analysis
   rst/diagram
   rst/environment
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
