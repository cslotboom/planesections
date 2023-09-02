# -*- coding: utf-8 -*-
"""
Created on Sun May 23 01:00:41 2021

@author: Christian


This section tests whether linearly distributed loads are correctly implemented
by comparing outputs to known results of simple beam equations.



"""

import planesections as ps
import numpy as np

x1 = 0
x2 = 5
q = -8000
fixed = np.array([1, 1, 0.])
q = np.array([0., -8000.])

x3 = 0
x4 = 5  
beam = ps.newEulerBeam(x2, meshSize=51)   
beam.addLinLoad(x1, x2, q, isRightHigh=False)

beam.setFixity(x1, fixed)
beam.setFixity(x2, fixed)

analysis = ps.OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()

def test_Fnet():
    R1, R2 = beam.reactions
    y = (R1+R2)[1]
    assert abs(y + x4*q[1]/2) < 0.0001

def test_Mmax():
    Mmin, Mmax = beam.Mmax

    tol = 0.0001
    check2 = abs(Mmax - 0) < tol
    check1 = abs(Mmin - (q[1]*(x4-x3)**2/(9*3**0.5)))/abs(Mmin) -1 < tol
    
    assert(np.all([check1,check2]))

def test_Vmax():
    tol = 0.0001
    Vmin, Vmax = beam.Vmax

    check1 = abs(Vmin - q[1]*x2/6) < tol
    check2 = abs(Vmax + q[1]*x2/3) < tol
    
    assert(np.all([check1,check2]))

def test_reactions():
    R1, R2 = beam.reactions

def test_reversed():
    beam = ps.newEulerBeam(x2, meshSize=51)   
    beam.addLinLoad(x1, x2, q)

    beam.setFixity(x1, fixed)
    beam.setFixity(x2, fixed)

    analysis = ps.OpenSeesAnalyzer2D(beam)
    analysis.runAnalysis()

    tol = 0.001
    R1, R2 = beam.reactions
    y1 =  R1[1]
    y2 =  R2[1]

    # We add because of the sign change, i.e. minus negative
    assert( abs(y1 + q[1]*x4/6) / abs(y1) - 1 < tol)
    assert( abs(y2 + q[1]*x4/3) / abs(y2) - 1< tol)



def test_FEM():
    """
    Tests results against results from a commercial FEM software suite.
    """
    x1 = 0
    x2 = 5
    q = -8000
    fixed = np.array([1, 1, 0.])
    q = np.array([0., -8000.])
    beam = ps.newEulerBeam(x2, meshSize=51)   


    x3 = 1
    x4 = 3  
    beam.addLinLoad(x3, x4, q, isRightHigh=False)

    beam.setFixity(x1, fixed)
    beam.setFixity(x2, fixed)

    analysis = ps.OpenSeesAnalyzer2D(beam)
    analysis.runAnalysis()
    
    Mmin, Mmax = beam.Mmax
    Vmin, Vmax = beam.Vmax

    # Tests total reaction
    R1, R2 = beam.reactions
    y = (R1+R2)[1]
    assert abs(y + (x4-x3)*q[1]/2) / abs(y)  < 0.0001
    

if __name__ == "__main__":
    test_Fnet()
    test_Vmax()
    test_Mmax()
    
    test_reversed()
    test_FEM()
