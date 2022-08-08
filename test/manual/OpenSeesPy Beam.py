# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 16:21:12 2022

@author: Christian
"""

import openseespy.opensees as ops
import openseespyhint as op

op.utility.wipe()
op.model.basic(3)

nCrds1 = [0.,0.,0.]
nCrds2 = [0.,0.,1.]

op.model.node(1, nCrds1)
op.model.node(2, nCrds2)

# op.model.

