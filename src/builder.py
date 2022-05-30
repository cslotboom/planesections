import openseespy.opensees as op
import numpy as np
import matplotlib.pyplot as plt

from planesections.archetypes import NodeArchetype
from dataclasses import dataclass
from abc import ABC, abstractproperty

# =============================================================================
# Future additons:
#  - plotting features
#  - Timoshenko beams
#  - Mass for dynamic analysis
#  - web interface
#  - beam summary?
# =============================================================================




# =============================================================================
# Problems:
# =============================================================================
# Summarize Nodes?
# Summarize Loads?


# @dataclass
class Section2D():
    E:None
    A:None
    Ixx:None
    


# Section()
class SectionBasic2D(Section2D):
    """
    A basic section that contains the global propreties of the beam section,
    without any geometry.
    """
    E:float = 1
    A:float = 1
    Ixx:float = 1


@dataclass
class SectionRectangle(Section2D):
    """
    Represents a Rectangular section.
    """
    
    E:float = 200*10**9
    d:float = 1
    w:float = 1
    units:str='m'
    
    def __post_init__(self):
        self.A = self.d*self.w
        self.Ixx = self.d**3*self.w / 12

        
class Node2D(NodeArchetype):
    def __init__(self, x, fixity, label = None):
        """
        Represents a node.
        Nodes have labels and IDs. 
        The Labe is a name the user assigns to the node and will be displayed
        in plots.
        
        The ID is a unique name that OpenSees will read. ID - 1 will be the 
        position in the beam node array

        Parameters
        ----------
        x : float
            The postion of the node.
        fixity : list
            A list of the input fixities for nodes.
        pointLoad : PointLoad
            DESCRIPTION.
        label : TYPE, optional
            DESCRIPTION. The default is None.

        """
        
        
        self.x = x
        self.fixity = fixity
        self.ID = None        
        self.label = label
        self.pointLoadIDs = []
        
        self.disp = None
        self.rFrc = None
        self.Fint = None

        self.hasReaction = False
        if np.any(fixity != [0,0,0]):
            self.hasReaction = True

    def setID(self, newID):
        self.ID  = newID
        
    def __repr__(self):
        return f'Node object at {self.x}'

    def getFixityType(self):
        """
        ???
        This isn't great, but we can't hash lists so I'm not sure how to 
        improve it.
        """
        if list(self.fixity) == [0,0,0]:
            return 'free'
        elif list(self.fixity) == [0,1,0]:
            return 'roller'    
        elif list(self.fixity) == [1,1,0]:
            return 'pinned'    
        elif list(self.fixity) == [1,1,1]:
            return 'fixed'
        else:
            return 'unsupported'

    def getLabel(self):
        return self.label
    
    def getPosition(self):
        return self.x
    
    

class Beam2D():
    """
    A representation of a beam object, that can be used to define information
    about basic beams.
    """

    def _initArrays(self):
        self.nodeLabels = {}
        self.nodes = []
        self.pointLoads = []
        self.distLoads = []
        self.nodeCoords = set()
        
    def getLength(self):
        return self.nodes[-1].x - self.nodes[0].x
    def getxLims(self):
        return self.nodes[0].x, self.nodes[-1].x
    
    def sortNodes(self):
        """
        Sorts and renames the nodes based on their x coordinate.
        This is expensive. Try to minimize calls to it.
        """               
        xcoords = np.zeros(self.Nnodes)
        labels  = [None] * self.Nnodes
        for ii, node in enumerate(self.nodes):
            xcoords[ii] = node.x
            labels[ii]  = node.label
        
        # subtract 1 because the indexes are one less.
        oldInd = np.array(self.getNodeIDs())
        # print(oldInd)
        
        # Sort the nodes.
        # print(xcoords)
        sortedInd   = np.argsort(xcoords)
        sortedNodes = np.array(self.nodes)[sortedInd]
        self.nodes  = list(sortedNodes)
        
        # print(sortedInd)
        self.resetNodeID()
        self.remapLabels(sortedInd)
        self.remapPointLoads(oldInd, sortedInd)    
        
    def getNodeIDs(self):
        
        IDs = [None]*self.Nnodes
        for ii, node in enumerate(self.nodes):
            IDs[ii] = node.ID
            # print(node.ID)
        
        return IDs
           
    def resetNodeID(self):
        """
        Resets all the node IDs based on their position. The ID starts counting
        at the left-most label
        """
        for ii, node in enumerate(self.nodes):
            node.setID(int(ii + 1))

    def remapPointLoads(self, oldIDs, sortedInd):
        """
        We don't know where the position is because of the newly added node,
        so we have to search each node and find the position.
        """        
        sortedIDs = np.array(oldIDs)[sortedInd]
        for pointLoad in self.pointLoads:
            newInd = np.where(sortedIDs == pointLoad.nodeID)[0][0] + 1
            pointLoad.nodeID = newInd
        
    def remapLabels(self, sortedInd):
        oldLabels = self.nodeLabels
        newLabel = {}
        for label in oldLabels:
            newLabel[label] = sortedInd[oldLabels[label]]
        self.nodeLabels = newLabel   
    
    def _addedNodeMessage(self, x):
        print(f'New node added at: {x}')
    
    def addNode(self, x, fixity = np.array([0.,0.,0.], int), label = None, sort = True):
        """
        Adds a new node to the model builder.

        Parameters
        ----------
        x : float
            The x coordinate of the node.
        fixity : np.array
            The fixity array. Contains 3 values, one for each dof in order
            x, y, rotation. 1 means the system is fixed in the DOF of question, 
            0 means the node is free in the DOF.
        label : int, optional
            The unique label of the node in question. 

        Returns
        -------
        flag: int
            returns 0 if a existing node has been updated, 1 if a new node is
            added, and -1 if the process failed.

        """
        newNode = Node2D(x, fixity, label)
        if x in self.nodeCoords:
            """
            ???
            Potential problem, the new node will not have any unique propreties 
            the old node had. That's why we have to reset the label.
            """
            index = self._findNode(x)
            nodeID = self.nodes[index].ID
            newNode.setID(nodeID)
            self.nodes[index] = newNode
            return 0
        else:
            # print(newNode)
            self._addNewNode(newNode, sort)
            return 1
        return -1


    def _addNewNode(self, newNode:Node2D, sort=True):
        self.Nnodes += 1
        newNode.setID(self.Nnodes)
        self.nodes.append(newNode)
        self.nodeCoords.add(newNode.x)
        if sort:
            self.sortNodes()
        

    def addNodes(self, xCoords, fixities = None, labels = None ):
        """
        Adds several new nodes to the beam at the same time.
        The nodes in question are added at the x coordinates in the model.
        Nodes are sorted at the end of the process
        
        Parameters
        ----------
        xCoords : list of float
            A list of the x coordinates to be added to the model.
        fixities : list of lists, optional
            Adds fixity to each of the new nodes. Fixity is given in a list 
            of boolean, where true means that the node if fixed in that DOF.
            The default is None, which results in all nodes being free.
            Ex.
            [[1,1,0], [0,0,0]]
            New node 1: fixed in x, fixed in y, free in rotation.
            New node 2: free in all DOF.


        """
               
        newNoads = len(xCoords)       
        if fixities == None:
            fixities = [np.array([0.,0.,0.])]*newNoads
                        
        if labels is None:
            labels = [None]*newNoads
            
        sort = False #only sort at the end!
        for ii in range(newNoads):
            self.addNode(xCoords[ii], fixities[ii], labels[ii], sort)     

        self.sortNodes()
        
    def _checkfixityInput(self, fixity):
        
        """
        Confirm that the appropriate input has been supplied to the fixity
        vector
        """
                
        if set(fixity).issubset({0,1}) != True:
            raise ValueError("Fixity must be a list of zeros and ones.")
        if len(fixity) == 2 or len(fixity) > 3:
            raise ValueError("Fixity must be a integer or vector of length 3")
       
    def _convertFixityInput(self, fixity):
        """
        If an integer is supplied, convert the input to a list.
        """
        
        if isinstance(fixity,int):
            return [fixity]*3
        else:
            return fixity

    def setFixity(self, x, fixity):
        """
        Sets the node fixity. If the node exists, update it. If the node doesn't
        exist, then a new node will be added

        Parameters
        ----------
        x : TYPE
            The x coordinant of the noded to be modified/added.
        fixity : int/list/array
            Either the integer 0/1, or a list of zeros/ones. If equal to 0, 
            that DOF is considered Free. Otherwise it is considered fixed.

        """

        fixity = self._convertFixityInput(fixity)
        self._checkfixityInput(fixity)
        
        if x in self.nodeCoords:
            index = self._findNode(x)
            self.nodes[index].fixity = fixity
            self.nodes[index].hasReaction = True 
        else:
            self.addNode(x, fixity)        
                 
    def addPointLoad(self, x, pointLoad):
        """
        Adds a load ot the model at location x.
        If a node exists at the current location, the old load value is overwritten.
        Old loads are deleted, and the node is relabled
        
        Parameters
        ----------
        x : float
            The location of the load.
        pointLoad : list
            A list of the forces in [Fx, Fy, M].
           [0., 10., 0.]
           New node 1: A vertical load of 10 is applied in beam units.
           [0., 0., 13]
           New node 2: A moment of 13 is applied in beam units.
        """
        
        loadID = len(self.pointLoads) + 1
        
        # Add the load ID to the node in question. Make a node if no ID.
        if x in self.nodeCoords:
            nodeIndex = self._findNode(x)
        else:
            self.addNode(x)
            nodeIndex = self._findNode(x)
        nodeID = nodeIndex + 1
            
        self.nodes[nodeIndex].pointLoadIDs.append(loadID) 
        newLoad = PointLoad(pointLoad, x, nodeID)
        self.pointLoads.append(newLoad)                
         
    def addVerticalLoad(self, x, Py):
        """
        Adds a vertical load to the model at location x.
        Old loads at this point are deleted.
        
        Parameters
        ----------
        x : float
            The x location to add a moment at.
        Py : float
            The magnitude of the vertical load to be added at x.
        """   

        pointLoad = np.array([0., Py, 0.])
        self.addPointLoad(x, pointLoad)
        
    def addMoment(self, x, M):
        """
        Adds a moment ot the model at location x.
        Old loads at this point are deleted.
        
        Parameters
        ----------
        x : float
            The x location to add a moment at.
        M : float
            The magnitude of the moment to be added at x.
        """        
        pointLoad = np.array([0.,0., M])
        self.addPointLoad(x, pointLoad)     
        
    def addHorizontalLoad(self, x, Px):
        """
        Adds a horizontal point load at the model at location x.
        Old loads are deleted.
        """       
        
        pointLoads = np.array([Px, 0., 0.])
        self.addPointLoad(x, pointLoads)            
             
    def _findNode(self, xInput:float):
        """
        Searches through all nodes, and returns the index of the node that has
        the input x-coordinant, if it exists.

        Parameters
        ----------
        xInput : float
            The x coordinant of the node being searched for.

        Returns
        -------
        ii : int
            The index of the node at the target location.

        """
        
        
        for ii, node in enumerate(self.nodes):
            if xInput == node.x:
                return ii
        return None
            
    def addDistLoad(self, x1, x2, distLoad):
        """
        Adds a distributed load to the model. The load is defined
        between two locations, x1 and x2, in the model. If nodes exist at these
        locations, then the load is definied between those existing nodes.
        If there are no nodes at these locations, then nodes are added to the 
        model.
        Old loads at this point are deleted.
        
        Parameters
        ----------
        x1 : float
            Start point of distributed load.
        x2 : float
            Start point of distributed load.
        distLoad : 2D array
            The distributed load in the form of 
            [Axial force, shear force]

        """
        
        genericFixity = np.array([0,0,0], int)
        genericPointLoad = np.array([0.,0.,0.], float)
        
        if x1 not in self.nodeCoords:
            self.addNode(x1, genericFixity, genericPointLoad)        
        if x2 not in self.nodeCoords:
            self.addNode(x2, genericFixity, genericPointLoad)
        
        newEleLoad = EleLoad(x1, x2, distLoad)
        self.eleLoads.append(newEleLoad)

    def addDistLoadVertical(self, x1, x2, qy):
        """
        Adds a distributed load to the model. The load is defined
        between two locations, x1 and x2, in the model. If nodes exist at these
        locations, then the load is definied between those existing nodes.
        If there are no nodes at these locations, then nodes are added to the 
        model.
        Old loads at this point are deleted.
        
        Parameters
        ----------
        x1 : float
            Start point of distributed load.
        x2 : float
            Start point of distributed load.
        qy : float
            A constantly distributed axial force.

        """

        distLoad = np.array([0., qy])
        self.addDistLoad(x1, x2, distLoad)

    def addDistLoadHorizontal(self, x1, x2, qx):
        """
        Adds a distributed load to the model. The load is defined
        between two locations, x1 and x2, in the model. If nodes exist at these
        locations, then the load is definied between those existing nodes.
        If there are no nodes at these locations, then nodes are added to the 
        model.
        Old loads at this point are deleted.
        
        Parameters
        ----------
        x1 : float
            Start point of distributed load.
        x2 : float
            Start point of distributed load.
        qx : float
            A constantly distributed axial force.
        """
        distLoad = np.array([qx, 0.])
        
        self.addDistLoad(x1, x2, distLoad)

    
    def plot(self):
        xcoords = np.array(list(self.nodeCoords))
        y = np.zeros_like(xcoords)
        plt.plot(xcoords, y)
        plt.plot(xcoords, y, '.')

    """OuputPropreties"""
    def Fmax(self, index):
        Fmax = 0
        Fmin = 0
        for node in self.nodes:
            F1 = node.Fint[index]
            F2 = node.Fint[index + 3]
            
            if F1 < Fmin or F2 < Fmin:
                Fmin = min(F1, F2)
            
            if Fmax < F1 or Fmax < F2:
                Fmax = max(F1, F2)
        return Fmin, Fmax


    def getNodes(self):
        return self.nodes
    
    def getForces():
        pass
    
    def getDistForses():
        pass 

# =============================================================================
# 
# =============================================================================



class EulerBeam2D(Beam2D):

    def __init__(self, xcoords = [], fixities = [], labels = [], 
                 section = SectionBasic2D(), geomTransform = 'Linear'):
        
        # print(self.nodeLabels)
        #
        self._initArrays()
        # geomTransform has values 'Linear' or 'PDelta'
        self.nodes = []
        self.eleLoads = []
                   
        self.Nnodes = 0
        NnewNodes = len(xcoords)
       
        if len(fixities) == 0:
            fixities = [np.array([0., 0., 0.])] * NnewNodes
            
        if len(labels) == 0:
            labels = [None] * NnewNodes            
        if len(xcoords) != 0:
            self.addNodes(xcoords, fixities, labels)
        
        self.section = section
        self.d = section.d
        self.materialPropreties = [section.A, section.E, section.Ixx]        
        self.plotter = None
        
        self.geomTransform = geomTransform
        self.EleType = 'elasticBeamColumn'
    
    @property
    def Mmax(self):
        return self.Fmax(2)

    @property
    def Vmax(self):
        return self.Fmax(1)

    @property
    def reactions(self):
        reactions = []
        for node in self.nodes:
            # print(node.hasReaction)
            if node.hasReaction:
                reactions.append(node.rFrc)
                
            # F1 = node.Reactions[index]
            # F2 = node.Fint[index + 3]
            
            # if F1 < Fmin or F2 < Fmin:
            #     Fmin = min(F1, F2)
            
            # if Fmax < F1 or Fmax < F2:
            #     Fmax = max(F1, F2)
        return reactions



# class Element():
       
#     def __init__(self, endNodes, eleLoad, ID):
#         self.endNodes = endNodes
#         self.eleLoad = eleLoad
#         self.ID = ID



class EleLoad:
    def __init__(self, x1, x2, distLoad):
        self.x1 = x1
        self.x2 = x2
        self.load = distLoad




class PointLoad:
    P = np.array([0.,0.,0.])
    nodeID = None
    
    def __init__(self, P, x, nodeID = None):
        self.P = P
        self.x = x
        self.nodeID = nodeID
        
    def setID(self, newID):
        # print(newID)
        self.nodeID = newID
        
        

class DistLoad():
    
    def __init__(self, ):
    
        pass
       
    
class PlotBeam():

    def __init__(self):
        pass
    
    def initBeamPlot(self):
        fig, ax = plt.subplots()
    
    


