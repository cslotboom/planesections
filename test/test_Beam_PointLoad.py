# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian
"""

from planesections import EulerBeam2D, OpenSeesAnalyzer2D
import numpy as np

x1 = 0
x2 = 5
x3 = x2/2
q = -8000
x = np.linspace(0, 5, 50)
fixed = np.array([1, 1, 0.])
q = np.array([0., -5000., 0.])


beam = EulerBeam2D(x)
# beam.addNodes(x)
beam.setFixity(x1, fixed)
beam.setFixity(x2, fixed)
beam.addPointLoad(x3, q)

analysis = OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()

Mmin, Mmax = beam.Mmax
Vmin, Vmax = beam.Vmax


def test_Mmax():
    tol = 0.0001
    check2 = abs(Mmax - 0)< tol
    check1 = abs(Mmin - q[1]*x2 / 4) < tol
    
    assert(np.all([check1,check2]))

def test_Vmax():
    tol = 0.0001
    check1 = abs(Vmin - q[1]/2) < tol
    check2 = abs(Vmax + q[1]/2) < tol
    
    assert(np.all([check1,check2]))

    # assert(np.all([check1,check2]))