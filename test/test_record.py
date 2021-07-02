# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian
"""

from planesections import EulerBeam, OpenSeesAnalyzer, RecordOutput
# from planesections import EulerBeam
import numpy as np

import openseespy.opensees as op

x = np.array([0,5])
fixities = [np.array([1,1,1], int), np.array([1,1,1], int)]
