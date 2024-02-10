# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian

Checks if negative and positive element loads with values on the same side
plot similarly

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
q = np.array([0.2*kN/m, kN/m])

beam.addLinLoadVertical(0, 4.5, -q)
beam.addLinLoadVertical(0, 4.5, q)

ps.plotBeamDiagram(beam)