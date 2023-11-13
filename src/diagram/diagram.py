# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 20:57:19 2022

@author: Christian

"""

import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch
from abc import ABC, abstractmethod
from planesections import diagramUnits
from planesections.builder import EleLoadDist


from .components import basic as basic

"""
Not used properly right now, but ideally this is defined only in one place.
"""
fixities  = {'free':[0,0,0], 'roller': [0,1,0], 
             'pinned':[1,1,0], 'fixed':[1,1,1]}


@dataclass
class EleLoadPlotCollection:
    fplot:float
    xcoord:list
    ycoord:float
    spacing:float
    isLinear:bool

@dataclass
class EleLoadBox:
    y:[float, float]
    x:[float, float]

    def __post_init__(self):
        self.x.sort()
        self.y.sort()


@dataclass
class DiagramEleLoad:
    loadBox:EleLoadBox
    

def _checkInRange(xrange1, xrange2):
    """
    Checks if either point of xrange1 is in xrange2
    """
    if  (xrange2[0] <= xrange1[1]) and (xrange1[0] <= xrange2[1]):
        return True
    else:
        return False

def checkBoxesForOverlap(box1:EleLoadBox, box2:EleLoadBox):
    """
    Checks if box1 overlaps with box2

    Parameters
    ----------
    box1 : EleLoadBox
        DESCRIPTION.
    box2 : EleLoadBox
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    if _checkInRange(box1.x, box2.x) and _checkInRange(box1.y, box2.y):
        return True  
    else:
        return False


class BeamPlotter2D:
    
    FORCE_LINE_SPACING = 25
    
    def __init__(self, beam, figsize = 8, units = 'environment'):
        """
        Used to make a diagram of the beam. Only certain fixities are supported
        for plotting, including free, roller (support only in y), 
        pinned (support in x and y), and fixed (support in x/y/rotation).
        Only certain forces are supported for plotting - for distrubuted
        forces only the y component of the beam can be plotted.
        Mixed Forces, those that contain a combination of Px/Py/Moment will 
        not be plotted
     
        Note, the diagram has been rescaled so it's length in the digram 
        isn't it's analysis lenght.
        This is to make consistent plotting easier across a number of beam 
        sizes, however, the matplotlib objects in the plot have 
        different lengths than the actual beam.
        
        The class used as a interface between the high level beam abstraction 
        and lower level rules plotting.    
        
        unitHandler: str, or dict
            Represents the . the env tag.
            
        """        
        
        self.beam = beam
        self.figsize = figsize
        
        if units == 'environment':
            self.unitHandler = diagramUnits.activeEnv
        else:
            self.unitHandler = diagramUnits.getEnvironment(units)
        
        L = beam.getLength()       
        xscale = L  / self.figsize
        self.xscale = xscale
        self.plotter = basic.BasicDiagramPlotter()
   
        xlims = beam.getxLims()
        self.xmin = xlims[0]
        self.xmax = xlims[0]
                
        self.xlimsPlot = [(xlims[0] - L/20) / xscale, (xlims[1] + L/20) / xscale]
        self.ylimsPlot = [-L/10 / xscale, L/10 / xscale]
        
        self.plottedNodeIDs = []
       

    def plot(self, plotLabel = False, labelForce = True, 
             plotForceValue = True, **kwargs):
        """
        Plots the beam, supports, point forces, element forces, and labels.
        
        Note that forces have a "static" and "adaptive" portion of their length
        . This means that arrows can't have values length less than a certain 
        length, preventing very small arrows from being plotted that look silly.
        However, this also means that the ratio between different arrows won't
        be exactly the ratio between their force magnitude.
        
        Only the vertical components of distributed forces are plotted.

        """
        args = (self.figsize, self.xlimsPlot, self.ylimsPlot)
        self.fig, self.ax = self.plotter._initPlot(*args)
        self.plotSupports()
        
        if self.beam.pointLoads:
            fplot = self.plotPointForces()
        if self.beam.pointLoads and plotLabel:
            self.plotPointForceLables(fplot, labelForce, plotForceValue)
        if self.beam.eleLoads:
            fplot, xcoords = self.plotEleForces()
        # if self.beam.eleLoads and plotLabel:
        #     self.plotDistForceLables(fplot, xcoords, labelForce, plotForceValue)
            
        if plotLabel:
            # print('here')
            self.plotLabels()
            
        self.plotBeam()
        
    def plotBeam(self):
        """
        Plots the base beam element.
        """
        xlims   = self.beam.getxLims()
        xy0     = [xlims[0]  / self.xscale, 0]
        xy1     = [xlims[1]  / self.xscale, 0]        
        self.plotter.plotBeam(self.ax, xy0, xy1)
               
    def plotSupports(self):
        """
        Finds the type of and plots each supports
        """
        
        for node in self.beam.nodes:
            fixityType  = node.getFixityType()
            x = node.getPosition()
            xy = [x / self.xscale, 0]
            
            """
            The direction assignment assumes the shape of the system.
            """
            kwargs = {}
            if fixityType == 'fixed' and x == self.xmin:
                kwargs =  {'isLeft':True}
                    
            if fixityType == 'fixed' and not x == self.xmin:
                kwargs  = {'isLeft':False}                
                        
            self.plotter.plotSupport(self.ax, xy, fixityType, kwargs)
        
    def _addLabelToPlotted(self, nodeID):
        self.plottedNodeIDs.append(nodeID)     

    def _checkIfLabelPlotted(self, nodeID):
        check = nodeID in self.plottedNodeIDs
        return check
        
    def plotLabels(self):
        """
        Adds all labels to the plot. Labels are offset from the point in the 
        x and y.
        """
        for node in self.beam.nodes:
            label = node.label
            x     = node.getPosition()
            
            if label and (self._checkIfLabelPlotted(node.ID) != True):
                xy = [x / self.xscale, 0]
                self.plotter.plotLabel(self.ax, xy, label)
                self._addLabelToPlotted(node.ID)

    def _getValueText(self, diagramType, forceValue):
        
        unit = self.unitHandler[diagramType].unit
        scale = self.unitHandler[diagramType].scale
        Ndecimal = self.unitHandler[diagramType].Ndecimal
        
        # Round force
        forceValue *= scale
        if Ndecimal == 0:
            forceValue = round(forceValue)
        else:
            forceValue = round(forceValue*10**Ndecimal) / 10**Ndecimal
        return forceValue, unit


    def plotPointForceLables(self, fplot, labelForce, plotForceValue):
        """
        Adds all labels to the plot. Labels are offset from the point in the 
        x and y.
        """
        
        inds = range(len(self.beam.pointLoads))
        for ii, force in zip(inds, self.beam.pointLoads):
            Px, Py, Mx = fplot[ii]
            isMoment = False
            if Mx != 0:
                isMoment = True
                Py = -0.15
                diagramType = 'moment'
                fText = force.P[2]
            else:
                # shift the force down so it fits in the diagram!
                Py += 0.15
                diagramType = 'force'
                fText = np.sum(force.P[:2]**2)**0.5
            
            # get the label from the node - it's store there and not on the force.
            labelBase = self.beam.nodes[force.nodeID - 1].label
            label = ''
            
            if labelBase and labelForce and isMoment:
                label +=  f'$M_{{{labelBase}}}$' # Tripple brackets needed to make the whole thing subscript
                
            elif labelBase and labelForce and (not isMoment):
                label += f'$P_{{{labelBase}}}$'
            else:
                pass
            
            if labelBase and plotForceValue and labelForce:
                valueText, unit = self._getValueText(diagramType, fText)
                label += ' = ' + str(valueText) + "" + unit
                        
            x = force.getPosition()
            xy = [x / self.xscale, -Py]
            
            if label and self._checkIfLabelPlotted(force.nodeID) != True:
                self.plotter.plotLabel(self.ax, xy, label)
                self._addLabelToPlotted(force.nodeID)
                                        
                            
    def plotDistForceLables(self, fplot, xcoords, labelForce, plotForceValue):
        """
        Adds all labels to the plot. Labels are offset from the point in the 
        x and y.
        """
        diagramType = 'distForce'
        inds = range(len(self.beam.eleLoads))
        for ii, force in zip(inds, self.beam.eleLoads):
            qx, qy = fplot[ii]
            fText = force.P[1]
            
            labelBase = force.label
            label = ''
            
            if labelBase and labelForce:
                label += f'$q_{{{labelBase}}}$'
            
            if labelBase and plotForceValue and labelForce:
                valueText, unit = self._getValueText(diagramType, fText)
                label += ' = ' + str(valueText) + "" + unit            
            
            x1, x2 = xcoords[ii]
            aMid = (x1 + x2 ) / 2
            xy = [aMid, -qy]   # note, aMid has already been scaled         
            self.plotter.plotLabel(self.ax, xy, label)              

    def _getForceVectorLengthPoint(self, forces, vectScale = 1):
        """
        Gets the force vector length in terms of the drawing units.
        Force vectors will have a static component that doesn't change,
        and a dynamic component that adapts to the magnitude of forces.
        
        The output plotting forces are in the direction they act.

        """
        fscale0 = 0.4
        fstatic0 = 0.3
        
        # Normalize forces
        forces = np.array(forces)
        signs = np.sign(forces)
        
        # The maximum force in each direction
        Fmax   = np.max(np.abs(forces), 0)          
        
        # Avoid dividing by zero later
        Inds   = np.where(np.abs(Fmax) == 0)
        Fmax[Inds[0]] = 1
        
        # Find all force that are zero. These should remain zero
        Inds0 = np.where(np.abs(forces) == 0)
        
        # Plot the static portion, and the scale port of the force
        fscale = fscale0*abs(forces) / Fmax
        fstatic = fstatic0*np.ones_like(forces)
        fstatic[Inds0[0],Inds0[1]] = 0
        
        fplot =  (fscale + fstatic)*signs
        
        return fplot*vectScale
    
    
    def plotPointForces(self):
        """
        Plots all point forces.
        
        Forces have a static portion to their length and dynamic portion.
        This means that arrows can't have length less than a certain value.
        This prevents small from being plotted that look silly.

        """
        forces  = []
        xcoords = []
        for force in self.beam.pointLoads:
            forces.append(force.P)
            xcoords.append(force.x / self.xscale)
        fplot  = self._getForceVectorLengthPoint(forces)
        NLoads = len(forces)
        
        for ii in range(NLoads):
            Px, Py, Mx = fplot[ii]
            x = xcoords[ii]
            if (Px == 0 and Py ==0): # if it's a moment, plot it as a moment
                if Mx < 0:
                    postive = True
                else:
                    postive = False
                self.plotter.plotPointMoment(self.ax, (x,0), postive)
            else:
                self.plotter.plotPointForce(self.ax, (x - Px, -Py), (Px, Py))
                
        return fplot

    def _plotEleForce(self, loadInput:EleLoadPlotCollection):
        
        Py = loadInput.fplot
        x1, x2 = loadInput.xcoord
        spacing = loadInput.spacing
        ydatum = loadInput.ycoord # y1 is the start point of the arrow
        
        if (Py[0] == 0) and (Py[1] == 0):
            print("WARNING: Plotted load has no vertical component.")            
        
        if not loadInput.isLinear:
            # This is a little akward, but Py is added to account for the offset of -Py in the base funciton.
            self.plotter.plotVerticalDistLoad(x1, x2, Py[1], ydatum, spacing)
        else:
            self.plotter.plotVerticalLinearLoad(x1, x2, Py, ydatum, spacing)

    def _getForceVectorLengthEle(self, 
                                 forces:list[list[float, float]], 
                                 vectScale = 1):
        """
        Gets the force vector length in terms of the drawing units.
        Force vectors will have a static component that doesn't change,
        and a dynamic component that adapts to the magnitude of forces.
        
        The output plotting forces are in the direction they act.
        
        The element load plotting does not work with non-vertical loads.

        """
        fscale0 = 0.4
        fstatic0 = 0.3
        
        forces = np.array(forces)
        
        Fmax = np.max(np.abs(forces))

        # Get the sign of the maximum force. Ignores loads with sign changes
        tmpForces = np.copy(forces)
        inds = np.where(tmpForces == 0)
        
        tmpForces[inds] = 1 
        signs = forces / np.abs(tmpForces)
        
        # Find all force that are zero. These should remain zero
        Inds0 = np.where(np.abs(forces) == 0)
        
        # Plot the static portion, and the scale port of the force
        fscale = fscale0*abs(forces) / Fmax
        fstatic = fstatic0*np.ones_like(forces)
        fstatic[Inds0[0], Inds0[1]] = 0
        
        fplot =  ((fscale + fstatic) * signs)
        
        return fplot*vectScale
       
    def _getEleForcePlotInput(self):
        """
        Handles all the logic of generating stacked object positions.
        
        This is a bandaid solution right now. The better approach would to have
        seperate plotting classes for each type of element, as opposed to
        one giant megaclass. We could then use a interface with object.plot()
        
        """
        
        # The spacing between force lines
        beam = self.beam
        spacing  = beam.getLength() / self.FORCE_LINE_SPACING / self.xscale
        forces   = []
        xcoords  = []
        isLinear = []
        
        for load in self.beam.eleLoads:
            xcoords.append([load.x1 / self.xscale, load.x2 / self.xscale])
            
            if isinstance(load, EleLoadDist):
                isLineartmp = False
                # Take vertical load. Adapt the load so it's a 2D vector
                forces.append(np.array([0, load.P[1]]))

            else:
                isLineartmp = True
                # Take vertical load. Signs can change for linear loads.
                forces.append(load.P[1])
                
            isLinear.append(isLineartmp)
        
        fplot   = self._getForceVectorLengthEle(forces, vectScale = 0.4)
        ycoords = self._getStackedPositions(xcoords, fplot, isLinear)
        
        elePlotInputCollections = []
        for ii, load in enumerate(beam.eleLoads):
            collection = EleLoadPlotCollection(fplot[ii], xcoords[ii], ycoords[ii], 
                                               spacing, isLinear[ii])
            elePlotInputCollections.append(collection)
        return elePlotInputCollections
             
    def plotEleForces(self):
        """
        Plots all distributed forces. Only vertical forces can be plotted.
        If a horizontal component is supplied to the force, it is not included
        in the plot.
        """

        elePlotInputCollections =  self._getEleForcePlotInput()
        
        NLoads = len(elePlotInputCollections)
        for ii in range(NLoads):
            collection = elePlotInputCollections[ii]
            self._plotEleForce(collection)
        
        # Bandaid fix..
        fplot = [item.fplot for item in elePlotInputCollections]
        xcoords = [item.xcoord for item in elePlotInputCollections]
        return fplot, xcoords
       
    def _getStackedPositions(self, xcoords: list[list[float, float]], 
                                   fplot:   list[list[float, float]],
                                   isLinear:list[bool]):
        """
        Gives the forces an order, and finds where to put them porportionally.
        Longer forces will go on the bottom, while shorter forces are
        placed on top of them.
        """      
        Nforces = len(xcoords)
        lengths = [None]*Nforces
        xcoords = np.array(xcoords)
        ycoords = np.zeros(Nforces) # [bottom, top]
        
        # Get the lengths
        lengths = xcoords[:,1] - xcoords[:,0]
        sortedInds = np.argsort(lengths)[::-1]
        
        # Make a copy of the plot.
        fplotOut = np.zeros_like(fplot)
        fplotOut[:] = fplot

        # the current x and y points being plotted.    
        posStackx = []
        posStackTop = []
        negStackx = []
        negStackTop = []
        
        # start at the widest items and plot them first
        for ind in sortedInds:

            fplotRow = fplotOut[ind]
            dy = fplot[ind]
            if not isLinear[ind]:
                dy = fplotRow[1]
            else: # do a complicated calculation to find the datum should be
                y1 = self._getStackedDatum(xcoords[ind], posStackx, posStackTop)    
                y2 = self._getStackedDatum(xcoords[ind], posStackx, posStackTop)    
                
                if y1 == 0 and y2 == 0:
                    
                    dy = abs(fplotRow[1] + fplotRow[0])
            
            if dy <0:
                y0 = self._getStackedDatum(xcoords[ind], posStackx, posStackTop)
                ycoords[ind] =  y0 - dy
                posStackx.append(xcoords[ind])           
                posStackTop.append(ycoords[ind])
            else:
                y0 = self._getStackedDatum(xcoords[ind], negStackx, negStackTop)
                ycoords[ind] =  y0 - dy
                negStackx.append(xcoords[ind])           
                negStackTop.append(ycoords[ind])
            
        return ycoords
      
    def _checkIfInRange(self, xtest, x1,x2):
        if (x1 < xtest) and (xtest < x2):
            return True
        return False
    
    def _getStackedDatum(self, xCurrent:list[float, float], 
                               stackRanges:list, 
                               currentY:list):
        """
        Look at all of the current forces on the side in question.
        
        Starting at the top of the force stack, check each force to see if
        it intersects with any other forces.
        """
        
        Nloads = len(stackRanges)
        for ii in range(Nloads):
            localInd = Nloads - 1 - ii
            x1, x2  = stackRanges[localInd]
            if self._checkIfInRange(xCurrent[0], x1, x2): # left side
                return currentY[localInd]
            if self._checkIfInRange(xCurrent[1], x1, x2): # right side
                return currentY[localInd]       
        return 0
                       

def plotBeamDiagram(beam, plotLabel = True, labelForce = False, 
                    plotForceValue = False, units = 'environment'):
    """
    Creates a diagram of the created beam.
    Only certain fixities are supported for plotting, including free, roller 
    (support only in y), pinned (support in x and y), and fixed 
    (support in x/y/rotation).
    Only certain forces are supported for plotting - for distrubuted
    forces only the y component of the beam can be plotted.
 
    Note, the diagram has been rescaled so the beam has lenght scaled to the
    maximum beam size of 8.
    This is to make consistent plotting easier across a number of beam sizes,
    however, the matplotlib objects in the plot have different value than 
    the actual beam.
    
    The resulting diagram is a matplotlib figure that can be further 
    manipulated.

    Parameters
    ----------
    beam : PlaneSections beam
        The Beam Object to be plotted.
    plotLabel : bool, optional
        A toggle that turns on or off plotting user defined labels along the 
        beam. The default is True.
    labelForce : bool, optional
        A toggle that turns on or off if forces get labeled. If toggled to 
        true, forces will be given a label instead of the beam location.
        The default is True.
    plotForceValue : bool, optional
        A toggle that turns on or off plotting the force values with the label. 
        If set to true, the magnitude of the force will be plotted in
        the digram units. The default is False.
    units : str, optional
        A string that specified how the diagram units will be managed in the.
        The default value 'environment' causes the plot to read from the active
        environment. see :py:class:`planesections.DiagramUnitEnvironmentHandler`
        
        If not set to environment, it can have value:  *'metric',  
        'metric_kNm',  'metric_Nm',  
        'imperial_ftkip',  'imperial_ftlb'*        

        The unit handler for the plot. This The default is 'environment'.

    Returns
    -------
    fig : matplotlib fig
    
    ax : matplotlib ax

    """
    diagram = BeamPlotter2D(beam, units = units)
    diagram.plot(plotLabel, labelForce, plotForceValue)
    return diagram.fig, diagram.ax



