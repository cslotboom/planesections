from planesections.units.diagramUnits import (mDiagramUnits_mkN, mDiagramUnits_mN,
                                        iDiagramUnits_ftkip, iDiagramUnits_ftlb)

from copy import deepcopy
   
class DiagramUnitEnvironmentHandler:
    """
    Creates and manages the unit environment
    """
    envTypes =  ['metric', 'metric_kNm', 'metric_Nm', 
                 'imperial_ftkip', 'imperial_ftlb', 'file']
    envPresetDict =  {'metric': mDiagramUnits_mkN, 
                    'metric_kNm': mDiagramUnits_mkN,
                    'metric_Nm': mDiagramUnits_mN,
                    'imperial_ftkip': iDiagramUnits_ftkip,
                    'imperial_ftlb': iDiagramUnits_ftlb,
                    }
    env = None
           
    def __init__(self, envType = "metric", fileName = ''):
        """
        Creates and manages the unit environment. THe environment must either
        be a value from envTypes, or a json file specified by 'file'.
        If it is a file, then a filename must be specified.
        """
        self.setEnvironment(envType, fileName)
    
    def _validateEnvInput(self, envType):
        """
        Checks if an environment type is valid.
        """
        if envType in self.envTypes:
            return True
        else:
            raise Exception(f'{envType} is not one of the supported types, use one of {self.envTypes}')
    
    # def _validateCustomEnv(self, envType):
    #     """
    #     Checks if a Custom Environment is valid
    #     """
    #     if envType in self.envTypes:
    #         self.env = self.envDict[envType]
    #     else:
    #         raise Exception(f'{envType} is not one of the supported types')    
    # envTypes =  ['Metric', 'metric_kNm', 'metric_Nm', 
    #              'Imperial_ftkip', 'Imperial_ftlb', 'file']
    
    def setEnvironment(self, envType, fileName = ''):
        """
        Sets the unit environment for diagrams. This manages the apperance 
        of all units.

        Parameters
        ----------
        envType : str
            The diagram unit environment to use. Custom values can be input
            via json file.
            Can have a value of:  *'metric',  'metric_kNm',  'metric_Nm',  
            'imperial_ftkip',  'imperial_ftlb',  'file'*
        fileName : str
            If a custom file is used, then  environment to use. Custom values can be input
            via json file.    
        """
        self._validateEnvInput(envType)
        
        if envType =='file':
            self.env = self.readCustomEnv(fileName)
        else:
            self.env = deepcopy(self.envPresetDict[envType])
    
   
    # TODO: fix this
    def readCustomEnv(self, file):
        pass
        
    def modifyEnvironment(self, parameters, modDicts):
        """
        Changes the current environment, modifying part of the units in the environment.

        Parameters
        ----------
        parameters : str, or list of str
            The parameter to change, or a list of parmeters to change.
            Must have a value in ['distance', 'force', 'moment', 'distForce']
        modDicts : dict, or list of dict
            The unit dictionary for the parameter in question. 
            For each unit, the value must have one of:
            {"unit": yourUnit, "scale": yourscale, "Ndecimal":yourDecimals}
        """        
        
        output = deepcopy(self.env)
        
        if isinstance(parameters, str):
            parameters = [parameters]
        if isinstance(modDicts, dict):
            modDicts = [modDicts]
            
        if isinstance(parameters, list) and isinstance(modDicts, list):
            if len(parameters) != len(modDicts):
                raise Exception('The input variable lengths do not match')
            for param, modDict in zip(parameters, modDicts):
                output[param].__dict__ = modDict

        self.env = output
        
        
    def __str__(self):
        summary = 'The diagram units arguements are:\n'
        for key in self.env.keys():
            summary += key + ' - ' + self.env[key].getSummary() + '\n'
        return summary
    
    def print(self):
        print(self)
    

diagramUnits = DiagramUnitEnvironmentHandler()



class DiagramUnitArgs:
    """
    Defines the units and scale used in the diagram and output postprocessing 
    plots
    distance_unit : str
        The unit to use for distance labels.
    distance_scale : float
        The scale to use to use for distance units.
    distance_Ndecimal : int
        The amount of decimals to round the distance units too.
    force_unit : str
        The unit to use for point force labels.
    force_scale : float
        The scale to use to use for point force magnitudes.
    force_Ndecimal : int
        The amount of decimals to use in point force labels.
    moment_unit : str
        The unit to use for moment labels.
    moment_scale : float
        The scale to use to use for moment magnitudes.
    moment_Ndecimal : int
        The amount of decimals to use in moment labels.
    distForce_unit : str
        The unit to use for distributed force labels.
    distForce_scale : float
        The scale to use to use for distributed force magnitudes.
    distForce_Ndecimal : int
        The amount of decimals to use in distributed force labels.
       
    """
   
    distance_unit:str     = 'm'
    distance_scale:float  = 1.
    distance_Ndecimal:int = 2
    force_unit:str        = 'kN' 
    force_scale:float     = 0.001
    force_Ndecimal:int    = 0
    moment_Unit:str       = 'kNm'
    moment_scale:float    = 0.001
    moment_Ndecimal:int    = 0
    distForce_unit:str    = 'kN/m' 
    distForce_scale:float = 0.001
    distForce_Ndecimal:int    = 0






