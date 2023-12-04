# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 20:57:19 2022

@author: Christian

"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Polygon, Circle

from .abstract import AbstractDiagramElement
from dataclasses import dataclass       
        
@dataclass
class supportDiagramOptions:
    
    # GlobalParameters
    lw:float
    scale:float
    supScale:float
    
    #
    r:float
    
    # Parameters for the triangle
    hTriSup:float
    wTriSup:float
    
    # Parameters for the rectangle below the support
    hFixedRect:float
    marginFixedSup:float
    hatch:str
    wRect:float
    
    # Roller
    lineOffset_roller:float
    hRollerGap:float
    y0:float    
    

@dataclass
class PointLoadOptions:
    
    # GlobalParameters
    lw:float
    c:float # colour
    arrowWidth:float
     

@dataclass
class MomentPointLoadOptions:
    
    # GlobalParameters
    lw:float
    c:float # colour
    arrowWidth:float
    
    # Circle parameters
    r:float
    rotationAngle:float



@dataclass
class DistLoadOptions:
    
    # GlobalParameters
    baseWidth:float
    c:float # colour
    arrowWidth:float
        
    spacing:float
    barWidth:float       



@dataclass
class LinLoadOptions:
    
    # GlobalParameters
    baseWidth:float
    c:float # colour
    arrowWidth:float
        
    spacing:float
    barWidth:float       
    minLengthCutoff:float



@dataclass
class LabelOptions:
    labelOffset:float 
    textsize:float = 12

    def __post_init__(self):
        self.textKwargs = {'size':self.textsize}

    
@dataclass
class BeamOptions:
    lw:float 
    c:float

class BasicOptionsDiagram:
    def __init__(self, scale = 1, supScale = 0.8):
        
        """
        A class that contains appearance options for the basic beam diagram.
        Scale affects thickness of drawing elements..!
        
        """
        
        self.lw = 1 * scale
        self.scale = scale # Scales all drawing elements
        self.supScale = supScale # Scales all drawing elements
        
        # Beam Propreties
        self.lw_beam = 2 * scale
        self.c_beam = 'black'
        
        # Point Load Propreties
        self.w_PointLoad = 0.03 * scale
        self.c_PointLoad = 'C0'
        self.c_PointLoadDist = 'grey'
        # changes the offset from the point in x/y
        self.labelOffset = 0.1*scale
        
        # Pin support geometry variables
        self.r = 0.08*scale*supScale
        self.hTriSup = 0.3*scale*supScale
        self.wTriSup = 2*self.hTriSup
        
        # Parameters for the rectangle below the pin support
        self.hFixedRect = 0.2*scale*supScale
        self.marginFixedSup = 0.2*scale*supScale
        self.hatch = '/'* int((3/(scale*supScale)))
        self.wRect   = self.wTriSup + self.marginFixedSup
        
        self.lineOffset_roller = self.hFixedRect / 10 
        self.hRollerGap = self.hFixedRect / 4
        self.y0 = 0

        # Point Load
        self.lw_pL = 0.03 * scale # The width of the
        # self.lw_pLbaseWidth = 0.01 * scale # The width of the
        self.arrowWidth = 5*self.lw_pL

        # Moment Point Load
        self.r_moment = 0.15
        self.rotationAngle = 30
        self.c_moment ='C0'
        
        # Distributed Load Propreties
        self.c_dist_bar = 'grey'
        self.spacing_dist = (1/20)
        self.barWidth = 1*scale
        
        self.lw_pL_dist = 0.015
        self.arrowWidth_pL_dist = 5*self.lw_pL_dist
        
        #Linear Distributed Load Options
        self.minLengthCutoff = 0.075*self.scale
        
        
        
        # label Options
        self.labelOffset = 0.1*scale
        self.textSize = 12*scale
    
    def getSupportDiagramOptions(self):
        
        args = [self.lw, self.scale, self.supScale, 
                self.r, self.hTriSup,self.wTriSup, self.hFixedRect, 
                self.marginFixedSup, self.hatch, self.wRect, 
                self.lineOffset_roller,
                self.hRollerGap, self.y0 ]
        
        return supportDiagramOptions(*args)
    
    def getPointLoadOptions(self):
        
        args = [self.lw_pL, self.c_PointLoad, self.arrowWidth]
        return PointLoadOptions(*args)
    
    def getPointLoadDistOptions(self):
        args = [self.lw_pL_dist, self.c_dist_bar, self.arrowWidth_pL_dist]
        return PointLoadOptions(*args)

    
    def getMomentPointLoadOptions(self):
        
        args = [self.lw_pL, self.c_moment, self.arrowWidth, self.r_moment, 
                self.rotationAngle]
        
        return MomentPointLoadOptions(*args)

    def getDistLoadOptions(self):
        args = [self.lw, self.c_dist_bar, self.arrowWidth, self.spacing_dist,
                self.barWidth]
        
        return DistLoadOptions(*args)
    
    def getLinLoadOptions(self):
        args = [self.lw, self.c_dist_bar, self.arrowWidth, self.spacing_dist,
                self.barWidth, self.minLengthCutoff]
        
        return LinLoadOptions(*args)    
    
    
    def getLabelOptions(self):
        
        args = [self.labelOffset, self.textSize]        
        
        return LabelOptions(*args)


    def getBeamOptions(self):
        args = [self.lw_beam, self.c_beam]
        return BeamOptions(*args)

     
class DiagramEleFreeSupport:
    
    def __init__(self, xy, diagramOptions:supportDiagramOptions):
        pass

    def plot(self, ax):
        """
        Plots a pin support at the location xy0. Pins are made up of the 
        fixed base rectangle, a triangle support, and the

        """        
        
        pass   

class DiagramElePinSupport(AbstractDiagramElement):
    
    def __init__(self, xy0, diagramOptions:supportDiagramOptions):
        self.xy0 = xy0
        self.options = diagramOptions

    def _getPinSupportCords(self, xy0, scale):
        """
        Gets gets the coordinants for the triangle, rectangle, and white
        line in the pin connector.

        """
        wTriSup     = self.options.wTriSup
        hTriSup     = self.options.hTriSup
        wRect       = self.options.wRect
        hFixedRect  = self.options.hFixedRect
                
        xyTri1 = [xy0[0] - wTriSup/2, xy0[1] - hTriSup]
        xyTri2 = [xy0[0] + wTriSup/2, xy0[1] - hTriSup]
        xyTri  = [xyTri1, xyTri2, xy0]
        
        xy0Rect = [xy0[0] - wRect/2, xy0[1] - hTriSup - hFixedRect]

        xyLine = [[xy0[0] - wRect/2, xy0[0] + wRect/2],
                  [xy0[1] - hTriSup - hFixedRect, xy0[1] - hTriSup - hFixedRect]]
        
        return xyTri, xy0Rect, xyLine

    def _plotPinGeom(self, ax, xy0, xyTri, xy0Rect, xyLine):
        """
        The pin connection consists of four components:
            The triangle face
            The hatched rectangle
            a white line to cover the bottom of the hatched rectagle
            a circle

        """
        # 
        lw = self.options.lw
        hatch = self.options.hatch
        wRect = self.options.wRect
        r = self.options.r
        hFixedRect = self.options.hFixedRect
        
        ax.add_patch(Polygon(xyTri, fill=False, lw = lw))
        ax.add_patch(Rectangle(xy0Rect, wRect, hFixedRect, ec='black', fc='white', hatch=hatch, lw = lw))
        ax.plot(xyLine[0], xyLine[1], c = 'white', lw = lw)
        ax.add_patch(Circle(xy0, r, facecolor='white', ec = 'black', fill=True, zorder=2, lw=lw))

    def plot(self, ax):
        """
        Plots a pin support at the location xy0. Pins are made up of the 
        fixed base rectangle, a triangle support, and the

        """        
        scale = self.options.scale
        xyTri, xy0Rect, xyLine = self._getPinSupportCords(self.xy0, scale)
        self._plotPinGeom(ax, self.xy0, xyTri, xy0Rect, xyLine)
         
class DiagramEleRollerSupport(DiagramElePinSupport):
    
    def __init__(self, xy0, diagramOptions:supportDiagramOptions):
        self.xy0 = xy0
        self.options = diagramOptions

    def _getRollerSupportCords(self, xy0, scale):
        """
        Gets gets the coordinants for the triangle, rectangle, and white
        line in the pin connector.

        """
        
        lineOffset  = self.options.lineOffset_roller
        hTriSup     = self.options.hTriSup
        hRollerGap  = self.options.hRollerGap
        wRect       = self.options.wRect
        
        # The gap starts a the botom-left surface of the roller
        xy0gap = [xy0[0] - wRect/2, xy0[1] - hTriSup + lineOffset]
        
        # The line starts at the top of the gap
        xyRollerLine = [[xy0[0] - wRect/2, xy0[0] + wRect/2],
                        [xy0[1] - hTriSup + hRollerGap + lineOffset, 
                         xy0[1] - hTriSup + hRollerGap + lineOffset]]
        
        return xy0gap, xyRollerLine

    def _plotRollerGeom(self, ax, xy0gap, xyRollerLine):
        lw = self.options.lw
        hRollerGap = self.options.hRollerGap
        wRect = self.options.wRect    
        
        ax.add_patch(Rectangle(xy0gap, wRect, hRollerGap, color='white', lw = lw))
        ax.plot(xyRollerLine[0], xyRollerLine[1], color = 'black', lw = lw)

    def plotRoller(self, ax):
        """
        Rollers use the same basic support as a pin, but adds some lines to 
        
        Plots a pin support at the location xy0. Pins are made up of the 
        fixed base rectangle, a triangle support, and the

        """
        xy0 = self.xy0
        scale = self.options.scale
        xyTri, xy0Rect, xyLine = self._getPinSupportCords(xy0, scale)
        self._plotPinGeom(ax, xy0, xyTri, xy0Rect, xyLine)
        xy0gap, xyRollerLine = self._getRollerSupportCords(xy0, scale)
        self._plotRollerGeom(ax, xy0gap, xyRollerLine)       
       

    def plot(self, ax):
        """
        Plots a pin support at the location xy0. Pins are made up of the 
        fixed base rectangle, a triangle support, and the

        """        
        
        self.plotRoller(ax)        

class DiagramEleFixedSupport(AbstractDiagramElement):
    
    def __init__(self, xy0, diagramOptions:supportDiagramOptions, 
                 isLeft=True):
        self.xy0 = xy0
        self.options = diagramOptions
        self.isLeft = isLeft

    def _getFixedSupportCords(self, xy0, isLeft):
        """
        Gets gets the coordinants for the triangle, rectangle, and white
        line in the pin connector.

        """

        wRect       = self.options.wRect
        hFixedRect  = self.options.hFixedRect
                
        if isLeft:
            xy0Rect = [xy0[0] - hFixedRect, xy0[1] - wRect/2]
    
            xyLine = [[xy0[0], xy0[0] - hFixedRect, xy0[0] - hFixedRect, xy0[0]],
                      [xy0[1] + wRect/2, xy0[1] + wRect/2,
                       xy0[1] - wRect/2, xy0[1] - wRect/2]]
        else:
            xy0Rect = [xy0[0], xy0[1] - wRect/2]    
            xyLine = [[  xy0[0],xy0[0] + hFixedRect,xy0[0] + hFixedRect, xy0[0]],
                      [xy0[1] + wRect/2, xy0[1] + wRect/2,
                       xy0[1] - wRect/2, xy0[1] - wRect/2]]
            
        return  xy0Rect, xyLine   

    def plot(self, ax):
        """
        Plots a pin support at the location xy0. Pins are made up of the 
        fixed base rectangle, a triangle support, and the

        """
        
        lw          = self.options.lw
        hFixedRect  = self.options.hFixedRect
        hatch       = self.options.hatch
        wRect       = self.options.wRect
        xy0         = self.xy0
        
        isLeft      = self.isLeft
        xy0Rect, xyLine = self._getFixedSupportCords(xy0, isLeft)
        ax.add_patch(Rectangle(xy0Rect, hFixedRect, wRect, ec='black', 
                               fc='white', hatch=hatch, lw = lw))
        ax.plot(xyLine[0], xyLine[1], c = 'white', lw = lw)

class DiagramElePointLoad(AbstractDiagramElement):
    
    def __init__(self, xy0, dxy0, options:PointLoadOptions):
        self.xy0 = xy0
        self.dxy0 = dxy0
        self.width = options.lw
        self.arrowWidth = options.arrowWidth
        self.c = options.c

    def plot(self, ax):
        """
        Note, Px and Py must be normalized!
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.arrow.html
        
        x and y are the start point of the arrow.
        
        """
        x , y = self.xy0
        Px, Py = self.dxy0
        c = self.c
                
        width  = self.width
        hwidth = self.arrowWidth 
        length = self.arrowWidth 
        ax.arrow(x, y, Px, Py, width=width, head_width = hwidth, 
                 head_length = length, edgecolor='none', 
                 length_includes_head=True, fc=c)

class DiagramEleMoment(AbstractDiagramElement):
    
    def __init__(self, xy0, diagramOptions:MomentPointLoadOptions,
                 isPositive=False):
        self.xy0 = xy0
        self.options = diagramOptions
        self.c = diagramOptions.c
        self.r = diagramOptions.r

        self.rotationAngle = diagramOptions.rotationAngle
        
        self.isPositive = isPositive

    def _getFixedSupportCords(self, positive):
        """
        Gets gets the coordinants for the triangle, rectangle, and white
        line in the pin connector.

        """

        r = self.r
        arrow = r / 4
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
            
        return  x, y, xarrow, yarrow


    def plot(self, ax):       

        lw = self.options.lw
        x, y, xarrow, yarrow = self._getFixedSupportCords(self.isPositive)
        rInner = self.r / 5

        # Define a rotation matrix
        theta = np.radians(self.rotationAngle)
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c, -s), (s, c)))
        
        # rotate the vectors
        xy = np.column_stack([x,y])
        xyArrow = np.column_stack([xarrow, yarrow])
        xyOut = np.dot(xy, R.T)
        xyArrowOut = np.dot(xyArrow, R.T)
        
        # Shift to the correct location
        
        x0 = self.xy0[0]
        xyOut[:,0] += x0
        xyArrowOut[:,0] += x0
        xy0 = [x0,0]
        
        c = self.options.c
        ax.add_patch(Circle(xy0, rInner, facecolor=c, fill=True, zorder=2, lw = lw))

        plt.plot(xyOut[:,0], xyOut[:,1])
        plt.plot(xyArrowOut[:,0], xyArrowOut[:,1], c=c)

class DiagramEleLabel:
    
    def __init__(self, xy0, label, labelOptions):
        self.xy0 = xy0
        self.label = label
        self.labelOffset = labelOptions.labelOffset
        self.textKwargs = labelOptions.textKwargs        
        
    def plot(self, ax):
        x = self.xy0[0] + self.labelOffset
        y = self.xy0[1] + self.labelOffset
        ax.text(x, y, self.label, self.textKwargs)

class DiagramEleLoadDistributed(AbstractDiagramElement):
    
    def __init__(self, loadBox, diagramOptions:DistLoadOptions, 
                                plOptions:PointLoadOptions):
        self.loadBox = loadBox
        # self.pointUp = loadBox.pointUp
        self.options = diagramOptions
        self.plOptions = plOptions

    def plot(self, ax):

        """
        The line load is compsed of the top bar, two side bars, and a series
        of arrows spaced between the side bars. Only vertical line loads
        are supported.

        """
        barWidth = self.options.barWidth
        spacing = self.options.spacing
        barC = self.options.c
        x1, x2 = self.loadBox.x
        y1, y2 = self.loadBox.y
        
        N = int((x2 - x1) / spacing) + 1
        xVals = np.linspace(x1, x2, N)
        
        ystart = self.loadBox.fout[0]
        yend = self.loadBox.datum
        dy = ystart - yend
        
        
        xbar = [x1, x2]
        yBarS = [ystart, ystart]
        yBarE = [yend, yend]
        plt.plot(xbar, yBarS, linewidth = barWidth, c = barC)
        plt.plot(xbar, yBarE, linewidth = barWidth, c = barC)
        
        for ii in range(N):
            x = xVals[ii]
            # pointLoad = DiagramElePointLoad((x, ystart), (0, yend), self.plOptions)
            pointLoad = DiagramElePointLoad((x, ystart), (0, -dy), self.plOptions)
            pointLoad.plot(ax)

class DiagramEleLoadLinear(AbstractDiagramElement):
    
    def __init__(self, loadBox, diagramOptions:LinLoadOptions, 
                                plOptions:PointLoadOptions):
        self.loadBox = loadBox
        self.options = diagramOptions
        self.plOptions = plOptions

    def plot(self, ax):

        """
        The line load is compsed of the top bar, two side bars, and a series
        of arrows spaced between the side bars. Only vertical line loads
        are supported.

        """
        barWidth = self.options.barWidth
        minLengthCutoff = self.options.minLengthCutoff
        spacing = self.options.spacing
        barC = self.options.c
        x1, x2 = self.loadBox.x
        # y1, y2 = self.loadBox.y
        
        # baseLineWidth = 0.015
        
        Nlines = int((x2 - x1) / spacing) + 1
        xVals = np.linspace(x1, x2, Nlines)
        
        q1, q2 = self.loadBox.fout
        yVals = np.linspace(q1, q2, Nlines)
        
        # The top/bottom lines .
        ydatum = self.loadBox.datum
        xbar  = [x1, x2]
        yBardatum = [ydatum, ydatum]                     
        yBarLinear = [q1, q2]

        plt.plot(xbar, yBardatum, linewidth = barWidth, c = barC)
        plt.plot(xbar, yBarLinear, linewidth = barWidth, c = barC)
        
        for ii in range(Nlines):
            xline = xVals[ii]
            yLine = yVals[ii]
            
            # plot just the line with no arrow                
            if abs(yLine - ydatum) > minLengthCutoff:
                xy0 = (xline, yLine)
                dxy0 = (0, ydatum - yLine)
                load = DiagramElePointLoad(xy0, dxy0, self.plOptions)
                load.plot(ax)
                
            # plot line and arrow.
            else:
                width = self.plOptions.lw
                ax.plot([xline, xline], [yLine, ydatum], c = barC,
                              linewidth=width)

class DiagramEleBeam:
    
    def __init__(self, xy0, xy1, diagramOptions:BeamOptions):
        """
        Draws a base beam diagram between two points.
        """
        
        self.xy0= xy0
        self.xy1= xy1
        self.options = diagramOptions

    def plot(self, ax):

        xy0 = self.xy0
        xy1 = self.xy1
        lw = self.options.lw
        c = self.options.c
        ax.plot([xy0[0], xy1[0]], [xy0[1], xy1[1]], lw = lw, c=c)

class BasicDiagramPlotter():
    supportTypeDict = {'free':DiagramEleFreeSupport,
                       'pinned':DiagramElePinSupport,
                       'roller':DiagramEleRollerSupport,
                       'fixed':DiagramEleFixedSupport}
    
    def __init__(self, scale = 1, supScale = 0.8, L=1):
        
        diagramOptions      = BasicOptionsDiagram(scale, supScale)
        self.supportParams  = diagramOptions.getSupportDiagramOptions()
        self.labelParams    = diagramOptions.getLabelOptions()
        self.plOptions      = diagramOptions.getPointLoadOptions()
        self.momentParams   = diagramOptions.getMomentPointLoadOptions()
        self.distParams     = diagramOptions.getDistLoadOptions()
        self.linParams      = diagramOptions.getLinLoadOptions()

        self.pldistOptions = diagramOptions.getPointLoadDistOptions()
        

        self.beamParams = diagramOptions.getBeamOptions()
    
    def setEleLoadLineSpacing(self, baseSpacing):
        self.distParams.spacing = self.distParams.spacing*baseSpacing
        self.linParams.spacing = self.linParams.spacing*baseSpacing
    
    def _checkSupType(self, supType):
        if supType not in self.supportTypeDict:
            options = list(self.supportTypeDict)
            raise Exception(f'Recived {supType}, expected one of {options}')
    
    def plotBeam(self, ax, xy0, xy1):

        beam = DiagramEleBeam(xy0, xy1, self.beamParams)
        beam.plot(ax)
                      
    def plotSupport(self, ax, xy, supType, kwargs):
        self._checkSupType(supType)
        supportClass = self.supportTypeDict[supType]
        support = supportClass(xy, self.supportParams, **kwargs)
        support.plot(ax)
                  
    def plotLabel(self, ax, xy, label):
        pl = DiagramEleLabel(xy, label, self.labelParams)
        pl.plot(ax)
                
    def plotPointForce(self, ax, xy, Pxy):
        pl = DiagramElePointLoad(xy, Pxy, self.plOptions)
        pl.plot(ax)
          
    def plotPointMoment(self, ax, xy, isPositive):
        pl = DiagramEleMoment(xy, self.momentParams, isPositive = isPositive)
        pl.plot(ax)

    def plotElementDistributedForce(self, ax, loadBox):
        pl = DiagramEleLoadDistributed(loadBox, self.distParams, self.pldistOptions)
        pl.plot(ax)

    def plotElementLinearForce(self, ax, loadBox):
        pl = DiagramEleLoadLinear(loadBox, self.linParams, self.pldistOptions)
        pl.plot(ax)                

    def _initPlot(self, figSize, xlims, ylims, dpi = 300):
        
        dy = ylims[-1] - ylims[0]
        fig, ax = plt.subplots(constrained_layout=True, figsize=(figSize, dy), dpi=300)
        ax.axis('equal')
        ax.axis('off')        
        ax.set_xlim(xlims)
        ax.set_ylim(ylims)
        return fig, ax
