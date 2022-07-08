# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian

Tests the point load analyses.
https://civil-terje.sites.olt.ubc.ca/files/2019/06/Fixed-roller-Beam-with-Point-Load.pdf


"""
import planesections as ps
from planesections.units.metric import mm, MPa, N
import numpy as np

E = 9500*MPa
b = 38*mm
h = 235*mm
section = ps.SectionRectangle(E, h, b)
I = section.Ixx

x1 = 0
x2 = 3
x3 = x2 * (2 / 3)

Py = -5000
x = np.linspace(0, x2, 100)
fixed = np.array([1, 1, 1])
pinned = np.array([1, 1, 0])

beam = ps.EulerBeam2D(x, section = section)
beam.setFixity(x1, fixed)
beam.setFixity(x2, pinned)
beam.addVerticalLoad(x3, Py)

ps.plotBeamDiagram(beam)

analysis = ps.OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()

R = beam.reactions

R1y = R[0][1]
R2y = R[1][1]

def test_Mmax():
    # pass
    tol = 0.0001
    MAsolution = abs(4*x2*Py / 27)
    MA = R[0][2]
    MA = abs(MA)
    
    assert(abs(MAsolution - MA) < tol)

# test_Mmax()


# def test_Vmax():
#     tol = 0.0001
#     check1 = abs(Vmin - q[1]/2) < tol
#     check2 = abs(Vmax + q[1]/2) < tol
    
#     assert(np.all([check1,check2]))

    # assert(np.all([check1,check2]))