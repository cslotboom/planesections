import numpy as np
from dataclasses import dataclass
from abc import ABC, abstractmethod


class Section():
    E:float = None
    G:float = None
    A:float = None
    Iz:float = None
    Iy:float = None
    J:float = None
    
    
@dataclass
class SectionBasic(Section):
    """
    A basic section that contains the global propreties of the beam section,
    without any geometry. It's assume the section is elastic.
    
        
    Parameters
    ----------
    E : float
        The elastic modulus to use for the section.
    G : float
        The shear modulus to use for the section.
    A : float
        The section's area.
    Iz : float
        The section's second moment of ineria about the local z axis. 
        (typically the strong axis)          
    Iy : float
        The section's second moment of ineria about the local z axis. 
        (typically the weak axis)              
    J : float
        The units to use for the section.              
    """
    
    E:float = 1
    G:float = 1
    A:float = 1
    Iz:float = 1
    Iy:float = 1
    J:float = 1
    Avx:float = 1
    Avy:float = 1


@dataclass
class SectionRectangle(Section):
    """
    Represents a elastic Rectangular section. Iz and A are calcualted using 
    the beam width and height.
    
    https://www.structx.com/Shape_Formulas_024.html
    
    
    Parameters
    ----------
    E : float
        The elastic modulus to use for the section.
    d : float
        The section's height.
    w : float
        The section's width.            
    G : float
        The shear modulus to use for the section.
    units : float
        The units to use for the section.        
        
    """
    
    E:float = 200*10**9
    d:float = 1
    w:float = 1
    G:float = None
    units:str='m'
    
    def __post_init__(self):
        if not self.G:
            self.G = self.E/16
        
        self.A = self.d*self.w
        self.Iz = self.d**3*self.w / 12
        self.Iy = self.w**3*self.d / 12
        self.Avx = self.A *(5/6)
        self.Avy = self.A *(5/6)
        
        a = min(self.d, self.w)
        b = max(self.d, self.w)
        self.J = a**3 * b * (1/3 - 0.21*a/b * (1 - (a**4 / (12*b**4))))


class Section2D(Section):

    def __post_init__(self):
        super().__post_init__()
        raise Exception('Section2D is depricated, and will be removed in a future release. Use Section instead.')
    
@dataclass
class SectionBasic2D(SectionBasic):
    """
    A basic section that contains the global propreties of the beam section,
    without any geometry. It's assume the section is elastic.
    """

    def __post_init__(self):
        super().__post_init__()
        raise Exception('SectionBasic2D is depricated, and will be removed in a future release. Use SectionBasic instead.')    
                
