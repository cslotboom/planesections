# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian


Showcases two linear loads plotted on top of eachother.

"""

import planesections as ps
from planesections.units.metric import m, kN
import numpy as np

x = np.array([0,5])
labels = ['A', 'B']

L       = 5*m
x       = np.linspace(0, L, 80)
beam    = ps.EulerBeam(x)

pinned = ps.FixityTypes2D.getPinned()
beam.setFixity(0, pinned, label = 'A')
beam.setFixity(L/2, pinned, label = 'B')
beam.setFixity(L, pinned, label = 'C')

P = -2*kN
M = 5*kN*m
q = np.array([0., kN/m])

beam.addLinLoadVertical(0, 4.5, -q)
beam.addLinLoadVertical(0, 5, -q[::-1]*2)

import time
t1 = time.time()
ps.plotBeamDiagram(beam)
t2 = time.time()

print(t2-t1)