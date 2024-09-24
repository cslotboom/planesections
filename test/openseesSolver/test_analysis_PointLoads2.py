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
section = ps.SectionRectangle(E, h, b, units='mm')
I = section.Iz

L = 3
x1 = 0
x2 = L
x3 = x2 * (2 / 3)

Py = -5000
x = np.linspace(0, x2, 100)
fixed = np.array([1, 1, 1])
pinned = np.array([1, 1, 0])

beam = ps.EulerBeam(x, section = section)
beam.setFixity(x1, fixed)
beam.setFixity(x2, pinned)
beam.addVerticalLoad(x3, Py)

# ps.plotBeamDiagram(beam)

analysis = ps.OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()

R = beam.reactions

R1y = R[0][1]
R2y = R[1][1]

analysis.beam


def test_Mmax():
    # pass
    tol = 0.0001
    MAsolution = abs(4*x2*Py / 27)
    MA = R[0][2]
    MA = abs(MA)
    
    assert(abs(MAsolution - MA) < tol)

def test_maxDisp():
    tolPercent = 0.002

    xmaxSol = 8*L / 13
    dispMaxSol = 128*L**3*Py / (13689*E*I)

    disp, x = ps.getVertDisp(beam)


    dispMax, xmax = ps.getMaxVertDisp(beam)
    
    check1 = abs(dispMax / dispMaxSol) - 1 < tolPercent
    check2 = abs(xmax / xmaxSol) - 1 < tolPercent
    assert (check1 and check2)


if __name__ == "__main__":
    test_Mmax()
    test_maxDisp()

# test_maxDisp()
    
    
# xmax = ps.getMaxVertDisp(beam)
