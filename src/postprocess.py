import openseespy.opensees as op
import numpy as np
import matplotlib.pyplot as plt

from planesections.builder import Node2D, Beam2D



def getInternalForces2D(node:Node2D, ind):
    """
    0 = axial force
    1 = shear force
    2 = moment
    """
    
    return node.Fint[[ind,ind+3]]
    



def plotMoment2D(beam:Beam2D, scale=1):
    """
    Plots the internal moment at each node in the beam. Note that internal 
    force is only plotted at nodes.

    Parameters
    ----------
    beam : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    return plotInternalForce2D(beam, 2, scale)
        
def plotShear2D(beam:Beam2D, scale=1):
    return plotInternalForce2D(beam, 1, scale)

def plotInternalForce2D(beam:Beam2D, index, scale=1):
    print('ran')
    xcoords = np.zeros(beam.Nnodes*2)
    force = np.zeros(beam.Nnodes*2)
    for ii, node in enumerate(beam.nodes):
        ind1 = 2*ii
        ind2 = ind1 + 2        
        xcoords[ind1:ind2]       = node.x
        force[ind1:ind2] = getInternalForces2D(node, index)
        
    fig, ax = plt.subplots()
    line = plt.plot(xcoords, force*scale)     
    
    return fig, ax, line
  
         
        
def plotVertDisp2D(beam:Beam2D):
    return plotDisp2D(beam) 


def plotRotation2D(beam:Beam2D):
    return plotDisp2D(beam, 2)

# def plotVertDisp(beam):
#     return plotDisp() 


def plotDisp2D(beam:Beam2D, index=1, scale=1):
    
    
    # Plotbeam....  
    xcoords = np.zeros(beam.Nnodes)
    disp = np.zeros(beam.Nnodes)
    for ii, node in enumerate(beam.nodes):
        xcoords[ii] = node.x
        disp[ii] = node.disps[index]
        # moment[ii] = 
    
    fig, ax = plt.subplots()
    line = plt.plot(xcoords, disp*scale)     
    
    return fig, ax, line   
        















# def plotMoment(beam):
    
#     # Plotbeam....
#     xcoords = np.zeros(beam.Nnodes*2)
#     moment = np.zeros(beam.Nnodes*2)
    
#     plotInd = 2
#     for ii, node in enumerate(beam.nodes):
#         ind1 = 2*ii
#         ind2 = ind1 + 2
#         xcoords[ind1:ind2] = node.x
#         moment[ind1:ind2] = getInternalForces(node, plotInd)
#         # moment[ii] = 
    
#     fig, ax = plt.subplots()
#     line = plt.plot(xcoords, moment, '.')
#     return fig, ax, line
        
        
# def plotShear(beam):
    
#     # Plotbeam....  
#     xcoords = np.zeros(beam.Nnodes*2)
#     moment = np.zeros(beam.Nnodes*2)
    
#     plotInd = 1
#     for ii, node in enumerate(beam.nodes):
#         ind1 = 2*ii
#         ind2 = ind1 + 2
#         xcoords[ind1:ind2] = node.x
#         moment[ind1:ind2] = getInternalForces(node, plotInd)
#         # moment[ii] = 
    
#     fig, ax = plt.subplots()
#     line = plt.plot(xcoords,moment)     
    
#     return fig, ax, line

    
    
    
        
