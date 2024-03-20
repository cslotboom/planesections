from abc import ABC, abstractmethod

class OutputRecorder(ABC):
    Nnodes:int
    nodeID0:float
    nodeIDEnd:int
    ndf:int
    node:list
    
    @abstractmethod
    def getEleInteralForce():
        pass
    