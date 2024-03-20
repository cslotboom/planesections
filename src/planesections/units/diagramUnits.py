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


