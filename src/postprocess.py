import openseespy.opensees as op
import numpy as np
import matplotlib.pyplot as plt



def getInternalForces(node, ind):
    """
    0 = axial force
    1 = shear force
    2 = moment
    """
    
    return node.Fint[[ind,ind+3]]
    


def plotMoment(beam):
    
    # Plotbeam....
    xcoords = np.zeros(beam.Nnodes*2)
    moment = np.zeros(beam.Nnodes*2)
    
    plotInd = 2
    for ii, node in enumerate(beam.nodes):
        ind1 = 2*ii
        ind2 = ind1 + 2
        xcoords[ind1:ind2] = node.x
        moment[ind1:ind2] = getInternalForces(node, plotInd)
        # moment[ii] = 
    
    fig, ax = plt.subplots()
    line = plt.plot(xcoords, moment, '.')
    return fig, ax, line
        
        
def plotShear(beam):
    
    # Plotbeam....  
    xcoords = np.zeros(beam.Nnodes*2)
    moment = np.zeros(beam.Nnodes*2)
    
    plotInd = 1
    for ii, node in enumerate(beam.nodes):
        ind1 = 2*ii
        ind2 = ind1 + 2
        xcoords[ind1:ind2] = node.x
        moment[ind1:ind2] = getInternalForces(node, plotInd)
        # moment[ii] = 
    
    fig, ax = plt.subplots()
    line = plt.plot(xcoords,moment)     
    
    return fig, ax, line

    
    
    
        
