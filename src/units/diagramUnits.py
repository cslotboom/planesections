"""
Defines some unit environments for the diagrams
"""

from dataclasses import dataclass


@dataclass
class DiagramArgUnit:
    """ Stores the propreties a diagram could have. """
    unit:float
    scale:float
    Ndecimal:int
    
    def getSummary(self):
        return f'unit={self.unit}, scale={self.scale}, Number of Decimals={self.Ndecimal}'

mDiagramUnits_mkN = {'distance':    DiagramArgUnit('kN', 1., 1),
                     'force':       DiagramArgUnit('kN', 0.001, 0),
                     'moment':      DiagramArgUnit('kN-m', 0.001, 0),
                     'distForce':   DiagramArgUnit('kN/m', 0.001, 0)}                    

mDiagramUnits_mN = {'distance':     DiagramArgUnit('N', 1., 1),
                    'force':        DiagramArgUnit('N', 1, 0),
                    'moment':       DiagramArgUnit('N-m', 1, 0),
                    'distForce':    DiagramArgUnit('N/m', 1, 0)}

iDiagramUnits_ftkip = {'distance':  DiagramArgUnit('ft', 1., 1),
                       'force':     DiagramArgUnit('kip', 0.001, 0),
                       'moment':    DiagramArgUnit('kip-ft', 0.001, 0),
                       'distForce': DiagramArgUnit('kip/ft', 0.001, 0)}

iDiagramUnits_ftlb = {'distance':   DiagramArgUnit('ft', 1., 1),
                       'force':     DiagramArgUnit('lb', 1., 0),
                       'moment':    DiagramArgUnit('lb-ft', 1., 0),
                       'distForce': DiagramArgUnit('lb/ft', 1., 0)}


# test = DiagramArgUnit('kN', 1., 1)

# test.__dict__ = {"unit":'test', 'scale':1, 'Ndecimal':3}



# class DiagramUnitArgs:
#     """
#     Defines the units and scale used in the diagram and output postprocessing 
#     plots
#     distance_unit : str
#         The unit to use for distance labels.
#     distance_scale : float
#         The scale to use to use for distance units.
#     distance_Ndecimal : int
#         The amount of decimals to round the distance units too.
#     force_unit : str
#         The unit to use for point force labels.
#     force_scale : float
#         The scale to use to use for point force magnitudes.
#     force_Ndecimal : int
#         The amount of decimals to use in point force labels.
#     moment_unit : str
#         The unit to use for moment labels.
#     moment_scale : float
#         The scale to use to use for moment magnitudes.
#     moment_Ndecimal : int
#         The amount of decimals to use in moment labels.
#     distForce_unit : str
#         The unit to use for distributed force labels.
#     distForce_scale : float
#         The scale to use to use for distributed force magnitudes.
#     distForce_Ndecimal : int
#         The amount of decimals to use in distributed force labels.
       
#     """
   
#     distance_unit:str     = 'm'
#     distance_scale:float  = 1.
#     distance_Ndecimal:int = 2
#     force_unit:str        = 'kN' 
#     force_scale:float     = 0.001
#     force_Ndecimal:int    = 0
#     moment_Unit:str       = 'kNm'
#     moment_scale:float    = 0.001
#     moment_Ndecimal:int    = 0
#     distForce_unit:str    = 'kN/m' 
#     distForce_scale:float = 0.001
#     distForce_Ndecimal:int    = 0

