# -*- coding: utf-8 -*-
"""
Created on Sun May 23 01:00:41 2021

@author: Christian


This section tests whether linearly distributed loads are correctly implemented
by comparing outputs to known results of simple beam equations.



"""
import pytest
import planesections as ps
import numpy as np

x1 = 0
x2 = 5
q = -8000
fixed = np.array([1, 1, 0.])
qin = [0.,-8000.]


x3 = 0
x4 = 5  
beam = ps.newTimoshenkoBeam(x2, meshSize=51)   
beam.addDistLoad(x1, x2, qin)

beam.setFixity(x1, fixed)
beam.setFixity(x2, fixed)

analysis = ps.OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()


def test_LinearLoad_Failure():
    with pytest.raises(Exception) as e_info:
        _, _ = beam.addLinLoad(x1, x2, qin)
    


def test_Fnet():
    R1, R2 = beam.reactions
    y = (R1+R2)[1]
    assert abs(y + x4*qin[1]) < 0.0001

def test_Mmax():
    Mmin, Mmax = beam.Mmax

    tol = 0.0001
    check2 = abs(Mmax - 0) < tol
    check1 = abs(Mmin - (qin[1]*x4**2/8))/abs(Mmin) -1 < tol
    
    assert(np.all([check1,check2]))

def test_Vmax():
    tol = 0.0001
    Vmin, Vmax = beam.Vmax

    check1 = abs(Vmin - x4*qin[1]/2) < tol
    check2 = abs(Vmax + x4*qin[1]/2) < tol
    
    assert(np.all([check1,check2]))


def test_u():
    u, _ = ps.getMaxVertDisp(beam)
    # Vmin, Vmax = beam.Vmax

    uSol = (5/384)*q*x4**4 + (1/8)*q*x4**2
    assert u == pytest.approx(uSol)
    # check1 = abs(uSol - u)/uSol < 1e-3
    # check2 = abs(Vmax + x4*qin[1]/2) < tol
    
    # assert check1



if __name__ == "__main__":
    test_LinearLoad_Failure()
    test_Fnet()
    test_Vmax()
    test_Mmax()
    test_u()