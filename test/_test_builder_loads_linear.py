# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian
"""


import planesections as ps
# import planesections as ps
import numpy as np
# import pytest

x1 = 0
x2 = 4
Lnet = x2-x1
distLoad = [0,1]
linearLoad = ps.EleLoadLinear(x1, x2, distLoad)


def test_Linear_load_bar():
    distLoad = [12, 0]
    linearLoad = ps.EleLoadLinear(x1, x2, distLoad)
    [P1, _, _], [P2, _, _] = linearLoad.getLinearEquivLoad(0, 1)
    
    assert P1 == 0.5
    assert P2 == 1
 
def test_Linear_load_bar_reversed():
    distLoad = [12, 0]
    linearLoad = ps.EleLoadLinear(x1, x2, distLoad, isrightHigh=False)
    [P1, _, _], [P2, _, _] = linearLoad.getLinearEquivLoad(0, 1)
    
    assert P1 == 4.5 + 1
    assert P2 == 4.5 + 0.5

def test_Linear_load_bar_offset():
    distLoad = [12, 0]
    linearLoad = ps.EleLoadLinear(1, 5, distLoad)
    [P1, _, _], [P2, _, _] = linearLoad.getLinearEquivLoad(1, 2)
    
    assert P1 == 0.5
    assert P2 == 1
  
def test_Linear_load_bar_reversed_offset():
    distLoad = [12, 0]
    linearLoad = ps.EleLoadLinear(1, 5, distLoad, isrightHigh=False)
    [P1, _, _], [P2, _, _] = linearLoad.getLinearEquivLoad(1, 2)
    
    assert P1 == 4.5 + 1
    assert P2 == 4.5 + 0.5
 
    
 

def test_Linear_load_beam():
    q = 20
    L = 1
    distLoad = [0, q]
    linearLoad = ps.EleLoadLinear(x1, x2, distLoad)
    [_, V1, M1], [_, V2, M2] = linearLoad.getLinearEquivLoad(0, L)
    
    assert (V1 == 3*(q/Lnet)*L / 20) and (V2 == 7*(q/Lnet)*L / 20)
    assert (M1 == (q/Lnet)*L**2 / 30) and (M2 == -(q/Lnet)*L**2 / 20)
 
def test_Linear_load_beam_reversed():
    q = 20
    L = 1
    distLoad = [0, q]
    linearLoad = ps.EleLoadLinear(x1, x2, distLoad, isrightHigh=False)
    [_, V1, M1], [_, V2, M2] = linearLoad.getLinearEquivLoad(0, 1)
    
    
    v1sol = 7*(q/Lnet)*L / 20 + (q*0.75)*L/2
    v2sol = 3*(q/Lnet)*L / 20 + (q*0.75)*L/2
    
    M1sol = -(q/Lnet)*L**2 / 20 - (q*0.75)*L**2 / 12
    M2sol = (q/Lnet)*L**2 / 30 + (q*0.75)*L**2 / 12
    
    
    assert (V1 == v1sol) and (V2 == v2sol)
    assert (M1 == M1sol) and (M2 == M2sol)
    # assert (M1 == 0.5) and (M2 == 1)

def test_Linear_load_beam_offset():
    q = 20
    L = 1
    distLoad = [0, q]
    linearLoad = ps.EleLoadLinear(1, 5, distLoad)
    [_, V1, M1], [_, V2, M2] = linearLoad.getLinearEquivLoad(1, 2)
    
    assert (V1 == 3*(q/Lnet)*L / 20) and (V2 == 7*(q/Lnet)*L / 20)
    assert (M1 == (q/Lnet)*L**2 / 30) and (M2 == -(q/Lnet)*L**2 / 20)





def test_Linear_load_beam_reversed_offset():
    q = 20
    L = 1
    distLoad = [0, q]
    linearLoad = ps.EleLoadLinear(1, 5, distLoad, isrightHigh=False)
    [_, V1, M1], [_, V2, M2] = linearLoad.getLinearEquivLoad(1, 2)
    
    
    v1sol = 7*(q/Lnet)*L / 20 + (q*0.75)*L/2
    v2sol = 3*(q/Lnet)*L / 20 + (q*0.75)*L/2
    
    M1sol = -(q/Lnet)*L**2 / 20 - (q*0.75)*L**2 / 12
    M2sol = (q/Lnet)*L**2 / 30 + (q*0.75)*L**2 / 12
    
    
    assert (V1 == v1sol) and (V2 == v2sol)
    assert (M1 == M1sol) and (M2 == M2sol)
 

if __name__ == '__main__':   
    test_Linear_load_bar()
    test_Linear_load_bar_offset()
    test_Linear_load_bar_reversed()
    test_Linear_load_bar_reversed_offset()
    
    test_Linear_load_beam()
    test_Linear_load_beam_reversed()
    test_Linear_load_beam_offset()
    test_Linear_load_beam_reversed_offset()

