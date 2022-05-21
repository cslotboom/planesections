# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 20:57:19 2022

@author: Christian

Problems - make sure that hatching is consistent at different beam scales.
Make sure that units support imperial

Hatching should be similar to beam size?

"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle

from abc import ABC, abstractmethod
 
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
# fixities  = {'free':0, 'roller': 1, 'pinned':2, 'fixed':3}
fixities  = {'free':[0,0,0], 'roller': [0,1,0], 'pinned':[1,1,0], 'fixed':[1,1,1]}




class NodeArchetype:
    """
    Represents a node/point of interst on the diagram.
    """
    @abstractmethod
    def getFixityType():
        """
        Gets the fixity type used.
        Currently supported - free, roller, pin, fixed.
        """
        pass
    
    @abstractmethod
    def getPosition():
        """
        Gets the x position of the node.
        Currently supported - roller, pin, fixed.
        """

        pass
    
    @abstractmethod
    def getLabel():
        """
        Returns the label that has been assigned to the node/
        ???:
            what values are supported??
        """
        pass    
    


class BeamArchetype:
    """
    Archetype class of data beams need in order to use make use of the beam
    diagram class
    
    ???:
        Should nodes be given a required internal naming convention?
    """
    nodes = []
    NodeArchetype = None
    forces = []
    distForces = []

    
    
    @abstractmethod
    def getNodes():
        """
        Returns all noed objects in the beam.
        """
        pass
    
    @abstractmethod
    def getForces():
        """
        Gets all applied point Loads.
        """        
        pass
    
    @abstractmethod
    def getDistForses():
        """
        Gets all applied distrubuted Loads.
        """ 
        pass    
    
    
    @abstractmethod
    def setNodeArchetype():
        """
        Sets the archetype method used to create new nodes.
        """ 
        pass
    
    @abstractmethod
    def addNode(self, xCoord, fixity, label=None):
        """
        Adds a new node to the model.
        """ 
        pass    

        
        
        


# ???
# call point force?

class ForceArchetype:
    """
    Represents a force applied to a single node
    """
    
    @abstractmethod
    def getConnectedNode():
        """
        """
        pass
    
    @abstractmethod
    def getMagnitudes():
        """
        Returns the magnitude of force at each of the connected nodes
        """
        pass   
    
     
    @abstractmethod
    def getLabelNodes():
        """
        Returns the nodes that are labeled
        """
        pass         

class DistrubtedForceArchetype:
    """
    Represents a force distributed across multiple nodes, i.e. uniform, etc
    """
    
    @abstractmethod
    def getConnectedNode():
        """
        
        """
        pass
    
    @abstractmethod
    def getMagnitudes():
        """
        Returns the magnitude of force at each of the connected nodes
        """
        pass   
    
     
    @abstractmethod
    def getLabelNodes():
        """
        Returns the nodes that are labeled
        """
        pass      
    
    


# =============================================================================
# Implementations.
# =============================================================================


class Node(NodeArchetype):
    """
    A concrete implementation for a class that represents a node/point of 
    interst on the diagram.
    """
    
    def __init__(self, xCoord, fixity, label):
        self.x = xCoord
        self.fixity = fixity
        self.label = label
    
    
    def getFixityType(self):
        """
        Gets the fixity type used.
        Currently supported - free, roller, pin, fixed.
        """
        return self.fixity
    
    def getPosition(self):
        """
        Gets the x position of the node.
        Currently supported - roller, pin, fixed.
        """

        return self.x
    
    def getLabel(self):
        """
        Returns the label that has been assigned to the node/
        ???:
            what values are supported??
        """
        return self.label  


class Beam(BeamArchetype):
    
    def __init__(self):
        """
        The concrete implementaiton of the beam class.

        """
        nodes = []
        NodeArchetype = None
        forces = []
        distForces = []
        
        self.setNodeArchetype()
    
    def getNodes(self):
        """
        Returns all noed objects in the beam.
        """
        return self.nodes
    
    def getForces(self):
        """
        Gets all applied point Loads.
        """        
        return self.forces
    
    def getDistForses(self):
        """
        Gets all applied distrubuted Loads.
        """ 
        print('NOT SUPPORTED YET')            
        
        
    def addNode(self, xCoord, fixity, label=None):
        NewNode = self.nodeArchetype(xCoord, fixity,label)
        self.nodes.append(NewNode)
    
    def setNodeArchetype(self, nodeArchetype:NodeArchetype = Node):
        """
        Used to set the type of node class used. The node should inherit from
        the nodeArhetype class.
        """
        self.nodeArchetype = nodeArchetype                
    
    
    










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
    
    def __init__(self, scale=1):
        
        
        
        self.lw = 1 * scale
        plt.rc("hatch", linewidth=self.lw)
        
        self.scale = scale
        self.r = 0.1*scale
        self.hTriSup = 0.3*scale
        self.wTriSup = 2*self.hTriSup
        
        self.hFixedRect = 0.2*scale
        self.marginFixedSup = 0.2*scale
        self.hatch = '/'* int((3/scale))
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
        xyTri = [xyTri1, xyTri2, xy0]
        
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
        # print(isLeft)
        self.ax.add_patch(Rectangle(xy0Rect, self.hFixedRect, self.wRect, ec='black', fc='white', hatch=self.hatch, lw = self.lw))
        self.ax.plot(xyLine[0], xyLine[1], c = 'white', lw = self.lw)

    def plotFree(self, xy0, **kwargs):
        pass

    def plotPointForce(self, x, P):
        pass

    def plotPointMoment(self, x, M):
        pass
        
    def plotLineLoad(self, x1, x2, q):
        pass



# =============================================================================
# 
# =============================================================================



class BeamPlotter:
    
    """
    The interface between the high level beam abstraction and plotting lower 
    level plotting.
    """
        
    def __init__(self, beam):
        L = beam.getLength()
        
        self.beam = beam
        self.plotter = BasicBeamDiagram(L / 10)
        self.nodes = beam.getNodes()
        figsize = beam.getLength()
        xlims = beam.getxLims()
        xlims = [xlims[0] - L/20, xlims[1] + L/20]
        ylims = [-L/10, L/10]
        
        self.plotter._initPlot(figsize, xlims, ylims)
        
    def plotBeam(self):
        xlims = self.beam.getxLims()
        xy0 = [xlims[0], 0]
        xy1 = [xlims[1], 0]
        
        d = self.beam.d
        # print(xy0, xy1, d)
        self.plotter.plotBeam(xy0, xy1)
               
    def plotSupports(self):
        
        for node in self.nodes:
            
            fixityType  = node.getFixityType()
            x = node.getPosition()
            """
            This makes some big assumptions about the shape of the system.
            """
            kwargs = {}
            if fixityType == 'fixed' and x == self.xmin:
                kwargs =  {'isLeft':True}
                    
            if fixityType == 'fixed' and x == self.xmin:
                kwargs  = {'isLeft':False}                
            
            xy = [x,0]
            # plot the appropriate option without an if statement!
            
            self.plotter.supportPlotOptions[fixityType](xy, **kwargs)

    def plot(self):
        self.plotBeam()
        self.plotSupports()
        

    def plotForce(self):
        pass
    
            

def plotBeam(beam, beamPlotter = BasicBeamDiagram):
    """
    Is called to actually plot the beam.

    Parameters
    ----------
    beam : TYPE
        DESCRIPTION.
    beamPlotter : TYPE, optional
        DESCRIPTION. The default is BasicBeamDiagram.

    Returns
    -------
    None.

    """
    pass


# =============================================================================
# 
# =============================================================================

# beamSize = 8
# xlims = [-beamSize/2, beamSize/2]
# ylims = [-1.6, 1.6]
# figSize = beamSize + 1
# xy0 = [-1.,0]
# scale = .8



# diagram = BasicBeamDiagram(scale)

# diagram._initPlot(figSize)
# # diagram.plotPin(fig, ax, xy0)
# diagram.plotFixed([-1.5,0])
# diagram.plotRoller([-.5,0])
# diagram.plotPinned([0.5,0])
# diagram.plotFixed([1.5,0], isLeft = False)



# x1 = 0
# x2 = 3

# newBeam = Beam()

# newBeam.addNode(x1, 'Roller', 'A')
# newBeam.addNode(x2, 'Pinned', 'B')

# newPlotter = BeamPlotter(newBeam)
# newPlotter.plotSupports()


