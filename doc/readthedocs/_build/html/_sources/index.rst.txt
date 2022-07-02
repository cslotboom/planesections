.. Hysteresis documentation master file, created by
   sphinx-quickstart on Thu Dec 31 18:57:31 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Hysteresis Documentation
======================================
Hysteresis is a library of tools for non-functional curves, with a emphasis on force-deformation hysteresis curves.

Install using:

.. code :: python

	pip install hysteresis

A simple script is shown below:

.. code :: python

	# import numpy and hysteresis
	import numpy as np
	import hysteresis as hys

	# Create a simple non-functional curve
	t = np.linspace(0,4,1000)*np.pi
	x = np.sin(t)
	y = np.cos(t)*t
	xy = np.column_stack([x,y])

	# Create a hysteresis object and 
	myHys = hys.Hysteresis(xy)
	myHys.plot(plotCycles = True)


.. toctree::
   :maxdepth: 3
   :numbered:
   
   rst/baseClass
   rst/basicFunctions
   rst/defaultFunctions
   rst/protocol
   rst/climate
   rst/examples

=============
 Developed by
=============

*Christian Slotboom* `<https://github.com/cslotboom/Hysteresis>`_.

| M.A.Sc. Structural Engineering
| Engineer in Training 

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
