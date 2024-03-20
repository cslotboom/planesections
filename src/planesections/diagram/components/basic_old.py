# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 20:57:19 2022

@author: Christian

"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Polygon, Circle

from .abstract import AbstractDiagramElement

# =============================================================================
# 
# =============================================================================

__all__ = ['BasicDiagramOptions', 'DiagramPinSupport', 'DiagramRollerSupport',
           'DiagramFixedSupport', 'DiagramPointLoad', 'DiagramMoment']


class BasicDiagramOptions:
    def __init__(self, scale = 1, supScale = 0.8):
        
        self.lw = 1 * scale
        self.scale = scale # Scales all drawing elements
        self.supScale = supScale # Scales all drawing elements
        
        # Beam Propreties
        self.lw_beam = 2 * scale
        self.c_beam = 'black'
        
        # Point Load Propreties
        self.w_PointLoad = 0.03 * scale
        self.c_PointLoad = 'C0'
        # Distributed Load Propreties
        self.c_dist_bar = 'grey'
        self.spacing_dist = 1*scale
        
        # changes the offset from the point in x/y
        self.labelOffset = 0.1*scale
        
        # Pin geometry variables
        self.r = 0.08*scale*supScale
        self.hTriSup = 0.3*scale*supScale
        self.wTriSup = 2*self.hTriSup
        
        # Parameters for the rectangle below the pin support
        self.marginFixedSup = 0.2*scale*supScale
        self.hatch = '/'* int((3/(scale*supScale)))
        self.wRect   = self.wTriSup + self.marginFixedSup
        
        self.hRollerGap = self.hFixedRect / 4
        self.y0 = 0



class DiagramPinSupport(AbstractDiagramElement):
    
    def __init__(self, xy0, diagramOptions:BasicDiagramOptions):
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

    def plot(self, ax, xy0):
        """
        Plots a pin support at the location xy0. Pins are made up of the 
        fixed base rectangle, a triangle support, and the

        """        
        scale = self.options.scale
        xyTri, xy0Rect, xyLine = self._getPinSupportCords(xy0, scale)
        self._plotPinGeom(ax, xy0, xyTri, xy0Rect, xyLine)

class DiagramFreeSupport(DiagramPinSupport):
    
    def __init__(self, diagramOptions:BasicDiagramOptions, xy0):
        self.xy0 = xy0
        self.options = diagramOptions
        self.lineOffset = self.options.hFixedRect/10 

    def plot(self, ax, xy0):
        """
        Plots a pin support at the location xy0. Pins are made up of the 
        fixed base rectangle, a triangle support, and the

        """        
        
        pass    
             
class DiagramRollerSupport(DiagramPinSupport):
    
    def __init__(self, diagramOptions:BasicDiagramOptions, xy0):
        self.xy0 = xy0
        self.options = diagramOptions
        self.lineOffset = self.options.hFixedRect/10 


    def _getRollerSupportCords(self, xy0, scale):
        """
        Gets gets the coordinants for the triangle, rectangle, and white
        line in the pin connector.

        """
        
        lineOffset  = self.lineOffset
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

    def plotRoller(self, ax, xy0):
        """
        Rollers use the same basic support as a pin, but adds some lines to 
        
        Plots a pin support at the location xy0. Pins are made up of the 
        fixed base rectangle, a triangle support, and the

        """
        scale = self.options.scale
        xyTri, xy0Rect, xyLine = self._getPinSupportCords(xy0, scale)
        self._plotPinGeom(ax, xy0, xyTri, xy0Rect, xyLine)
        xy0gap, xyRollerLine = self._getRollerSupportCords(xy0, self.scale)
        self._plotRollerGeom(ax, xy0gap, xyRollerLine)       
       

    def plot(self, ax, xy0):
        """
        Plots a pin support at the location xy0. Pins are made up of the 
        fixed base rectangle, a triangle support, and the

        """        
        
        self.plotRoller(ax, xy0)        

class DiagramFixedSupport(AbstractDiagramElement):
    
    def __init__(self, xy0, diagramOptions:BasicDiagramOptions, isLeft):
        self.xy0 = xy0
        self.options = diagramOptions
        self.isLeft = isLeft

    def _getFixedSupportCords(self, xy0, isLeft=True):
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

    def plot(self, ax, xy0):
        """
        Plots a pin support at the location xy0. Pins are made up of the 
        fixed base rectangle, a triangle support, and the

        """
        
        lw          = self.lw
        hFixedRect  = self.options.hFixedRect
        hatch       = self.options.hatch
        wRect       = self.options.wRect
        
        isLeft      = self.isLeft
        xy0Rect, xyLine = self._getFixedSupportCords(xy0, isLeft)
        ax.add_patch(Rectangle(xy0Rect, hFixedRect, wRect, ec='black', fc='white', hatch=hatch, lw = lw))
        ax.plot(xyLine[0], xyLine[1], c = 'white', lw = lw)

class DiagramPointLoad(AbstractDiagramElement):
    
    def __init__(self, xy0, Pxy0, diagramOptions:BasicDiagramOptions):
        self.xy0 = xy0
        self.Pxy0 = Pxy0
        self.options = diagramOptions
        self.baseWidth = diagramOptions.w_PointLoad
        self.c = diagramOptions.c_PointLoad

    def _getFixedSupportCords(self, xy0, isLeft=True):
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

    def plot(self, ax, xy0):
        """
        Note, Px and Py must be normalized!
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.arrow.html
        
        x and y are the start point of the arrow.
        
        """
        x , y = self.xy0
        Px, Py = self.Pxy0
        c = self.c
                
        width = self.baseWidth
        hwidth = width* 5
        length = width* 5
        ax.arrow(x, y, Px, Py, width=width, head_width = hwidth, head_length = length, 
                      edgecolor='none', length_includes_head=True, fc=c)

class DiagramMoment(AbstractDiagramElement):
    
    def __init__(self, xy0, Pxy0, diagramOptions:BasicDiagramOptions, 
                 baseWidth = 0.03, c='C0'):
        self.xy0 = xy0
        self.Pxy0 = Pxy0
        self.options = diagramOptions
        self.baseWidth = baseWidth
        self.c = c
        
        self.r = 0.15
        self.rotationAngle = 30

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


    def plot(self, ax, x0, positive=False):       

        lw = self.lw
        x, y, xarrow, yarrow = self._getFixedSupportCords(positive)
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
        xyOut[:,0] += x0
        xyArrowOut[:,0] += x0
        xy0 = [x0,0]

        ax.add_patch(Circle(xy0, rInner, facecolor='C0', fill=True, zorder=2, lw = lw))

        plt.plot(xyOut[:,0], xyOut[:,1])
        plt.plot(xyArrowOut[:,0], xyArrowOut[:,1], c='C0')




class DiagramLoadDistributed(AbstractDiagramElement):
    
    def __init__(self, loadBox, diagramOptions:BasicDiagramOptions, 
                 pointUp = True):
        self.loadBox = loadBox
        self.pointUp = pointUp
        self.options = diagramOptions


    def _getFixedSupportCords(self, xy0, isLeft=True):
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

    def plot(self, ax, xy0):

        """
        The line load is compsed of the top bar, two side bars, and a series
        of arrows spaced between the side bars. Only vertical line loads
        are supported.

        """
        
        spacing = self.options.spacing_dist
        x1, x2 = self.loadBox.x
        y1, y2 = self.loadBox.y
        
        barWidth = 1
        N = int((x2 - x1) / spacing) + 1
        xVals = np.linspace(x1, x2, N)
        
        if self.pointUp:
            ystart = 
        ystart = self._get_ystart(q,y0)
                        
        xbar = [x1, x2]
        yBarS = [ystart, ystart]
        yBarE = [ystart+q, ystart+q]
        plt.plot(xbar, yBarS, linewidth = barWidth, c = barC)
        plt.plot(xbar, yBarE, linewidth = barWidth, c = barC)
        
        for ii in range(N):
            x = xVals[ii]
            self.plotPointForce(x, ystart, 0, q, baseWidth = 0.015, c = barC)



# DiagramLoadLinear

# plotVerticalLinearLoad


