from planesections.units.diagramUnits import (mDiagramUnits_mkN, mDiagramUnits_mN,
                                        iDiagramUnits_ftkip, iDiagramUnits_ftlb)

from copy import deepcopy
   
class DiagramUnitEnvironmentHandler:
    """
    Creates and manages the units in the diagrams. When a diagram goes to 
    plot units, they will either be read from the active environment, or by
    reading from a specific set of units. The active environment can be 
    modified using the 'modifyActiveEnvironment' method, and a new active
    environment can be set using the 'setActiveEnvironment' method.

    By default, the active environment is used for all plots.
    """
    envTypes =  ['metric', 'metric_kNm', 'metric_Nm', 
                 'imperial_ftkip', 'imperial_ftlb', 'file']
    envPresetDict =  {'metric': mDiagramUnits_mkN, 
                      'metric_kNm': mDiagramUnits_mkN,
                      'metric_Nm': mDiagramUnits_mN,
                      'imperial_ftkip': iDiagramUnits_ftkip,
                      'imperial_ftlb': iDiagramUnits_ftlb}
    activeEnv = None
           
    def __init__(self, envType = "metric", fileName = ''):

        self.setActiveEnvironment(envType, fileName)
    
    def _validateEnvInput(self, envType):
        """
        Checks if an environment type is valid.
        """
        if envType in self.envTypes:
            return True
        else:
            raise Exception(f'{envType} is not one of the supported types, use one of {self.envTypes}')
    
    def setActiveEnvironment(self, envType, fileName = ''):
        """
        Sets the unit environment for diagrams. This manages the apperance 
        of all units.

        Parameters
        ----------
        envType : str
            The diagram unit environment to use. Custom values can be input
            via json file.
            Can have a value of:  *'metric',  'metric_kNm',  'metric_Nm',  
            'imperial_ftkip',  'imperial_ftlb'*
        fileName : str
            If a custom file is used, then  environment to use. Custom values can be input
            via json file.    
        """
        self._validateEnvInput(envType)
        if envType =='file':
            self.activeEnv = self.readCustomEnv(fileName)
        else:
            self.activeEnv = deepcopy(self.envPresetDict[envType])

    # TODO: fix this
    def readCustomEnv(self, file):
        print('Custom Environments coming soon....')
        
    def modifyActiveEnvironment(self, parameters, modDicts):
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
        
        output = deepcopy(self.activeEnv)
        
        if isinstance(parameters, str):
            parameters = [parameters]
        if isinstance(modDicts, dict):
            modDicts = [modDicts]
        if isinstance(parameters, list) and isinstance(modDicts, list):
            if len(parameters) != len(modDicts):
                raise Exception('The input variable lengths do not match')
            for param, modDict in zip(parameters, modDicts):
                output[param].__dict__ = modDict
        self.activeEnv = output
    
    def getActiveEnvironment(self):
        """
        Returns an copy of the active environment.

        Returns
        -------
        Environment Dict
            A dictionary of the environment classes.

        """
        return deepcopy(self.activeEnv)

    def getEnvironment(self, envType:str):
        """
        Returns a copy of the input environment type.

        Parameters
        ----------
        envType : str
            The diagram unit environment to use. Custom values can be input
            via json file.
            Can have a value of:  *'metric',  'metric_kNm',  'metric_Nm',  
            'imperial_ftkip',  'imperial_ftlb',  'file'*

        """
        if self._validateEnvInput(envType):
            return deepcopy(self.envPresetDict[envType])
        
    def __str__(self):
        summary = 'The diagram units arguements are:\n'
        for key in self.activeEnv.keys():
            summary += key + ' - ' + self.activeEnv[key].getSummary() + '\n'
        return summary
    
    def print(self):
        print(self)
    