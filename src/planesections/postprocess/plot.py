import numpy as np
import matplotlib.pyplot as plt
from planesections import Node2D, Beam
import textalloc as ta

from dataclasses import dataclass

from .parse import _getForceValues
from .poi import findAllPOI, removeFalsePOI

   
# =============================================================================
# Plotting
# =============================================================================

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

def plotMoment(beam:Beam, scale:float=-1, yunit = 'Nm', **kwargs):
    """
    Plots the internal moment at each node in the beam. 
    Two values are given for each point, one at the left side, one at the right
    side. 
    Note that internal force is only known exactly at nodes, and linear 
    interpolation is used for all other values.
    
    For 3D beams, returns the strong axis Moment.

    Parameters
    ----------
    beam : Beam
        The beam to plot internal forces with. The analysis must be run.
    scale : float, optional
        The scale to apply to y values of the plot. The default is 1.
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
    labelPOI : bool, optional
        Turns on or off the plot point of interst labels.    
    POIOptions : dict, optional
        The options to use for the POI labels. There are several flags that 
        have values true or false which can be used to turn on or off certain
        points of interst. Notably:
            
            showLabels: this flag turns on or off 
            
            showDiscontinutiy: this flag turns on labeling points of discontinuity
            
            showMax: this turns on or off
        
        The default is None, which sets all flags to true    
    fig : bool, optional
        A existing figure to use in the plot.   
    ax : bool, optional
        A existing axis to use in the plot.   

    Returns
    -------
    fig : matplotlib fig
    
    ax : matplotlib ax
    
    line : matplotlib line
        the plotted line.

    """
    ind = beam.getDOF() - 1
    return plotInternalForce(beam, ind, scale , yunit = yunit, **kwargs)


def plotMoment2D(beam:Beam, scale:float=-1, yunit = 'Nm', **kwargs):
    """
    Depricated, use plotMoment instead

    """ 
    ind = beam.getDOF() - 1
    return plotInternalForce2D(beam, ind, scale , yunit = yunit, **kwargs)
     
def plotShear2D(beam:Beam, scale:float=1, **kwargs):
    """
    Depricated, use plotShear instead

    """    
    
    return plotInternalForce2D(beam, 1, scale, **kwargs)
    

def plotShear(beam:Beam, scale:float=1, **kwargs):
    """
    Plots the internal shear force within a beam. 
    Two values are given for each point, one at the left side, one at the right
    side. 
    The analysis must be run on the beam prior to plotting.
    Note that internal force is only known exactly at nodes, and linear 
    interpolation is used for all other values.
    
    For 3D beams, returns the Vy, the vertical component of force.

    
    Parameters
    ----------
    beam : Beam
        The beam to plot internal forces with. The analysis must be run.
    scale : float, optional
        The scale to apply to y values of the plot. The default is 1.
        
    Kwarg Parameters
    ----------        
    
    These are possible Kwarg parameters that will be passed to plotInternalForce.
    
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
    labelPOI : bool, optional
        Turns on or off the plot point of interst labels.    
    POIOptions : dict, optional
        The options to use for the POI labels. There are several flags that 
        have values true or false which can be used to turn on or off certain
        points of interst. Notably:
            
            showLabels: this flag turns on or off 
            
            showDiscontinutiy: this flag turns on labeling points of discontinuity
            
            showMax: this turns on or off
        
        The default is None, which sets all flags to true    
    fig : bool, optional
        A existing figure to use in the plot.   
    ax : bool, optional
        A existing axis to use in the plot.   

    Returns
    -------
    fig : matplotlib fig
    
    ax : matplotlib ax
    
    line : matplotlib line
        The plotted line.

    """    
    
    return plotInternalForce(beam, 1, scale, **kwargs)

@dataclass
class _NodeOutputs:
    xcoords:list[float]
    force:list[float]
    labels:list[str]


def plotInternalForce(beam:Beam, index:int, scale:float, xunit= 'm', yunit = 'N',
                      showAxis = True, showGrid = False, labelPlot = True,
                      labelPOI = False, POIOptions = None, 
                      fig = None, ax = None):
    """
    Plots the internal forces within a beam. 
    Two values are given for each point, one at the left side, one at the right
    side. 
    The analysis must be run on the beam prior to plotting.
    Note that internal force is only known exactly at nodes, and linear 
    interpolation is used for all other values.
    
    Parameters
    ----------
    beam : Beam
        The beam to plot internal forces with. The analysis must be run.
    index : int
        The type of response to plot, can have value 
        
        In 2D has values:
            [0:Fx, 1: Fy, 2: M]
            
        In 3D has values:
            [0:Fx, 1: Fy, 2: Fz, 3: Mx, 4: Mx, 5: Mz]
            
    scale : float, optional
        The scale to apply to y values of the plot. The default is 1.
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
    labelPOI : bool, optional
        Turns on or off the plot point of interst labels.    
    POIOptions : dict, optional
        The options to use for the POI labels. There are several flags that 
        have values true or false which can be used to turn on or off certain
        points of interst. Notably:
            showLabels: this flag turns on or off POI label on points with user labels.
            
            showDiscontinutiy: this flag turns on POI labels on points of discontinuity.
            
            showMax: this turns on or off POI at maximum points.
        
        The default is None, which sets all flags to true          
    fig : bool, optional
        A existing figure to use in the plot.   
    ax : bool, optional
        A existing axis to use in the plot.   
        
    Returns
    -------
    fig : matplotlib fig
    
    ax : matplotlib ax
    
    line : matplotlib line
        the plotted line.

    """
    xcoords, force, labels = _getForceValues(beam, index)
    forceScaled = force*scale
    
    fig, ax = _initOutputFig(showAxis, showGrid)
    _plotAxis(ax, xcoords, xunit, yunit)
    
    if labelPlot:
        _plotLabels(ax, xcoords[::2], forceScaled, labels)
    line = plt.plot(xcoords, forceScaled)
    
    if labelPOI:
        shear = None
        if index == 2:
            _, shear, _ = _getForceValues(beam, index-1)
        candidatePOI    = findAllPOI(xcoords, forceScaled, labels, shear, POIOptions)
        filteredPoiInd  = removeFalsePOI(candidatePOI, force)
        plotPOI(fig, ax, xcoords, forceScaled, labels, filteredPoiInd)
    
    return fig, ax, line


def plotInternalForce2D(beam:Beam, index:int, scale:float, xunit= 'm', yunit = 'N',
                        showAxis = True, showGrid = False, labelPlot = True):
    raise Exception('All 2D plot functions are depricated and will be removed in future releases. \
          Use the generic plot functions instead, i.e. plotInternalForce instead of plotInternalForce2D' )
    

def plotVertDisp(beam:Beam, scale=1000, yunit = 'mm', **kwargs):
    """
    Plots the rotation of a beam. Each node will contain the
    relevant dispancement information. Analysis must be run on the beam prior to 
    plotting.
    
    Parameters
    ----------
    beam : Beam
        The beam to plot internal forces with. The analysis must be run.
    index : int
        The type of response to plot, can have value 0:ux, 1: uy 2: rotation.
    scale : float, optional
        The scale to apply to the plot. The default is 0.001.
    xunit : str, optional
        The xunit for the plot labels. The default is m.
    yunit : str, optional
        The scale to apply to y values of the plot. The default is mm.
    showAxis : bool, optional
        Turns on or off the axis.
    showGrid : bool, optional
        Turns on or off the grid.        
    labelPlot : bool, optional
        Turns on or off the plot labels.   
    fig : bool, optional
        A existing figure to use in the plot.   
    ax : bool, optional
        A existing axis to use in the plot.   
        
    Returns
    -------
    fig : matplotlib fig
    
    ax : matplotlib ax
    
    line : matplotlib line
        the plotted line.
    """    
    
    return plotDisp(beam, 1, scale, yunit= yunit, **kwargs) 


def plotRotation(beam:Beam, scale=1000, yunit = 'mRad', **kwargs):
    """
    Plots the rotation of a beam. Each node will contain the
    relevant dispancement information. Analysis must be run on the beam prior to 
    plotting.
    
    Parameters
    ----------
    beam : Beam
        The beam to plot internal forces with. The analysis must be run.
    index : int
        The type of response to plot, can have value 0:ux, 1: uy 2: rotation.
    scale : float, optional
        The scale to apply to y values of the plot. The default is 0.001.
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
    fig : bool, optional
        A existing figure to use in the plot.   
    ax : bool, optional
        A existing axis to use in the plot.   
        
    Returns
    -------
    fig : matplotlib fig
    
    ax : matplotlib ax
    
    line : matplotlib line
        the plotted line.
    """
    
    ind = beam.getDOF() - 1
    
    return plotDisp(beam, ind, scale, yunit= yunit, **kwargs)


def plotDisp(beam:Beam, index=1, scale=1000, xunit= 'm', yunit = 'mm',
             showAxis = True, showGrid = False, labelPlot = True,
             labelPOI = False, POIOptions = None, fig = None, ax = None):
    """
    Plots the displacement of one dimension of the beam. Each node will contain the
    relevant dispancement information. Analysis must be run on the beam prior to 
    plotting.
    
    Parameters
    ----------
    beam : Beam
        The beam to plot internal forces with. The analysis must be run.
    index : int
        The type of response to plot, can have value 0:ux, 1: uy 2: rotation.
    scale : float, optional
        The scale to apply to y values of the plot. The default is 0.001.
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
    fig : bool, optional
        A existing figure to use in the plot.   
    ax : bool, optional
        A existing axis to use in the plot.   
        
    Returns
    -------
    fig : matplotlib fig
    
    ax : matplotlib ax
    
    line : matplotlib line
        The plotted line.

    """
    
    # Plotbeam....  
    xcoords = np.zeros(beam.Nnodes)
    disp = np.zeros(beam.Nnodes)
    labels = [None]*beam.Nnodes
    
    for ii, node in enumerate(beam.nodes):
        xcoords[ii] = node.x
        disp[ii] = node.disps[index]
        labels[ii] = node.label
    
    if not fig and not ax:
        fig, ax = _initOutputFig(showAxis, showGrid)
        _plotAxis(ax, xcoords, xunit, yunit, 'Displacement')
        
    disp = disp*scale

    if labelPlot:
        _plotLabels(ax, xcoords, disp, labels)
        
    line = plt.plot(xcoords, disp)     

    if labelPOI:
        candidatePOI = findAllPOI(xcoords, disp, labels, POIOptions = POIOptions)
        filteredPoiInd = removeFalsePOI(candidatePOI, disp)
        plotPOI(fig, ax, xcoords, disp, labels, filteredPoiInd)

    return fig, ax, line 
 
def plotDisp2D(beam:Beam, index=1, scale=1000, xunit= 'm', yunit = 'mm',
                        showAxis = True, showGrid = False, labelPlot = True):
    print('All 2D plot functions are depricated and will return an error in future releases. \
          Use the generic plot functions instead, i.e. plotInternalForce instead of plotInternalForce2D' )
    return plotDisp(beam, index, scale, xunit, yunit,
                            True, False, True)
     
def plotVertDisp2D(beam:Beam, scale=1000, yunit = 'mm', **kwargs):
    """
    Depricated, instead use plotVertDisp
    """
    
    return plotDisp2D(beam, 1, scale, yunit= yunit, **kwargs) 

def plotRotation2D(beam:Beam, scale=1000, yunit = 'mRad', **kwargs):
    """
    Depricated, instead use plotRotation
    """
    
    ind = beam.getDOF() - 1
    
    return plotDisp2D(beam, ind, scale, yunit= yunit, **kwargs)

def plotPOI(fig, ax, xcoords, force, labels, filteredPoiInd):
    
    labelX = []
    labelY = []
    labelText = []
    for ind in filteredPoiInd:
        labelName = labels[int((ind+1)/2)]
        x0 = xcoords[ind]
        y0 = force[ind]
        xOut = round(x0,2)
        yOut = round(y0,1)
        base = ''
        if labelName:
            base = ' Point ' + labelName + ' \n'
        textX = f' x = {xOut} \n'
        textY = f' y = {yOut} '
        text = base + textX + textY
        labelX.append(x0)
        labelY.append(y0)
        labelText.append(text)

    ta.allocate_text(fig, ax, labelX, labelY, labelText, textsize=8,
                     x_scatter=labelX, y_scatter=labelY,
                     x_lines=[xcoords], y_lines=[force], 
                     linecolor='grey', linewidth=0.5,
                     max_distance = 0.5, min_distance = 0.02)