# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian
Manually used to check if loads are stacking properly!
"""



import planesections as ps
from planesections.units.metric import m, kN
import numpy as np
# import pytest

x = np.array([0,5])
labels = ['A', 'B']
fixities = [np.array([1,1,1]), np.array([1,1,1])]

L       = 5*m
x       = np.linspace(0, L, 80)
beam    = ps.EulerBeam(x)

pinned = [1,1,0]
fixed = [1,1,1]
beam.setFixity(0.4, pinned, label = 'A')
beam.setFixity(L, fixed, label = 'B')

P = -2*kN
M = 5*kN*m
q = np.array([0.,kN/m])
beam.addVerticalLoad(0, P, label = 'C')
beam.addVerticalLoad(2.5, P, label = 'D')
beam.addVerticalLoad(4, -P, label = 'E')

beam.addMoment(3, M)
beam.addDistLoad(0, 3, -q) 
beam.addDistLoad(0, 2, -q) 
beam.addDistLoad(0.2,1, q*2)

beam.addDistLoad(2.8,3.5, q)

beam.addLinLoadVertical(3, 4.5, q[1]*2, isRightHigh=False)
beam.addLinLoadVertical(3, 4.5, q[1]*2, isRightHigh=True)

ps.plotBeamDiagram(beam)

