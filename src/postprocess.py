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

def _plotAxis(ax, xcoords, xunit, yunit, baseY = 'Internal Force'):
    plt.plot([xcoords[0],xcoords[-1]], [0,0] , c='black', linewidth=0.5)
    
    
    xlabel = 'Distance (' + xunit + ')'
    ylabel = baseY + '  (' + yunit + ')'
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def _plotLabels(ax, xcoords, ycoords, labels):
    
    offsetx = (max(xcoords) - min(xcoords)) / 100
    offsety = (max(ycoords) - min(ycoords)) / 50
    for ii in range(len(labels)):
        xcoord = xcoords[ii]
        label = labels[ii]
        if label is not None:
            _plotLabel(ax, xcoord, label, offsetx, offsety)
 
def _plotLabel(ax, xcoord, label, offsetx, offsety):
    x = xcoord  + offsetx
    y = 0 + offsety
    ax.text(x, y, label)

def plotMoment2D(beam:Beam2D, scale:float=-1, yunit = 'Nm', **kwargs):
    """
    Plots the internal moment at each node in the beam. 
    Two values are given for each point, one at the left side, one at the right
    side. 
    Note that internal force is only known exactly at nodes, and linear 
    interpolation is used for all other values.

    Parameters
    ----------
    beam : Beam2D
        The beam to plot internal forces with. The analysis must be run.
    scale : float, optional
        The scale to apply to the plot. The default is 1.
    yunit : str, optional
        The yunit for the plot labels. The default is Nm.
        
    Kwarg Parameters
    ----------        
    These are possible Kwarg parameters that will be passed to plotInternalForce2D.
    
    xunit : str, optional
        The xunit for the plot labels. The default is m.
    showAxis : bool, optional
        Turns on or off the axis.
    showGrid : bool, optional
        Turns on or off the grid.        
    labelPlot : bool, optional
        Turns on or off the plot labels.    
        
    Returns
    -------
    fig : matplotlib fig
    ax : matplotlib ax
    line : matplotlib line
        the plotted line.

    """
    return plotInternalForce2D(beam, 2, scale , yunit = yunit, **kwargs)
     

    

def plotShear2D(beam:Beam2D, scale:float=1, **kwargs):
    """
    Plots the internal shear force within a beam. 
    Two values are given for each point, one at the left side, one at the right
    side. 
    The analysis must be run on the beam prior to plotting.
    Note that internal force is only known exactly at nodes, and linear 
    interpolation is used for all other values.
    
    Parameters
    ----------
    beam : Beam2D
        The beam to plot internal forces with. The analysis must be run.
    scale : float, optional
        The scale to apply to the plot. The default is 1.
        
    Kwarg Parameters
    ----------        
    
    These are possible Kwarg parameters that will be passed to plotInternalForce2D.
    
    xunit : str, optional
        The xunit for the plot labels. The default is m.
    yunit : str, optional
        The yunit for the plot labels. The default is N.
    showAxis : bool, optional
        Turns on or off the axis.
    showGrid : bool, optional
        Turns on or off the grid.        
    labelPlot : bool, optional
        Turns on or off the plot labels.        

    Returns
    -------
    fig : matplotlib fig
    
    ax : matplotlib ax
    
    line : matplotlib line
        the plotted line.

    """    
    
    return plotInternalForce2D(beam, 1, scale, **kwargs)

def plotInternalForce2D(beam:Beam2D, index:int, scale:float, xunit= 'm', yunit = 'N',
                        showAxis = True, showGrid = False, labelPlot = True):
    """
    Plots the internal forces within a beam. 
    Two values are given for each point, one at the left side, one at the right
    side. 
    The analysis must be run on the beam prior to plotting.
    Note that internal force is only known exactly at nodes, and linear 
    interpolation is used for all other values.
    
    Parameters
    ----------
    beam : Beam2D
        The beam to plot internal forces with. The analysis must be run.
    index : int
        The type of response to plot, can have value 0:axial force, 1: shear force
        2: moment.
    scale : float, optional
        The scale to apply to the plot. The default is 1.
    xunit : str, optional
        The xunit for the plot labels. The default is m.
    yunit : str, optional
        The yunit for the plot labels. The default is N.
    showAxis : bool, optional
        Turns on or off the axis.
    showGrid : bool, optional
        Turns on or off the grid.        
    labelPlot : bool, optional
        Turns on or off the plot labels.        

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
        _plotLabels(ax, xcoords[::2], force*scale, labels)
    
    line = plt.plot(xcoords, force*scale)     
    
    return fig, ax, line
  
         
        
def plotVertDisp2D(beam:Beam2D, scale=1000, yunit = 'mm', **kwargs):
    """
    Plots the rotation of a beam. Each node will contain the
    relevant dispancement information. Analysis must be run on the beam prior to 
    plotting.
    
    Parameters
    ----------
    beam : Beam2D
        The beam to plot internal forces with. The analysis must be run.
    index : int
        The type of response to plot, can have value 0:ux, 1: uy 2: rotation.
    scale : float, optional
        The scale to apply to the plot. The default is 0.001.
    xunit : str, optional
        The xunit for the plot labels. The default is m.
    yunit : str, optional
        The yunit for the plot labels. The default is mm.
    showAxis : bool, optional
        Turns on or off the axis.
    showGrid : bool, optional
        Turns on or off the grid.        
    labelPlot : bool, optional
        Turns on or off the plot labels.        
        
    Returns
    -------
    fig : matplotlib fig
    
    ax : matplotlib ax
    
    line : matplotlib line
        the plotted line.
    """    
    
    return plotDisp2D(beam, 1, scale, yunit= yunit, **kwargs) 


def plotRotation2D(beam:Beam2D, scale=1000, yunit = 'mRad', **kwargs):
    """
    Plots the rotation of a beam. Each node will contain the
    relevant dispancement information. Analysis must be run on the beam prior to 
    plotting.
    
    Parameters
    ----------
    beam : Beam2D
        The beam to plot internal forces with. The analysis must be run.
    index : int
        The type of response to plot, can have value 0:ux, 1: uy 2: rotation.
    scale : float, optional
        The scale to apply to the plot. The default is 0.001.
    xunit : str, optional
        The xunit for the plot labels. The default is m.
    yunit : str, optional
        The yunit for the plot labels. The default is mm.
    showAxis : bool, optional
        Turns on or off the axis.
    showGrid : bool, optional
        Turns on or off the grid.        
    labelPlot : bool, optional
        Turns on or off the plot labels.        
        
    Returns
    -------
    fig : matplotlib fig
    
    ax : matplotlib ax
    
    line : matplotlib line
        the plotted line.
    """
    
    
    
    return plotDisp2D(beam, 2, scale, yunit= yunit, **kwargs)


def plotDisp2D(beam:Beam2D, index=1, scale=0.001, xunit= 'm', yunit = 'mm',
                        showAxis = True, showGrid = False, labelPlot = True):
    """
    Plots the displacement of one dimension of the beam. Each node will contain the
    relevant dispancement information. Analysis must be run on the beam prior to 
    plotting.
    
    Parameters
    ----------
    beam : Beam2D
        The beam to plot internal forces with. The analysis must be run.
    index : int
        The type of response to plot, can have value 0:ux, 1: uy 2: rotation.
    scale : float, optional
        The scale to apply to the plot. The default is 0.001.
    xunit : str, optional
        The xunit for the plot labels. The default is m.
    yunit : str, optional
        The yunit for the plot labels. The default is mm.
    showAxis : bool, optional
        Turns on or off the axis.
    showGrid : bool, optional
        Turns on or off the grid.        
    labelPlot : bool, optional
        Turns on or off the plot labels.        
        
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
    labels = [None]*beam.Nnodes
    
    for ii, node in enumerate(beam.nodes):
        xcoords[ii] = node.x
        disp[ii] = node.disps[index]
        labels[ii] = node.label
        
    fig, ax = _initOutputFig(showAxis, showGrid)
    _plotAxis(ax, xcoords, xunit, yunit, 'Displacement')
    
    if labelPlot:
        _plotLabels(ax, xcoords, disp*scale, labels)
        
    line = plt.plot(xcoords, disp*scale)     

    return fig, ax, line   
        

     
