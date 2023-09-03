# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 00:06:19 2023

@author: Christian
"""

import openseespy.opensees as op
import numpy as np
L = 5

op.wipe()
op.model('Basic' , '-ndm',  2)
op.geomTransf('Linear', 1)

op.node(1, 0., 0.)
op.node(2, L, 0.)
op.fix(1, 1, 1, 0)
op.fix(2, 1, 1, 0)

matPropreties = [1.,200*10**9,1.]
op.element('elasticBeamColumn',  1 , 1, 2 , *matPropreties, 1)

op.timeSeries('Linear',1)
op.pattern('Plain', 1, 1)

op.constraints("Lagrange")
op.numberer("Plain")
op.system('BandGeneral')
op.test('NormDispIncr',  1.*10**-8, 40, 0 , 2)
# op.algorithm('Newton')
op.algorithm('Linear')
op.integrator('LoadControl',1.)
op.analysis('Static')

op.eleLoad('-ele', 1, '-type', '-beamUniform', 1, 0)
# ops.eleLoad('-ele',eleTag,'-type','beamUniform',wya,wxa,aOverL,bOverL,wyb,wxb)
op.eleLoad('-ele', 1,'-type','beamUniform', 1., 0., 0.,1.,0., 0.)


ok = op.analyze(1)
op.reactions()


def getEleInteralForce( nodID:int):
    """
    Gets the internal force at the left and right side of a node.
    The left and right side forces represent internal force at either side
    of a section cut.       
    
    """
    ndf = 3
    Fint = np.zeros(ndf*2)
    if nodID == 1: # Left most node
        eleR = nodID      
        # 0 is used to so that the plot "closes", i.e. starts at zero the goes up
        Fint[:ndf] =  0                                   # Left side forces
        Fint[ndf:] =  op.eleForce(eleR)[:ndf]             # Right side forces
        
    #Direct Check, this is scary.
    elif nodID == 2: # right side node
        eleL = nodID - 1
        Fint[:ndf] = -np.array(op.eleForce(eleL)[ndf:]) # Right side forces
        Fint[ndf:] = 0                               # Left side forces
    else: # center nodes
        eleL = nodID - 1
        eleR = nodID      

        Fint[:ndf] = -np.array(op.eleForce(eleL)[ndf:]) # left entries
        Fint[ndf:] =  np.array(op.eleForce(eleR)[:ndf]) # right entries
    
    return Fint


for ii, node in enumerate([1,2]):
    ID = node            
    disps = np.array(op.nodeDisp(ID))
    rFrc  = np.array(op.nodeReaction(ID))
    Fint  = getEleInteralForce(ID)

print(rFrc)