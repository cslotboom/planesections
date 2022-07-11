# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 20:57:19 2022

@author: Christian

These are the abstract classes a user needs in order to "hook" into.

They define the promise we make - if people match these classes, they
can hook into the beam classes.
"""

from abc import ABC, abstractmethod

# =============================================================================
# Archetype classes
# =============================================================================


class LabelArchetype:
    
    pass

    """
    Methods to be determined closer to implementation.
    The methods used by the BeamPlotter will go here.
    """





class BeamArchetype(ABC):
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


class ForceArchetype(ABC):
    """
    Represents a force distributed across multiple nodes
    """
    FixityTypes = ['Fixed', 'Pinned', 'Roller']
    
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

class DistrubtedForceArchetype(ABC):
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
# 
# =============================================================================

class BeamDiagramArchetype(ABC):
    """
    The beam class will manage the beam diagram and holds it's current state.
    Currently this only really makes sense using Matplotlib.
    """
    
    @abstractmethod
    def plotPinned():
        """
        Makes a plot of the pin elements.
        """
        pass

    @abstractmethod
    def plotRoller():
       """
       Makes a plot of the roller elements.
       """
       pass
    
    @abstractmethod
    def plotFixed():
       """
       Makes a plot of the roller elements.
       """        
       pass
    



