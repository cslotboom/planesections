"""
Common post-processing functions for plotting.
"""

import numpy as np
from planesections import Beam




def getDisp(beam: Beam, ind: int):
    """
    Gets the beam displacement along the axis specified for the index.

    Parameters
    ----------
    beam : Beam
        The beam to read displacement from. The beam must be analyzed to get 
        data.
    ind : int
        The index of the axis to read from. Can have value 0: horizontal 
        displacement
        1: vertical displacement 
        2: rotation.

    Returns
    -------
    disp : numpy array
        The displacement at each x coordinant.
    xcoords : numpy array
        The x coordinants.
    """
    
    xcoords = np.zeros(beam.Nnodes)
    disp = np.zeros(beam.Nnodes)   
    for ii, node in enumerate(beam.nodes):
        xcoords[ii] = node.x
        disp[ii] = node.disps[ind]
    return  disp, xcoords



def getVertDisp(beam: Beam):
    """
    Gets the beam vertical displacement for the beam

    Parameters
    ----------
    beam : Beam
        The beam to read displacement from. The beam must be analyzed to get 
        data.

    Returns
    -------
    disp : numpy array
        The displacement at each x coordinant.
    xcoords : numpy array
        The x coordinants.
    """
    return getDisp(beam, 1)


def getMaxVertDisp(beam: Beam):
    """
    Gets the absolute value of beam vertical displacement and it's location.

    Parameters
    ----------
    beam : Beam
        The beam to read displacement from. The beam must be analyzed to get 
        data.

    Returns
    -------
    dispMax : float
        The displacement at each x coordinant.
    xcoords : numpy array
        The x coordinants.
    """
    disp, x  = getVertDisp(beam)
    dispAbs = np.abs(disp)
    ind = np.argmax(dispAbs)
    return disp[ind], x[ind]


def _getForceValues(beam, index):
    Nnodes = len(beam.nodes)
    xcoords = np.zeros(Nnodes*2)
    force = np.zeros(Nnodes*2)
    labels = [None]*Nnodes
    for ii, node in enumerate(beam.nodes):
        ind1 = 2*ii
        ind2 = ind1 + 2        
        xcoords[ind1:ind2]       = node.x        
        force[ind1:ind2] = node.getInternalForces(index)
        labels[ii] = node.label
        
    return xcoords, force, labels