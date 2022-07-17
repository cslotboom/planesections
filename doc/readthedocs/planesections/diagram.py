# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 20:57:19 2022

@author: Christian

Problems - make sure that hatching is consistent at different beam scales.
Make sure that units support imperial

Hatching should be similar to beam size?

"""

import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch

from abc import ABC, abstractmethod
from planesections import diagramUnits

# hatches = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']



# fig, axs = plt.subplots(2, 5, constrained_layout=True, figsize=(6.4, 3.2))

# =============================================================================
# Archetype classes
# =============================================================================


"""
These archetype classes represent what a 3rd part tool will need to have
to plug into the functions.
They should define all the meaningful interfaces/abstractions in the class.

"""

"""
Not used properly right now, but ideally this is defined only in one place.
"""
fixities  = {'free':[0,0,0], 'roller': [0,1,0], 'pinned':[1,1,0], 'fixed':[1,1,1]}





# =============================================================================
# 
# =============================================================================

class BeamDiagram:
    """
    Manages the beam diagram and it's current state.
    """
    
    
    def _initPlot():
        pass
    
    @abstractmethod
    def plotPin():
        pass

    @abstractmethod
    def plotRoller():
        pass
    
    @abstractmethod
    def plotFixed():
        pass
    
class BasicBeamDiagram(BeamDiagram):
    
    """
    Manages the beam diagram and it's current state.
    In theory, this could manage plots for frame systems as well.

    """
    
    def __init__(self, scale = 1, supScale = 0.8):

        self.lw = 1 * scale
        self.scale = scale # Scales all drawing elements
        
        # changes the offset from the point in x/y
        self.labelOffset = 0.1*scale
        
        # Pin geometry variables
        self.r = 0.08*scale*supScale
        self.hTriSup = 0.3*scale*supScale
        self.wTriSup = 2*self.hTriSup
        
        self.hFixedRect = 0.2*scale*supScale
        self.marginFixedSup = 0.2*scale*supScale
        self.hatch = '/'* int((3/(scale*supScale)))
        self.wRect   = self.wTriSup + self.marginFixedSup
        
        self.hRollerGap = self.hFixedRect / 4

        self.fig = None
        self.ax = None
        self.y0 = 0

        self.supportPlotOptions = {'fixed':self.plotFixed, 
                                   'pinned':self.plotPinned,
                                   'roller':self.plotRoller,
                                   'free':self.plotFree}

    def _initPlot(self, figSize, xlims, ylims, dpi = 300):
        
        dy = ylims[-1] - ylims[0]
        self.fig, self.ax = plt.subplots(constrained_layout=True, figsize=(figSize, dy), dpi=300)
        self.ax.axis('equal')
        self.ax.axis('off')        
        self.ax.set_xlim(xlims)
        self.ax.set_ylim(ylims)
        
        
    def plotBeam(self, xy0, xy1):
        self.ax.plot([xy0[0], xy1[0]], [xy0[1], xy1[1]], lw = self.lw*2, c='black')

    def returnCurrentPlot(self):
        """
        Returns the figure in the current state.
        """
        return self.fig, self.ax


    def _getPinSupportCords(self, xy0, scale):
        """
        Gets gets the coordinants for the triangle, rectangle, and white
        line in the pin connector.

        """

        xyTri1 = [xy0[0] - self.wTriSup/2, xy0[1] - self.hTriSup]
        xyTri2 = [xy0[0] + self.wTriSup/2, xy0[1] - self.hTriSup]
        xyTri  = [xyTri1, xyTri2, xy0]
        
        xy0Rect = [xy0[0] - self.wRect/2, xy0[1] - self.hTriSup - self.hFixedRect]

        xyLine = [[xy0[0] - self.wRect/2, xy0[0] + self.wRect/2],
                  [xy0[1] - self.hTriSup - self.hFixedRect, xy0[1] - self.hTriSup - self.hFixedRect]]
        
        return xyTri, xy0Rect, xyLine

    def _getPointLoadCoords(self, xy0):
        pass

    def _plotPinGeom(self, xy0, xyTri, xy0Rect, xyLine):
        """
        The pin connection consists of four components:
            The triangle face
            The hatched rectangle
            a white line to cover the bottom of the hatched rectagle
            a circle

        """
        self.ax.add_patch(Polygon(xyTri, fill=False, lw = self.lw))
        self.ax.add_patch(Rectangle(xy0Rect, self.wRect, self.hFixedRect, ec='black', fc='white', hatch=self.hatch, lw = self.lw))
        self.ax.plot(xyLine[0], xyLine[1], c = 'white', lw = self.lw)
        # self.ax.add_patch(Circle(xy0, self.r, facecolor='w', ec = 'black'))
        self.ax.add_patch(Circle(xy0, self.r, facecolor='white', ec = 'black', fill=True, zorder=2, lw = self.lw))
                
    def plotPinned(self, xy0, **kwargs):
        """
        Plots a pin support at the location xy0. Pins are made up of the 
        fixed base rectangle, a triangle support, and the

        """
        xyTri, xy0Rect, xyLine = self._getPinSupportCords(xy0, self.scale)
        self._plotPinGeom(xy0, xyTri, xy0Rect, xyLine)
        
        return

    def _getRollerSupportCords(self, xy0, scale):
        """
        Adds the patches for a roller support geometry.
        TODO: I don't like how this instance uses similar code to the getPin
        method. Consider finding a way to standarize the coordinant positions.
        
        """
        # 
        lineOffset = self.hFixedRect/10 
        
        # The gap starts a the botom-left surface of the roller
        xy0gap = [xy0[0] - self.wRect/2, xy0[1] - self.hTriSup + lineOffset]
        
        # The line starts at the top of the gap
        xyRollerLine = [[xy0[0] - self.wRect/2, xy0[0] + self.wRect/2],
                        [xy0[1] - self.hTriSup + self.hRollerGap + lineOffset, 
                         xy0[1] - self.hTriSup + self.hRollerGap + lineOffset]]
        
        return xy0gap, xyRollerLine
    
    def _addRollerGeom(self, xy0gap, xyRollerLine):
        self.ax.add_patch(Rectangle(xy0gap, self.wRect, self.hRollerGap, color='white', lw = self.lw))
        self.ax.plot(xyRollerLine[0], xyRollerLine[1], color = 'black', lw = self.lw)

    def plotRoller(self, xy0, **kwargs):
        """
        Rollers use the same basic support as a pin, but adds some lines to 
        
        Plots a pin support at the location xy0. Pins are made up of the 
        fixed base rectangle, a triangle support, and the

        """
        # print(self)
        xyTri, xy0Rect, xyLine = self._getPinSupportCords(xy0, self.scale)
        self._plotPinGeom(xy0, xyTri, xy0Rect, xyLine)
        xy0gap, xyRollerLine = self._getRollerSupportCords(xy0, self.scale)
        self._addRollerGeom(xy0gap, xyRollerLine)



    def _getFixedSupportCords(self, xy0, isLeft=True):
        """
        Gets gets the coordinants for the triangle, rectangle, and white
        line in the pin connector.

        """
        
        if isLeft:
            xy0Rect = [xy0[0] - self.hFixedRect, xy0[1] - self.wRect/2]
    
            xyLine = [[xy0[0], xy0[0] - self.hFixedRect, xy0[0] - self.hFixedRect, xy0[0]],
                      [xy0[1] + self.wRect/2, xy0[1] + self.wRect/2,
                       xy0[1] - self.wRect/2, xy0[1] - self.wRect/2]]
        else:
            xy0Rect = [xy0[0], xy0[1] - self.wRect/2]
    
            # xy0Rect = [xy0[0] - self.hFixedRect, xy0[1] - self.wRect/2]
    
            xyLine = [[  xy0[0],xy0[0] + self.hFixedRect,xy0[0] + self.hFixedRect, xy0[0]],
                      [xy0[1] + self.wRect/2, xy0[1] + self.wRect/2,
                       xy0[1] - self.wRect/2, xy0[1] - self.wRect/2]]
            
        return  xy0Rect, xyLine   

    def plotFixed(self, xy0, isLeft = True):
        """
        Plots a pin support at the location xy0. Pins are made up of the 
        fixed base rectangle, a triangle support, and the

        """
        xy0Rect, xyLine = self._getFixedSupportCords(xy0, isLeft)
        self.ax.add_patch(Rectangle(xy0Rect, self.hFixedRect, self.wRect, ec='black', fc='white', hatch=self.hatch, lw = self.lw))
        self.ax.plot(xyLine[0], xyLine[1], c = 'white', lw = self.lw)

    def plotFree(self, xy0, **kwargs):
        pass

    def plotPointForce(self, x, y, Px, Py, baseWidth = 0.03, c='C0'):
        """
        Note, Px and Py must be normalized!
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.arrow.html
        
        x and y are the start point of the arrow.
        
        """
        
        width = baseWidth*self.scale
        hwidth = width* 5
        length = width* 5
        self.ax.arrow(x, y, Px, Py, width=width, head_width = hwidth, head_length = length, 
                      edgecolor='none', length_includes_head=True, fc=c)
        
    def plotPointMoment(self, x0, positive=False):       
        r = 0.15
        rInner = r / 5
        arrow = r / 4
        rotationAngle = 30
        arclength = 1 * 2*np.pi
        
        # Get base rectangle point.
        t = np.linspace(0.0, 0.8, 31) * arclength        
        x = r*np.cos(t)
        y = r*np.sin(t)
        
        if positive:
            ind = -1
            x0c = x[ind]
            y0c = y[ind]
            xarrow =  [x0c - arrow*1.2, x0c, x0c - arrow*1.2]
            yarrow =  [y0c + arrow*1.5, y0c, y0c - arrow*1.5]            
            
        if not positive:
            ind = 0
            x0c = x[ind]
            y0c = y[ind]
            xarrow =  [x0c - arrow*1.5, x0c, x0c + arrow*1.5]
            yarrow =  [y0c + arrow*1.2, y0c, y0c + arrow*1.2]   

        # Define a rotation matrix
        theta = np.radians(rotationAngle)
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c, -s), (s, c)))
        
        # rotate the vectors
        xy = np.column_stack([x,y])
        xyArrow = np.column_stack([xarrow, yarrow])
        xyOut = np.dot(xy, R.T)
        xyArrowOut = np.dot(xyArrow, R.T)
        
        # Shift to the correct location
        xyOut[:,0] += x0
        xyArrowOut[:,0] += x0
        xy0 = [x0,0]

        self.ax.add_patch(Circle(xy0, rInner, facecolor='C0', fill=True, zorder=2, lw = self.lw))

        plt.plot(xyOut[:,0], xyOut[:,1])
        plt.plot(xyArrowOut[:,0], xyArrowOut[:,1], c='C0')

                
    def plotVerticalLineLoad(self, x1, x2, q, y0 = 0, spacing = 1, barC = 'grey'):
        """
        The line load is compsed of the top bar, two side bars, and a series
        of arrows spaced between the side bars. Only vertical line loads
        are supported.

        """
        barWidth = 1
        N = int((x2 - x1) / spacing) + 1
        xVals = np.linspace(x1, x2, N)
 
        if q < 0: # if the dirrection is negative, start high and point down
            ystart = y0 - q # the positon of arrow start
        else:
            ystart = y0 # the positon of arrow start
                        
        xbar = [x1, x2]
        yBarS = [ystart, ystart]
        yBarE = [ystart+q, ystart+q]
        plt.plot(xbar, yBarS, linewidth = barWidth, c = barC)
        plt.plot(xbar, yBarE, linewidth = barWidth, c = barC)
        
        for ii in range(N):
            x = xVals[ii]
            self.plotPointForce(x, ystart, 0, q, baseWidth = 0.015, c = barC)
        
    def plotLabel(self, xy0, label):
        x = xy0[0] + self.labelOffset
        y = xy0[1] + self.labelOffset
        self.ax.text(x, y, label, {'size':12*self.scale})
        # self.labelOffset
        
    # def plotForceLabel(self, xy0, label):
    #     x = xy0[0] + self.labelOffset
    #     y = xy0[1] + self.labelOffset
    #     self.ax.text(x, y, label, {'size':12*self.scale})


# =============================================================================
# 
# =============================================================================



class BeamPlotter2D:
    def __init__(self, beam, figsize = 8, units = 'environment'):
        """
        Used to make a diagram of the beam. Only certain fixities are supported
        for plotting, including free, roller (support only in y), pinned (support in x and y),
        and fixed (support in x/y/rotation).
        Only certain forces are supported for plotting - for distrubuted
        forces only the y component of the beam can be plotted.
        Mixed Forces, those that contain a combination of Px/Py/Moment will 
        not be plotted
     
        Note, the diagram has been rescaled so it's length in the digram 
        isn't it's analysis lenght.
        This is to make consistent plotting easier across a number of beam sizes,
        however, the matplotlib objects in the plot have different value than 
        the actual beam.
        
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
        xscale = beam.getLength()  / self.figsize
        self.xscale = xscale
        self.plotter = BasicBeamDiagram()
   
        xlims = beam.getxLims()
        self.xmin = xlims[0]
        self.xmax = xlims[0]
                
        self.xlimsPlot = [(xlims[0] - L/20) / xscale, (xlims[1] + L/20) / xscale]
        self.ylimsPlot = [-L/10 / xscale, L/10 / xscale]
        
        self.plottedNodeIDs = []
        
        
    def plotBeam(self):
        xlims   = self.beam.getxLims()
        xy0     = [xlims[0]  / self.xscale, 0]
        xy1     = [xlims[1]  / self.xscale, 0]        
        d       = self.beam.d
        self.plotter.plotBeam(xy0, xy1)
               
    def plotSupports(self):
        for node in self.beam.nodes:
            fixityType  = node.getFixityType()
            x = node.getPosition()
            """
            This makes some big assumptions about the shape of the system.
            """
            kwargs = {}
            if fixityType == 'fixed' and x == self.xmin:
                kwargs =  {'isLeft':True}
                    
            if fixityType == 'fixed' and not x == self.xmin:
                kwargs  = {'isLeft':False}                
            
            xy = [x / self.xscale, 0]
            
            # plot the appropriate option without an if statement!
            self.plotter.supportPlotOptions[fixityType](xy, **kwargs)

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
        
        self.plotter._initPlot(self.figsize, self.xlimsPlot, self.ylimsPlot)
        self.plotSupports()
        if self.beam.pointLoads:
            fplot = self.plotPointForces()
        if self.beam.pointLoads and plotLabel:
            self.plotPointForceLables(fplot, labelForce, plotForceValue)
            
        if self.beam.eleLoads:
            fplot, xcoords = self.plotEleForces()
        if self.beam.eleLoads and plotLabel:
            self.plotDistForceLables(fplot, xcoords, labelForce, plotForceValue)
            
        if plotLabel:
            # print('here')
            self.plotLabels()
        self.plotBeam()
        
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
                self.plotter.plotLabel(xy, label)
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

    def _checkIfLabelPlotted(self, nodeID):
        check = nodeID in self.plottedNodeIDs
        return check
        
    def _addLabelToPlotted(self, nodeID):
        self.plottedNodeIDs.append(nodeID)

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
            
            if self._checkIfLabelPlotted(force.nodeID) != True:
                self.plotter.plotLabel(xy, label)
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
            self.plotter.plotLabel(xy, label)              

    def _getForceVectorLength(self, forces, vectScale = 1):
        """
        Gets the corce vector length in terms of the drawing units.
        Force vectors will have a static component that doesn't change,
        and a dynamic component that adapts to the magnitude of forces.
        
        The output plotting forces are in the direction they act.

        """
        # Normalize forces
        forces = np.array(forces)
        signs = np.sign(forces)
        Fmax   = np.max(np.abs(forces), 0)
        
        # Avoid dividing by zero later
        Inds   = np.where(np.abs(Fmax) == 0)
        Fmax[Inds[0]] = 1
        
        # Find all force that are zero. These should remain zero
        Inds0 = np.where(np.abs(forces) == 0)
        
        # Plot the static portion, and the scale port of the force
        fscale = 0.4*abs(forces) / Fmax
        fstatic = 0.3*np.ones_like(forces)
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
        fplot  = self._getForceVectorLength(forces)
        NLoads = len(forces)
        
        for ii in range(NLoads):
            Px, Py, Mx = fplot[ii]
            x = xcoords[ii]
            if (Px == 0 and Py ==0): # if it's a moment, plot it as a moment
                if Mx < 0:
                    postive = True
                else:
                    postive = False
                self.plotter.plotPointMoment(x, postive)
            else:
                self.plotter.plotPointForce(x - Px, -Py, Px, Py)
                
        return fplot

    def plotEleForces(self):
        """
        Plots all distributed forces. Only vertical forces can be plotted.
        If a horizontal component is supplied to the force, it is not included
        in the plot.
        """
        
        # The spacing between force lines
        spacing = self.beam.getLength() / 25 / self.xscale
        forces  = []
        xcoords = []        
        for force in self.beam.eleLoads:
            forces.append(force.P)
            xcoords.append([force.x1 / self.xscale, force.x2 / self.xscale])
        
        fplot = self._getForceVectorLength(forces, vectScale = 0.4)
        ycoords = self._getStackedPositions(xcoords, fplot)
                
        NLoads = len(forces)
        for ii in range(NLoads):       
            Px, Py = fplot[ii]
            x1, x2 = xcoords[ii]
            y1 = ycoords[ii] # y1 is the start point of the arrow
            
            if (Px != 0 ):
                print("WARNING: A force with an X component is being used, but plotting isn't supported for this force type.")
            if (Py == 0):
                print("WARNING: Distributed load has no vertical component.")            
            else:
                # This is a little akward, but Py is added to account for the offset of -Py in the base funciton.
                self.plotter.plotVerticalLineLoad(x1, x2, Py, y1 + Py, spacing=spacing)
        return fplot, xcoords
   
    
    def _getStackedPositions(self, xcoords: list[list[float]], fplot):
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
        fplotOut = np.zeros_like(fplot)
        fplotOut[:] = fplot

        # the current x and y points being plotted.        
        plottedxCoords = []
        plottedyCoords = []
        plottedDyCoords = []
        
        # start at the widest items and plot them first
        for ind in sortedInds:
            dy = fplotOut[ind][1]
            y0 = self._getStackedDatum(xcoords[ind], plottedxCoords, plottedyCoords)

            ycoords[ind] =  y0 - dy
            plottedxCoords.append(xcoords[ind])           
            plottedyCoords.append(ycoords[ind])
        return ycoords
    
    def _checkIfInRange(self, xtest, x1,x2):
        if (x1 < xtest) and (xtest < x2):
            return True
        return False
    
    def _getStackedDatum(self, xCurrent, currentRanges, plottedY):
        """
        Starting at the top of the force stack, check each force to see if
        it intersects with any other forces.
        """
        
        Npoint = len(currentRanges)
        for ii in range(Npoint):
            localInd = Npoint - 1 - ii
            x1, x2  = currentRanges[localInd]
            if self._checkIfInRange(xCurrent[0], x1, x2):
                    return plottedY[localInd]
            if self._checkIfInRange(xCurrent[0], x1, x2):
                    return plottedY[localInd]       
        return 0
                       

def plotBeamDiagram(beam, plotLabel = True, labelForce = True, plotForceValue = False, units = 'environment'):
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
    
    The resulting diagram is a matplotlib figure that can be further manipulated.

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
    return diagram.plotter.fig, diagram.plotter.ax




# class NodeArchetype:
#     """
#     Represents a node/point of interst on the diagram.
#     """
#     @abstractmethod
#     def getFixityType():
#         """
#         Gets the fixity type used.
#         Currently supported - free, roller, pin, fixed.
#         """
#         pass
    
#     @abstractmethod
#     def getPosition():
#         """
#         Gets the x position of the node.
#         Currently supported - roller, pin, fixed.
#         """

#         pass
    
#     @abstractmethod
#     def getLabel():
#         """
#         Returns the label that has been assigned to the node/
#         ???:
#             what values are supported??
#         """
#         pass    
    


# class BeamArchetype:
#     """
#     Archetype class of data beams need in order to use make use of the beam
#     diagram class
    
#     ???:
#         Should nodes be given a required internal naming convention?
#     """
#     nodes = []
#     NodeArchetype = None
#     forces = []
#     distForces = []

    
    
#     @abstractmethod
#     def getNodes():
#         """
#         Returns all noed objects in the beam.
#         """
#         pass
    
#     @abstractmethod
#     def getForces():
#         """
#         Gets all applied point Loads.
#         """        
#         pass
    
#     @abstractmethod
#     def getDistForses():
#         """
#         Gets all applied distrubuted Loads.
#         """ 
#         pass    
    
    
#     @abstractmethod
#     def setNodeArchetype():
#         """
#         Sets the archetype method used to create new nodes.
#         """ 
#         pass
    
#     @abstractmethod
#     def addNode(self, xCoord, fixity, label=None):
#         """
#         Adds a new node to the model.
#         """ 
#         pass    

        
        
        


# ???
# call point force?

# class ForceArchetype:
#     """
#     Represents a force applied to a single node
#     """
    
#     @abstractmethod
#     def getConnectedNode():
#         """
#         """
#         pass
    
#     @abstractmethod
#     def getMagnitudes():
#         """
#         Returns the magnitude of force at each of the connected nodes
#         """
#         pass   
    
     
#     @abstractmethod
#     def getLabelNodes():
#         """
#         Returns the nodes that are labeled
#         """
#         pass         

# class DistrubtedForceArchetype:
#     """
#     Represents a force distributed across multiple nodes, i.e. uniform, etc
#     """
    
#     @abstractmethod
#     def getConnectedNode():
#         """
        
#         """
#         pass
    
#     @abstractmethod
#     def getMagnitudes():
#         """
#         Returns the magnitude of force at each of the connected nodes
#         """
#         pass   
    
     
#     @abstractmethod
#     def getLabelNodes():
#         """
#         Returns the nodes that are labeled
#         """
#         pass      
    
    


# =============================================================================
# Implementations.
# =============================================================================


# class Node(NodeArchetype):
#     """
#     A concrete implementation for a class that represents a node/point of 
#     interst on the diagram.
#     """
    
#     def __init__(self, xCoord, fixity, label):
#         self.x = xCoord
#         self.fixity = fixity
#         self.label = label
    
    
#     def getFixityType(self):
#         """
#         Gets the fixity type used.
#         Currently supported - free, roller, pin, fixed.
#         """
#         return self.fixity
    
#     def getPosition(self):
#         """
#         Gets the x position of the node.
#         Currently supported - roller, pin, fixed.
#         """

#         return self.x
    
#     def getLabel(self):
#         """
#         Returns the label that has been assigned to the node/
#         ???:
#             what values are supported??
#         """
#         return self.label  


# class Beam(BeamArchetype):
    
#     def __init__(self):
#         """
#         The concrete implementaiton of the beam class.

#         """
#         nodes = []
#         NodeArchetype = None
#         forces = []
#         distForces = []
        
#         self.setNodeArchetype()
    
#     def getNodes(self):
#         """
#         Returns all noed objects in the beam.
#         """
#         return self.nodes
    
#     def getForces(self):
#         """
#         Gets all applied point Loads.
#         """        
#         return self.forces
    
#     def getDistForses(self):
#         """
#         Gets all applied distrubuted Loads.
#         """ 
#         print('NOT SUPPORTED YET')            
        
        
#     def addNode(self, xCoord, fixity, label=None):
#         NewNode = self.nodeArchetype(xCoord, fixity,label)
#         self.nodes.append(NewNode)
    
#     def setNodeArchetype(self, nodeArchetype:NodeArchetype = Node):
#         """
#         Used to set the type of node class used. The node should inherit from
#         the nodeArhetype class.
#         """
#         self.nodeArchetype = nodeArchetype                
    

