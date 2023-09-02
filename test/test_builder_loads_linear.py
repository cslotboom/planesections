# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian

These test if linear loads are being applied properly.

"""

import planesections as ps
import numpy as np

x1 = 0
x2 = 4
q = 1
beam = ps.newEulerBeam(x2)

Lnet = x2-x1
distLoad = [0,q]

beam.addLinLoadVertical(x1, x2, q)
beam.addLinLoadHorizontal(x1, x2, q)


def test_addition():
    assert len(beam.eleLoads) == 2
    
def test_parameter_retreval():
    s1, s2 = beam.eleLoads[0].getLoadComponents(1,3, q)
    assert s1 == 0.25 and s2 == 0.75
    
if __name__ == "__main__":
    test_addition()
    test_parameter_retreval()