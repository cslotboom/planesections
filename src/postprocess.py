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
    



def _initOutputFig(showAxis, showGrid):
    
    fig, ax = plt.subplots(dpi=300)
        

    if not showAxis:
        ax.axis("off")
    else:
        ax.spines['top'].set_linewidth(0)
        ax.spines['right'].set_linewidth(0)
        ax.spines['left'].set_linewidth(0)
        ax.spines['bottom'].set_linewidth(0)
    
    if showGrid:
        ax.grid(which='major', axis='both', c= 'black', linewidth = 0.4)
        ax.minorticks_on()
        ax.tick_params(axis='y', which='minor', colors='grey')
        # ax.tick_params(axis='y', which='minor', colors='grey')
        ax.grid(which='minor', axis='both', c='grey')
    
    
    return fig, ax

def _plotAxis(ax, xcoords, xunit, yunit):
    plt.plot([xcoords[0],xcoords[-1]], [0,0] , c='black', linewidth=0.5)
    
    
    xlabel = 'Distance (' + xunit + ')'
    ylabel = 'Internal Force  (' + yunit + ')'
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

# def plotAxis():
    

def _plotLabels(ax, xcoords, ycoords, labels):
    
    offsetx = (max(xcoords) - min(xcoords)) / 100
    # offsetx = 0
    offsety = (max(ycoords) - min(ycoords)) / 50
    # print(len(xcoords))
    # print(len(labels))
    
    # print(xcoords)
    for ii in range(len(labels)):
        xcoord = xcoords[ii*2]
        label = labels[ii]
        # print(label)
        if label is not None:
            _plotLabel(ax, xcoord, label, offsetx, offsety)

    
def _plotLabel(ax, xcoord, label, offsetx, offsety):
    x = xcoord  + offsetx
    y = 0 + offsety
    # ax.text(x, y, label, {'size':12})
    ax.text(x, y, label)



def plotMoment2D(beam:Beam2D, scale:float=1, **kwargs):
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
    return plotInternalForce2D(beam, 2, scale, **kwargs)
     

    



def plotShear2D(beam:Beam2D, scale:float=1, **kwargs):
    return plotInternalForce2D(beam, 1, scale, **kwargs)

def plotInternalForce2D(beam:Beam2D, index:int, scale:float, xunit= 'm', yunit = 'kN',
                        showAxis = True, showGrid = False, labelPlot = True):
    """
    Plots the internal forces within a beam. Each node will contain the
    relevant force information. Analysis must be run on the beam prior to 
    plotting.
    
    Both the lest and right side forces at each node will be plotted.
    
    Parameters
    ----------
    beam : Beam2D
        The beam to plot internal forces with. The analysis must be run.
    index : TYPE
        The type of response to plot, can have value 0:axial force, 1: shear force
        2: moment.
    scale : float, optional
        The scale to apply to the plot. The default is 1.
    xunit : str, optional
        The xunit for the plot. The default is 1.
    yunit : str, optional
        The scale to apply to the plot. The default is 1.
    showAxis : bool, optional
        Turns on or off the axis.
    labelPeak : bool, optional
        Turns on or off labels for the peaks.

    Returns
    -------
    fig : matplotlib fig
    ax : matplotlib ax
    line : matplotlib line
        the plotted line.

    """
    
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
        
    fig, ax = _initOutputFig(showAxis, showGrid)
    _plotAxis(ax, xcoords, xunit, yunit)
    
    if labelPlot:
        _plotLabels(ax, xcoords, force*scale, labels)
    
    line = plt.plot(xcoords, force*scale)     
    
    return fig, ax, line
  
         
        
def plotVertDisp2D(beam:Beam2D):
    return plotDisp2D(beam) 


def plotRotation2D(beam:Beam2D):
    return plotDisp2D(beam, 2)

# def plotVertDisp(beam):
#     return plotDisp() 


def plotDisp2D(beam:Beam2D, index=1, scale=1):
    """
    Plots the displacement of a beam. Each node will contain the
    relevant dispancement information. Analysis must be run on the beam prior to 
    plotting.
    
    Parameters
    ----------
    beam : Beam2D
        The beam to plot internal forces with. The analysis must be run.
    index : TYPE
        The type of response to plot, can have value 0:axial force, 1: shear force
        2: moment.
    scale : float, optional
        The scale to apply to the plot. The default is 1.

    Returns
    -------
    fig : matplotlib fig
    ax : matplotlib ax
    line : matplotlib line
        the plotted line.

    """
    
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
        

     
