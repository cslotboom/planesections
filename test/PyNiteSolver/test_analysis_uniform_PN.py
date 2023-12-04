# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian

Tests if the maximum values are being recorded proprely.
"""

import planesections as ps
import numpy as np

x1 = 0
x2 = 5
q = -8000
x = np.linspace(0, 5, 3)
fixed = np.array([1, 1, 0.])
q = np.array([0., -8000.])


beam = ps.EulerBeam(x)
beam.setFixity(x1, fixed)
beam.setFixity(x2, fixed)
beam.addDistLoad(x1, x2, q)

analysis = ps.PyNiteAnalyzer2D(beam)
analysis.runAnalysis()

Mmin, Mmax = beam.Mmax
Vmin, Vmax = beam.Vmax


def test_Mmax():
    tol = 0.0001
    check2 = abs(Mmax - 0) < tol
    check1 = abs(Mmin - q[1]*x2**2 / 8) < tol
    
    assert(np.all([check1, check2]))

def test_Vmax():
    tol = 0.0001
    check1 = abs(Vmin - q[1]*x2/2) < tol
    check2 = abs(Vmax + q[1]*x2/2) < tol
    
    assert(np.all([check1, check2]))


if __name__ == "__main__":

    test_Mmax()
    test_Vmax()

