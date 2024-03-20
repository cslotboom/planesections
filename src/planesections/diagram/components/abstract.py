# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 20:57:19 2022

@author: Christian

Contains classes that could apply to any different diagram style.

"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Polygon, Circle
from abc import ABC, abstractmethod
from dataclasses import dataclass

# class DiagramOptions:
#     def __init__(self, scale = 1, supScale = 0.8):
#         """
#         A class that controls how diagrams will be laid out, and provides
#         options for changing the apperance used. 

#         Parameters
#         ----------
#         scale : TYPE, optional
#             DESCRIPTION. The default is 1.
#         supScale : TYPE, optional
#             DESCRIPTION. The default is 0.8.

#         Returns
#         -------
#         None.

#         """
        
#         self.lw = 1 * scale
#         self.scale = scale # Scales all drawing elements
#         self.supScale = supScale # Scales all drawing elements
        
#         # changes the offset from the point in x/y
#         self.labelOffset = 0.1*scale
        
#         # Pin geometry variables
#         self.r = 0.08*scale*supScale
#         self.hTriSup = 0.3*scale*supScale
#         self.wTriSup = 2*self.hTriSup
        
#         # Parameters for the rectangle below the pin support
#         self.marginFixedSup = 0.2*scale*supScale
#         self.hatch = '/'* int((3/(scale*supScale)))
#         self.wRect   = self.wTriSup + self.marginFixedSup
        
#         self.hRollerGap = self.hFixedRect / 4
#         self.y0 = 0

class AbstractDiagramElement(ABC):
    """
    Diagram classes will contain the logic required to create a unique diagram
    element, and will be able plot them.
    """
    
    @abstractmethod
    def plot(self):
        """
        The pin connection consists of four components:
            The triangle face
            The hatched rectangle
            a white line to cover the bottom of the hatched rectagle
            a circle

        """
        pass

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