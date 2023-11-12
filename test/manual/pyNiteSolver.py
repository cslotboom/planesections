# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 21:14:01 2023

@author: Christian
"""


import planesections as ps
import numpy as np
from planesections.units.metric import m, mm, kN, GPa

E = 9*GPa
d = 300*mm
w = 265*mm
section = ps.SectionRectangle(E, d, w)

def getBeam():
    L = 10*m
    Loffset = 0.5*m
    beam = ps.EulerBeam(section = section)
    x       = np.linspace(0, L, 80)
    beam.addNodes(x)
    
    pin   = ps.FixityTypes2D.getPinned()
    beam.setFixity(Loffset, pin)
    beam.setFixity(L - Loffset, pin)
    
    q = np.array([0.,-1*kN])
    beam.addVerticalLoad(0, -5*kN)
    beam.addVerticalLoad(L *0.7, -5*kN)
    beam.addVerticalLoad(L, -5*kN)
    beam.addDistLoad(0, L, q) 
    beam.addLinLoad(0, L, q)
    ps.plotBeamDiagram(beam)
    return beam

beamOps = getBeam()

analysis = ps.OpenSeesAnalyzer2D(beamOps)
analysis.runAnalysis()

# ps.plotDisp(beam, scale=1000, yunit = 'mm')
# ps.plotRotation(beam, scale=1000, yunit = 'mrad')

# ps.plotVertDisp(beam)

beamPyNite = getBeam()

pyNiteAnalysis = ps.PyNiteAnalyzer2D(beamPyNite)
pyNiteAnalysis.runAnalysis()

ps.plotMoment(beamOps)
ps.plotMoment(beamPyNite)

ps.plotShear(beamOps)
ps.plotShear(beamPyNite)



analysisBeam = pyNiteAnalysis._getBeam()
ele = analysisBeam.Members['M1']


mysum = 0
for key in analysisBeam.Nodes.keys():
    node = analysisBeam.Nodes[key]
    
    if node.RxnFY['Combo 1']:
        mysum += node.RxnFY['Combo 1']

for key in analysisBeam.Members.keys():
    ele = analysisBeam.Members[key]
    ele.axial_array(2)[1]
    ele.shear_array('Fy',2)[1]
    # ele.moment_array(Direction, n_points)
    ele.shear_array('Fz',2)
    
    # print()
    
    # ele.shear('Fy', 5, '1.2D+1.6S')
    # print(node.X)
    # print(node.NodeLoads)
    # print(node.RxnFY)
    # print()


# for key in analysisBeam.Nodes.keys():
#     print(analysisBeam.Nodes[key].RxnFY)
# print(np.sum(beamOps.reactions))
# print(np.sum(mysum))




# Print reactions at each end of the beam
# print('Left Support Reaction:', analysisBeam.Nodes['N1'].RxnFY, 'kip')



# # Example of a simply supported beam with a uniform distributed load.
# # Units used in this example are inches and kips
# # This example does not use load combinations. The program will create a default load combindation called 'Combo 1'

# # Import `FEModel3D` from `PyNite`
# from PyNite import FEModel3D

# # Create a new finite element model
# analysisBeam = FEModel3D()

# nodeAnalysisNames = []
# for ii, node in enumerate(beam.nodes):
#     name = 'N' + str(node.ID)
#     nodeAnalysisNames.append(name)
#     analysisBeam.add_node(name, node.x, 0, 0)
#     if node.hasReaction:
#         f1, f2, f3 = node.fixity.fixityValues
#         print(node.fixity.fixityValues)
#         analysisBeam.def_support(name, f1, f2, True, True, False, f3)
  
# # Define a material
# E = 29000       # Modulus of elasticity (ksi)
# G = 11200       # Shear modulus of elasticity (ksi)
# nu = 0.3        # Poisson's ratio
# rho = 2.836e-4  # Density (kci)
# matName = 'baseMat'
# analysisBeam.add_material(matName, E, G, nu, rho)

# memberNames = []
# for ii in range(len(nodeAnalysisNames)-1):
#     memberName = 'M' + str(ii)
#     N1 = nodeAnalysisNames[ii]
#     N2 = nodeAnalysisNames[ii+1]
#     # Add a beam with the following properties:
#     # Iy = 100 in^4, Iz = 150 in^4, J = 250 in^4, A = 20 in^2
#     # print(N1, N2)
#     analysisBeam.add_member(memberName, N1, N2, matName, 100, 150, 250, 20)
#     memberNames.append(memberName)
# # Provide simple supports

        
# for eleload in beam.eleLoads:
#     N1 = beam._findNode(eleload.x1) + 1
#     N2 = beam._findNode(eleload.x2) + 1

#     load = eleload.P
#     for ii in range(N1, N2-1):
#         # print(memberNames[ii])
#         # print(nodeAnalysisNames[ii], nodeAnalysisNames[ii])
        
#         analysisBeam.add_member_dist_load(memberNames[ii], 'Fy', q[1], q[1])






# Analyze the beam
# analysisBeam.analyze()

# Print the shear, moment, and deflection diagrams
# analysisBeam.Members['M1'].plot_shear('Fy')
# analysisBeam.Members['M1'].plot_moment('Mz')
# analysisBeam.Members['M1'].plot_deflection('dy')


# print('Right Support Reacton:', analysisBeam.Nodes['N2'].RxnFY, 'kip')

# Render the deformed shape of the beam magnified 100 times, with a text height of 5 inches
# from PyNite.Visualization import Renderer
# renderer = Renderer(analysisBeam)
# renderer.annotation_size = 6
# renderer.deformed_shape = True
# renderer.deformed_scale = 100
# renderer.render_loads = True
# renderer.render_model()





