# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 20:57:19 2022

@author: Christian

"""

import numpy as np
from planesections import diagramUnits
from planesections.builder import EleLoadDist, EleLoadLinear

from .components import basic as basic
from matplotlib.pyplot import Figure, Axes

"""
Not used properly right now, but ideally this is defined only in one place.
"""
fixities  = {'free':[0,0,0], 'roller': [0,1,0], 
             'pinned':[1,1,0], 'fixed':[1,1,1]}

class EleLoadBox:
    """
    Assume that y is bounded by zero, or crosses boundaries
    
    The internal datum is where the datum lies between y1 and y2 as a ratio.
    
    By default assumes that the distribution is a constant oin the positive 
    side.
    
    Parameters
    ----------
    x : tuple[float]
        A tuple containing [x1, x2] for the box.
    y : tuple[float]
        A tuple containing [y1, y2] for the box. Y is always ordered where
        y1 < y2.
    fint : tuple[float], optional
        A tuple contiaining [fint1, fint2], where each value ranges from 0 to 1.
        The default is None.

    Returns
    -------
    None.

    """    
    def __init__(self, x:tuple[float], y:tuple[float], fint:tuple[float]=None,
                 intDatum:float=None):

        self.x = x
        self.y = y    

        self.x.sort()
        self.y.sort()
        
        if fint == None:
            fint = [1, 1]

        self.fint = fint
        self.fout = [self._interpolate(fint[0]), self._interpolate(fint[1])]
        
        # If the internal datum is manually set
        if intDatum:
            self.intDatum = intDatum
            self.datum = self._interpolate(intDatum)
            
            sign1 = np.sign(self.fout[0])
            sign2 = np.sign(self.fout[1])
            if sign1 == sign2 >= 0:
                self.changedDirection = False
            else:
                self.changedDirection = True
                
        # If there is no internal datum, this is the typical case.
        else:    
            self._initInternalDatum()
    
    def setDatum(self, datum):
        dy = datum - self.datum
        self.y = [self.y[0] + dy, self.y[1] + dy]
        self.datum = datum
        
        fint = self.fint
        self.fout = [self._interpolate(fint[0]), self._interpolate(fint[1])]
    
    def shiftDatum(self, dy):
        self.y = [self.y[0] + dy, self.y[1] + dy]
        self.datum = self.datum + dy
        
        fint = self.fint
        self.fout = [self._interpolate(fint[0]), self._interpolate(fint[1])]

    def getInternalDatum(self):
        return self.datum
    
    def _interpolate(self, fint):
        return (self.y[1] - self.y[0])*fint + self.y[0]
    
    def _initInternalDatum(self):
        """
        Sets the internal datum, making assumptions about the shape of the 
        system. Notably:
            - the box is "placed" next to the x axis
        """
        sign1 = np.sign(self.fout[0])
        sign2 = np.sign(self.fout[1])
        
        self.datum = 0
        if sign1 >= 0 and sign2 >= 0:
            self.changedDirection = False
            self.intDatum = 0
        
        elif sign1 <= 0 and sign2 <= 0:
            self.changedDirection = False
            self.intDatum = 1
        else:
            self.changedDirection = True
            dy = self.y[0] - self.y[1]
            self.intDatum =  self.y[0] / dy
    
    @property
    def isConstant(self):
        return self.fint[0] == self.fint[1]
        
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
        The first Box.
    box2 : EleLoadBox
        The second Box.

    Returns
    -------
    None.

    """
    
    if _checkInRange(box1.x, box2.x) and _checkInRange(box1.y, box2.y):
        return True  
    else:
        return False

class Boxstacker:
    
    def __init__(self, boxes:list[EleLoadBox]):
        """
        A class that can be used to stack a series of element boxes.

        Parameters
        ----------
        boxes : list[EleLoadBox]
            The list of boxes to stack.

        Returns
        -------
        None.

        """
        self.boxes = boxes

    def setStackedDatums(self):
        """
        Gives the forces an order, and finds where to put them porportionally.
        Longer forces will go on the bottom, while shorter forces are
        placed on top of them.
        """
        
        boxes = self.boxes
        Nforces = len(boxes)
        lengths = [None]*Nforces
        xcoords = np.array([box.x for box in boxes])
        ycoords = np.array([box.y for box in boxes]) # [bottom, top]
        
        # Get the lengths, the start with the longest and go to shortest
        lengths = xcoords[:,1] - xcoords[:,0]
        sortedInds = np.argsort(lengths)[::-1]

        # the current x and y points being plotted.    
        posStackx = []
        posStackTop = []
        negStackx = []
        negStackTop = []
        
        # start at the widest items and plot them first
        for ind in sortedInds:
            box = boxes[ind]
            
            # Datum is where we point towards!
            y = ycoords[ind]
            x = xcoords[ind]
                       
            # Case 1: Constantly distributed, use dy
            if box.isConstant:
                dy = box.fout[0]
                
                if 0 < dy:
                    self._addToStack(box, dy, x, posStackx, posStackTop)
                else:
                    self._addToStack(box, dy, x, negStackx, negStackTop)                
                
            # Case 2: linearly distributed, no sign change, use max values
            elif not box.changedDirection:
                # If a value is greater than zero, stack on pos side.
                if 0 < max(y):
                    dy = max(y)
                else:
                    dy = min(y)               
            
                if 0 < dy:
                    self._addToStack(box, dy, x, posStackx, posStackTop)
                else:
                    self._addToStack(box, dy, x, negStackx, negStackTop)
            
            # Case 3: Linearly distributed through zero, we work with fout
            # print(box.changedDirection)
            elif box.changedDirection:
                inPos, _ = self._checkInStack(x, posStackx)
                inNeg, _ = self._checkInStack(x, negStackx)
                
                # If 
                dyPos = max(box.fout)
                dyNeg = min(box.fout)
                
                # Case 3i: 
                # If there is no stacks, add it to the bottom of both stacks
                if (not inPos) and (not inNeg):
                    self._addToStack(box, dyPos, x, posStackx, posStackTop)
                    self._addToStack(box, dyNeg, x, negStackx, negStackTop)
                
                # Case 3ii: 
                # If there is a positive stack add it to the top of that stack
                elif inPos:
                    dy = dyPos - dyNeg
                    dDatum =  -dyNeg

                    self._addToStack(box, dy, x, posStackx, posStackTop, dDatum)
                # Case iii:
                # If there is only negative, shift above the x axis
                elif inNeg:
                    # box.shiftDatum(-box.datum)
                    dDatum =  -dyNeg
                    dy =  -dyNeg
                    self._addToStack(box, dy, x, posStackx, posStackTop, dDatum) 
                        
        return boxes
     
    def _checkIfInRange(self, xtest, x1,x2):
        if (x1 < xtest) and (xtest < x2):
            return True
        return False

    def _addToStack(self, box, dy, xcoords, stackx, stacktops, dDatum = 0):
        y0 = self._getStackTop(xcoords, stackx, stacktops)
        box.shiftDatum(y0 + dDatum)
        stackx.append(xcoords)           
        stacktops.append((y0 + dy))

    def _checkInStack(self,   xCurrent     :list[float, float], 
                              stackRanges  :list[list[float, float]]):
        """
        Checks all the stacks to seee if the current range is within the stack.
        
        """
        
        # Check all the stacks to see if the current stack is 
        inStack = False
        Nloads = len(stackRanges)
        for ii in range(Nloads):
            localInd = Nloads - 1 - ii
            x1, x2  = stackRanges[localInd]
            if self._checkIfInRange(xCurrent[0], x1, x2): # left side
                return  True, localInd
            if self._checkIfInRange(xCurrent[1], x1, x2): # right side
                return  True, localInd
            
            # Stack boxes that are directly on top of eachother.
            # We need both to be true so boxes side by side do not stack
            if (xCurrent[0] == x1) and (xCurrent[1] == x2): # right side
                return  True, localInd
        return inStack, None         
                
    def _getStackTop(self,   xCurrent     :list[float, float], 
                             stackRanges  :list[list[float, float]], 
                             currentY     :list[list[float, float]]):
        """
        Look at all of the current forces on the side in question.
        
        Starting at the top of the force stack, check each force to see if
        it intersects with any other forces.
        """
        
        inStack, localInd = self._checkInStack(xCurrent, stackRanges)
        if inStack == True:
            return currentY[localInd]       
        
        return 0

def _getSigns(forces):
    """
    Safely gets the signs in a way that won't result in dividing by zero.

    Returns
    -------
    None.

    """
    tmpForces = np.copy(forces)
    inds = np.where(tmpForces == 0)
    tmpForces[inds] = 1 
    signs = forces / np.abs(tmpForces)
    return signs   
    
def _setForceVectorLengthEle(boxes:list[EleLoadBox], vectScale = 1):
    """
    Gets the force vector length in terms of the drawing units.
    Force vectors will have a static component that doesn't change,
    and a dynamic component that adapts to the magnitude of forces.
    
    The output plotting forces are in the direction they act.
    
    The element load plotting does not work with non-vertical loads.

    """
    fscale0 = 0.4
    fstatic0 = 0.3
    
    forces = np.array([box.y for box in boxes])
    boxesOut = [None]*len(boxes)
    
    Fmax = np.max(np.abs(forces))

    # Get the sign of the maximum force. Ignores loads with sign changes
    signs = _getSigns(forces)
    
    # Find all force that are zero. These should remain zero
    Inds0 = np.where(np.abs(forces) == 0)
    
    # Plot the static portion, and the scale port of the force
    fscale = fscale0*abs(forces) / Fmax
    fstatic = fstatic0*np.ones_like(forces)
    fstatic[Inds0[0], Inds0[1]] = 0 # don't move the bottom of the plot!
    fplot =  ((fscale + fstatic) * signs)*vectScale
    
    for ii in range(len(boxes)):
        boxOld = boxes[ii]
        
        dy = fplot[ii][1] - fplot[ii][0]
        # We scale fout appropriately and calcualte a new fint
        fout_fscale  = fscale0*(np.array(boxOld.fout) / Fmax)
        signs        = _getSigns(fout_fscale)
        fout_plot    =  ((abs(fout_fscale) + fstatic0) * signs)*vectScale
        fint         = (fout_plot - fplot[ii][0]) / dy
        boxesOut[ii] = EleLoadBox(boxOld.x, fplot[ii], list(fint))
    
    return boxesOut       

class BeamPlotter2D:
        
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
        
        L           = beam.getLength()       
        xscale      = L  / self.figsize
        self.xscale = xscale
        baseSpacing = self.beam.getLength() / self.xscale
        
        self.plotter:basic.BasicDiagramPlotter = basic.BasicDiagramPlotter(L=L)
        self.plotter.setEleLoadLineSpacing(baseSpacing)
   
        xlims = beam.getxLims()
        self.xmin = xlims[0]
        self.xmax = xlims[1]
                
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
        
        pfplot, efplot = None, None
        if self.beam.pointLoads:
            pfplot = self.plotPointForces()
        if self.beam.pointLoads and plotLabel:
            self.plotPointForceLables(pfplot, labelForce, plotForceValue)
        if self.beam.eleLoads:
            efplot, xcoords = self.plotEleForces()
        if self.beam.eleLoads and plotLabel:
            self.plotDistForceLables(efplot, xcoords, labelForce, plotForceValue)
        
        if plotLabel:
            self.plotLabels()
    
        self.plotBeam()
        
        if (not (pfplot is None)) or (not (efplot is None)):
            self._adjustPlot(pfplot, efplot)
            

    def _adjustPlot(self, pfplot, efplot):
        if (pfplot is None):
            pfplot = (0)
        if (efplot is None):
            efplot = (0)
            
        fmax = max(np.max(pfplot), np.max(efplot))
        fmin = min(np.min(pfplot), np.min(efplot))
        if fmin < self.ylimsPlot[0]:
            self.ylimsPlot[0] = fmin
        if self.ylimsPlot[1] < fmax:
            self.ylimsPlot[1] = fmax
                
        self.ax.set_ylim(self.ylimsPlot)
       
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
            labelBase = force.label
            # labelBase = self.beam.nodes[force.nodeID - 1].label
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

    def _plotEleForce(self, box:EleLoadBox):
        
        Py = box.fout
        
        if (Py[0] == 0) and (Py[1] == 0):
            print("WARNING: Plotted load has no vertical component.")            
        
        if box.isConstant:
            self.plotter.plotElementDistributedForce(self.ax, box)
        else:
            self.plotter.plotElementLinearForce(self.ax, box)
    
    def normalizeData(self, data):
        return (data - np.min(data)) / (np.max(data) - np.min(data))
    
    def _getLinFint(self, Ptmp):
        """
        Contains the logic for finding the signs of Fint
        """
                
                
        # fintTemp = list(self.normalizeData(Ptmp))
        # If both are on the positive side
        if 0 < np.sign(Ptmp[0]) and 0 < np.sign(Ptmp[1]):
            
            if Ptmp[0] < Ptmp[1]:
                fintTemp = [Ptmp[0]/Ptmp[1], 1]
            elif Ptmp[0] == Ptmp[1]: # If equal the load acts like a constant load
                fintTemp = [1, 1]
            else:
                fintTemp = [1, Ptmp[1]/Ptmp[0]]
            Ptmp = [0, max(Ptmp)]
                
        # If both are on the negative side side
        elif  np.sign(Ptmp[0]) < 0 and np.sign(Ptmp[1]) < 0 :
            
            if Ptmp[0] < Ptmp[1]:
                fintTemp = [0, Ptmp[1]/Ptmp[0]]
            elif Ptmp[0] == Ptmp[1]: # If equal the load acts like a constant load
                fintTemp = [0, 0]
            else:
                fintTemp = [1-Ptmp[0]/Ptmp[1], 0]
            Ptmp = [min(Ptmp), 0]
                
        # If the inputs change sign, just use the normalized value.
        else:
            fintTemp = list(self.normalizeData(Ptmp))   
        return Ptmp, fintTemp
                    
    def _getEleForceBoxes(self):
        """
        Handles all the logic of generating stacked object positions.
        
                
        """
        
        eleBoxes = []        
        
        for load in self.beam.eleLoads:
            xDiagram = [load.x1 / self.xscale, load.x2 / self.xscale]     
            
            if isinstance(load, EleLoadDist):  # Constant Load
                # Adapt the load so it's a 2D vector
                Ptmp = [0, -load.P[1]] #!!! The sign is flipped to properly stack
                if -load.P[1] < 0:  #!!! The sign is flipped to properly stack
                    fintTemp = [0, 0] # start at the bottom if negative
                else:
                    fintTemp = [1, 1] # start at the top if negative
                eleBoxes.append(EleLoadBox(xDiagram, Ptmp, fintTemp))
            # Arbitary Distributed Load between two points
            elif isinstance(load, EleLoadLinear):   
                Ptmp = -load.P[1]  #!!! The sign is flipped to properly stack
                
                Ptmp, fintTemp = self._getLinFint(Ptmp)               
                eleBoxes.append(EleLoadBox(xDiagram, Ptmp, fintTemp))
        
        eleBoxes    = _setForceVectorLengthEle(eleBoxes, vectScale = 0.4)
        stacker     = Boxstacker(eleBoxes)
        eleBoxes    = stacker.setStackedDatums()
        
        return eleBoxes
                     
    def plotEleForces(self):
        """
        Plots all distributed forces. Only vertical forces can be plotted.
        If a horizontal component is supplied to the force, it is not included
        in the plot.
        """

        eleBoxes =  self._getEleForceBoxes()
        for box in eleBoxes:
            self._plotEleForce(box)
        
        fplot       = [box.y for box in eleBoxes]
        xcoords     = [box.x for box in eleBoxes]
                        
        return fplot, xcoords                     

def plotBeamDiagram(beam, plotLabel = True, labelForce = False, 
                    plotForceValue = False, 
                    units = 'environment') -> (Figure, Axes):
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



