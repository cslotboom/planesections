import numpy as np
from dataclasses import dataclass
from abc import ABC, abstractmethod
from planesections.section import SectionBasic
from typing import Union
        
# =============================================================================
# 
# =============================================================================

class NodeArchetype(ABC):
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

class Fixity:
    def __init__(self, name:str, fixityValues:list[int]):
        """
        A object that represents fixities around a certain degree of freedom.
        """
        self.name = name
        self.fixityValues = fixityValues
    def __repr__(self):
        return f'<Fixity type {self.name} with {self.fixityValues}.>'


class FixityTypes2D:
    """
    Used to generate possible fixity types. Currently the supported types for
    2D fixities are free, roller, pinned, and fixed. The Fixity class can be
    used to dispatch each of these objects with it's relevant "get" methods.
    
    Note each fixity types will all be set equal to the same object as opposed
    to new objects being created.
    
    Takes input of:
        - 'free'
        - 'roller'
        - 'pinned'
        - 'fixed'
    
    """
    releaseNames = ['free', 'roller', 'pinned', 'fixed']
    releaseTypes = [[0,0,0], [0,1,0], [1,1,0], [1,1,1]]
    free   = Fixity(releaseNames[0],   releaseTypes[0])
    roller = Fixity(releaseNames[1],   releaseTypes[1])
    pinned = Fixity(releaseNames[2],   releaseTypes[2])
    fixed  = Fixity(releaseNames[3],   releaseTypes[3])
    types2D = {releaseNames[0]:free, releaseNames[1]:roller, 
               releaseNames[2]:pinned, releaseNames[3]:fixed}
    
    @classmethod
    def getFree(cls):
        """
        Returns a free support.
        """       
        return cls.free
    @classmethod
    def getRoller(cls):
        """
        Returns a roller support.
        """   
        return cls.roller
    @classmethod
    def getPinned(cls):
        """
        Returns a pinned support.
        """
        return cls.pinned
    @classmethod
    def getFixed(cls):
        """
        Returns a fixed support.
        """        
        return cls.fixed

NAMED_RELEASES_2D = set(FixityTypes2D.releaseNames)

def _getFixitystr(fixityInput):
    if fixityInput in FixityTypes2D.types2D.keys():
        return FixityTypes2D.types2D[fixityInput]
    else:
        raise Exception('fixity of type, {fixityInput} not supported, use one of', FixityTypes2D.keys())
        
def _getFixitylist(fixityInput):
    if list(fixityInput) == [0,0,0]:
        return FixityTypes2D.free
    elif list(fixityInput) == [0,1,0]:
        return FixityTypes2D.roller
    elif list(fixityInput) == [1,1,0]:
        return FixityTypes2D.pinned
    elif list(fixityInput) == [1,1,1]:
        return FixityTypes2D.fixed
    else:
        return Fixity('other', fixityInput)

def _convertFixityInput2D(fixityInput) -> Fixity:
    """
    Looks at fixity inputs and returns an appropriate fixity object.
    Supported options for fixity inputs include strings, i.e. 'pinned',
    
    """
    if isinstance(fixityInput, Fixity):
        return fixityInput
    
    if isinstance(fixityInput, list) or isinstance(fixityInput,np.ndarray):
        return _getFixitylist(fixityInput)
    
    if isinstance(fixityInput, str):
        return _getFixitystr(fixityInput)
    
    else:
        raise Exception('Given input not supported')

class Node(NodeArchetype):
    """
    Represents a node and isn't inteded to be used by users. Instead the
    2D and 3D node classes will be used.
    Nodes have labels and IDs. 
    The Label is a name the user assigns to the node and will be displayed
    in plots.
    
    The ID is a unique name that OpenSees will read. ID - 1 will be the 
    position in the beam node array. As new nodes are added, the IDs will be 
    sorted and updated so that they are always increasing from left to right.    
    """
    
    _dimension = '2D'   # the number for forces that can be applied
    _Nforce = 3         # the number for forces that can be applied    
    def __init__(self, x:float, fixity:Union[list, str, Fixity], label:str = ''):
        
        self.x = x
        self.fixity = _convertFixityInput2D(fixity)
        self.ID = None        
        self.label = label
        self.labelIsPlotted = False
        
        self.pointLoadIDs = []
        
        self.disp = None
        self.rFrc = None
        self.Fint = None
        
        self.averageShear = False
        
        self._setHasReaction()
            
    def _setHasReaction(self):
        self.hasReaction = False
        fixities = np.array(self.fixity.fixityValues)
        if np.any(fixities == np.array([1]*self._Nforce, int)):
            self.hasReaction = True        
    
    def _setID(self, newID):
        """
        Sets the node ID. The node ID is a unique identifier that can be used.
        Users can use this to set the ID, but the old ID will be replaced 
        every time the sort function is called.

        Parameters
        ----------
        newID : int
            A unique integer that represents the node.
            
        """
        self.ID  = newID
        
    def __repr__(self):
        return f'{self._dimension} Node object at {self.x}'

    def getLabel(self):
        return self.label
    
    def getPosition(self):
        return self.x
    
    def _checkIfResultsAveraged(self):
        if self.hasReaction == False and len(self.pointLoadIDs) == 0:
            return True
        return False
        
    
    def getInternalForces(self, ind):
        """
        Returns the left and right internal forces each node has for the input
        force type. For 2D:
            0: Px (axial force)
            1: Vx (shear force)
            2: M (bending
        For 3D:
            0: Px (axial force)
            1: Vx (shear force)
            2: Vy (bending
            3: Mx (Torsion)
            4: My (Out of Plane Bending)
            5: Mz (bending)            
        """

        return self.Fint[[ind,ind + self._Nforce]]
    
        
        
class Node2D(Node):
    """
    Represents a node 2D. Nodes have labels and IDs and fixities. 
    The Label is a name the user assigns to the node and will be displayed
    in plots.
    
    The ID is a unique name that OpenSees will read. ID - 1 will be the 
    position in the beam node array. As new nodes are added, the IDs will be 
    sorted and updated so that they are always increasing from left to right.

    Parameters
    ----------
    x : float
        The postion of the node.
    fixity : [list, str, Fixity]
        In 2D, the fixity can be input as either a fixtiy object, a string 
        from the variable NAMED_RELEASES_2D, or A list of the input fixities 
        for each possible degree of freedom. 
        
        Each node will have three degree of freedoms; [x, y, :math:`\\theta`]
        1 represents a fixed condition, 0 represents a free conditon. 
        
        The passed object can be a fixity object, a  string e.x. 'pinned', or 
        a list of integers, e.x. [1,1,0] gives a pin conneciton that's 
        fixed in x/y but free in rotation.
    label : str, optional
        A name for the node. This can be displayed in the plots. The default is ''.
    """    
    
    _dimension = '2D'   # the number for forces that can be applied
    _Nforce = 3         # the number for forces that can be applied
    
    def __init__(self, x:float, fixity:Union[list, str, Fixity], label:str = ''):
        super().__init__(x, fixity, label)

    def getFixityType(self):
        """
        Returns the type of beam fixity for supported 2D fixities.
        Currently only free, roller, pinned, and fixed are supported.

        """

        return self.fixity.name
  
    
class Node3D(Node):
    """
    Represents a node 3D. Nodes have labels and IDs and fixities. 
    The Label is a name the user assigns to the node and will be displayed
    in plots.
    
    The ID is a unique name that OpenSees will read. ID - 1 will be the 
    position in the beam node array. As new nodes are added, the IDs will be 
    sorted and updated so that they are always increasing from left to right.

    Parameters
    ----------
    x : float
        The postion of the node.
    fixity : fixity, list
        In 3D, the fixity can be input as either a fixtiy object, or a list of 
        the input fixities for each possible degree of freedom. 
        Each node will have six degree of freedoms; [x, y, :math:`\\theta`x]
        1 represents a fixed condition, 0 represents a free conditon. 
        e.x. [1,1,0,1,1,1]
        A pin conneciton that's fixed in x/y and fixed all in rotation DOF.
    label : str, optional
        A name for the node. This can be displayed in the plots. The default is ''.
        
    """    
    
    _dimension = '3D'   # the number for forces that can be applied
    _Nforce = 6         # the number for forces that can be applied
    
    def __init__(self, x:float, fixity:Union[list, str, Fixity], label:str = ''):
        super().__init__(x, fixity, label)

    def getFixityType(self):
        """
        Unsupported for 3D beams.

        """
        raise Exception('Plotting for 3D beams not yet supported')

# =============================================================================
# 
# =============================================================================

class Beam:
    """
    A representation of a beam object, that can be used to define information
    about basic beams. Units must form a consist unit basis for FEM analysis.
    
    The base Beam class isn't used by the user, the inherited classes Node2D and
    Node3D are used instead.
    
    """
    _dimension = ''
    _ndf = None
    _NodeTypes = {'2D':Node2D, '3D':Node3D}
    _activeNodeType = None
    
    def _initDimensionVariables(self, dimension):
        self._dimension = dimension
        if dimension == '2D':
           self._ndf = 3
        elif dimension == '3D':
           self._ndf = 6           
        self._activeNodeType = self._NodeTypes[self._dimension]

    def getDOF(self):
        """
        Returns the number of degrees of Freedom at each point in the beam.
        """
        return self._ndf

    def _initArrays(self):
        self.nodeLabels = {}
        self.nodes:list[Node] = []
        self.Nnodes = 0
        self.pointLoads = []
        self.distLoads = []
        self.nodeCoords = set()
        
    def getLength(self):
        """
        Returns the length of the beam.

        Returns
        -------
        float
            The beam length.

        """
        return self.nodes[-1].x - self.nodes[0].x
    
    def getxLims(self):
        """
        Returns the  of the beam.

        Returns
        -------
        list[float]
            A list with the left most and right most point.

        """        
        
        return self.nodes[0].x, self.nodes[-1].x
    
    def _sortNodes(self):
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
        
        # Sort the nodes.
        sortedInd   = np.argsort(xcoords)
        sortedNodes = np.array(self.nodes)[sortedInd]
        self.nodes  = list(sortedNodes)
        
        self._resetNodeID()
        self._remapLabels(sortedInd)
        self._remapPointLoads(oldInd, sortedInd)    
        
    def getNodeIDs(self):
        """
        Gets all of the node IDs.

        Returns
        -------
        IDs : list[int]
            a list of all of the node IDs in the model.

        """
        
        IDs = [None]*self.Nnodes
        for ii, node in enumerate(self.nodes):
            IDs[ii] = node.ID
        
        return IDs
           
    def _resetNodeID(self):
        """
        Resets all the node IDs based on their position. The ID starts counting
        at the left-most label.
        """
        for ii, node in enumerate(self.nodes):
            node._setID(int(ii + 1))

    def _remapPointLoads(self, oldIDs, sortedInd):
        """
        Remaps the point node pointer to the new node positionl. When the nodes
        are sorted the old pointer will not reference the correct positon.
        We don't know where the position is because of the newly added node,
        so we have to search each node and find the position.
        """        
        sortedIDs = np.array(oldIDs)[sortedInd]
        for pointLoad in self.pointLoads:
            newInd = np.where(sortedIDs == pointLoad.nodeID)[0][0] + 1
            pointLoad.nodeID = newInd
        
    def _remapLabels(self, sortedInd):
        """
        Remaps the label objects so that they point towards the correct node.
        """
        oldLabels = self.nodeLabels
        newLabel = {}
        
        for label in oldLabels:
            newLabel[label] = sortedInd[oldLabels[label]]
        self.nodeLabels = newLabel   
    
    def _addedNodeMessage(self, x):
        print(f'New node added at: {x}')
    
    
    def addNode(self, x:float, fixity:Union[list, str, Fixity] = None, 
                label:str = '', sort:bool = True):
        """
        Adds a new node to the beam. Keyword arguments are passed to the node.
        See :py:class:`Node2D` for more details

        Parameters
        ----------
        x : float
            The x coordinate of the node.
        fixity : Fixity, list
            A fixity object, or a list of the input fixities for each 
            possible degree of freedom. 
            2D nodes have three degree of freedoms; [x, y, :math:`\\theta`]
            3D nodes have six degree of freedoms; [x, y, z, :math:`\\theta_x`, :math:`\\theta_y`, :math:`\\theta_z`]
            For each degree of freedom, 1 represents a fixed condition, 0 represents a free conditon. 
            e.x. 
            
            [1,1,0] - A 2D connection that's fixed in x/y but free in rotation.
            
            [1,1,0,0,0,1] - A 3D connection that's fixed in x/y and :math:`\\theta_z` .
        label : str, optional
            A name for the node. This can be displayed in the plots. The default is ''.
        sort : bool, optional
            A toggle that turns on or off node sorting as new nodes are added.
            Nodes are sorted after each new node as added, this can be toggled 
            off to inprove performance. However, nodes must be sorted before 
            the analysis is run.
        
        Returns
        -------
        flag: int
            returns 0 if a existing node has been updated, 1 if a new node is
            added, and -1 if the process failed.

        """
        if fixity is None:
            fixity = Fixity('free',np.zeros(self._ndf, int))
        newNode = self._activeNodeType(x, fixity, label)
        if x in self.nodeCoords:
            """
            Note, the new node will not have any unique propreties 
            the old node had. That's why we have to reset the label.
            """
            index = self._findNode(x)
            nodeID = self.nodes[index].ID
            newNode._setID(nodeID)
            
            if label is not None:
                newNode.label = label
            
            self.nodes[index] = newNode
            return 0
        else:
            self._addNewNode(newNode, sort)
            return 1
        return -1

    def addLabel(self, x:float, label:str, sort:bool = True):
        """
        Adds a label to the beam at the coordinate in question. If a node 
        exists at this location the label is added to it. If no node exists at 
        location x, a new node is added. The new node will have default fixity.

        Parameters
        ----------
        x : float
            The x coordinate of the node.
        label : str, optional
            A name for the node. This can be displayed in the plots. The default is ''.            
        sort : bool, optional
            A switch which turns on or off sorting of the nodes after a lable is
            added. The default value is True, which sorts the nodes.
        
        Returns
        -------
        flag: int
            returns 0 if a existing node has been updated, 1 if a new node is
            added, and -1 if the process failed.

        """

        fixity = Fixity('free',np.zeros(self._ndf, int))
        newNode = self._activeNodeType(x, fixity, label) # either 2D or 3D depending on the dimension type.        
        if x in self.nodeCoords:
            index = self._findNode(x)
            self.nodes[index].label = label
            return 0
        else:
            self._addNewNode(newNode, sort)
            return 1
        return -1

    def _addNewNode(self, newNode:Node2D, sort:bool=True):
        self.Nnodes += 1
        newNode._setID(self.Nnodes)
        self.nodes.append(newNode)
        self.nodeCoords.add(newNode.x)
        if sort:
            self._sortNodes()

    def addNodes(self, xCoords:list[float], 
                 fixities:list[Union[list, str, Fixity]]|None = None, 
                 labels:list[str]|None = None ):
        """
        Adds several new nodes to the beam at the same time.
        The nodes in question are added at the x coordinates in the model.
        Nodes are sorted at the end of the process
        
        Parameters
        ----------
        xCoords : list of float
            A list of the x coordinates to be added to the model.
        fixities : list of fixity or booliean, optional
            A fixity object, or a list of the input fixities for each 
            possible degree of freedom. 
            2D nodes have three degree of freedoms; [x, y, :math:`\\theta`]
            3D nodes have six degree of freedoms; [x, y, z, :math:`\\theta_x`, :math:`\\theta_y`, :math:`\\theta_z`]
            For each degree of freedom, 1 represents a fixed condition, 0 represents a free conditon. 
            e.x. 
            
            [1,1,0] - A 2D connection that's fixed in x/y but free in rotation.
            
            [1,1,0,0,0,1] - A 3D connection that's fixed in x/y and :math:`\\theta_z` .

        label : list[str], optional
            A list of the labels for each node. 
            labels are displayed in the plots. The default is ''.

        """
               
        newNoads = len(xCoords)       
        if fixities == None:
            fixity = Fixity('free', np.zeros(self._ndf, int))
            fixities = [fixity]*newNoads
                        
        if labels is None:
            labels = [None]*newNoads
            
        sort = False #only sort at the end!
        for ii in range(newNoads):
            self.addNode(xCoords[ii], fixities[ii], labels[ii], sort)     

        self._sortNodes()
        
    def _checkfixityInput(self, fixity:Fixity):
        
        """
        Confirms that the appropriate input has been supplied to the fixity
        vector.
        """
        fixVals = fixity.fixityValues
        if set(fixVals).issubset({0,1}) != True:
            raise ValueError("Fixity must be a list of zeros and ones.")
            
        # I forget why I explicitly check for 2 here. 
        # I'd guess we're runing out if just one value is provided
        if (len(fixVals) == 2 or len(fixVals) > self._ndf):
            raise ValueError(f"Fixity must be a integer or vector of length {self._ndf}")

    def _convertFixityInput(self, fixity):
        """
        If an integer is supplied, convert the input to a list.
        """
        
        if isinstance(fixity,int):
            return [fixity]*self._ndf
        else:
            return fixity

    def setFixity(self, x:float, fixity:list[Union[list, Fixity]], 
                  label = None):
        """
        Sets the model fixity at locaiton x. If the node exists, update it. If the node doesn't
        exist, then a new node will be added

        Parameters
        ----------
        x : float
            The x coordinant of the noded to be modified/added.
        fixity : list, Fixity
            A fixity object, or a list of the input fixities for each 
            possible degree of freedom. 
            2D nodes have three degree of freedoms; [x, y, :math:`\\theta`]
            3D nodes have six degree of freedoms; [x, y, z, :math:`\\theta_x`, :math:`\\theta_y`, :math:`\\theta_z`]
            For each degree of freedom, 1 represents a fixed condition, 0 represents a free conditon. 
            e.x. 
            
            [1,1,0] - A 2D connection that's fixed in x/y but free in rotation.
            
            [1,1,0,0,0,1] - A 3D connection that's fixed in x/y and :math:`\\theta_z` .
        label : str, optional
            The label of the input node. 
            labels are displayed in the plots. The default is ''.
        """

        fixity = self._convertFixityInput(fixity)
        fixity = _convertFixityInput2D(fixity)
        self._checkfixityInput(fixity)
        
        if x in self.nodeCoords:
            index = self._findNode(x)
            self.nodes[index].fixity = fixity
            self.nodes[index].hasReaction = True 
            if label:
                self.nodes[index].label = label 
        else:
            self.addNode(x, fixity, label)        
                 
    def addPointLoad(self, x:float, pointLoad:list, label:str = '', 
                     labelNode=False):
        """
        Adds a load ot the model at location x.
        If a node exists at the current location, the old load value is overwritten.
        Old loads are deleted, and the node is relabled.
        Can represent objects in 2D or 3D.
        
        Parameters
        ----------
        x : float
            The location of the load.
        pointLoad : list
            A list of the forces. For a 2D beam has form [Fx, Fy, M].
            For a 3D beam has form [Fx, Fy, Fz, Mx, My, Mz].    
            
            New Load 1: 
                [0., 10., 0.]
                A vertical load of 10 is applied in beam units.
            New Load 2:
               [0., 0., 13]
               A moment of 13 is applied in beam units.
        label : str, optional
            The label of the input node. 
            labels are displayed in the plots. The default is ''.        
        labelNode : bool, optional
            A label that specifies if the node the force is assigned to 
            should also be labeled.
        """
        
        # Catch incorrectly given types.
        if hasattr(pointLoad, '__iter__') == False:
            raise Exception('Point load vector must be a list or Numpy array.')
        
        # Converty to np array. We do vector operations on data downstream
        if isinstance(pointLoad, list):
            pointLoad = np.array(pointLoad)
            
        loadID = len(self.pointLoads) + 1
        
        # Check if the node exists, add it if not.
        if x in self.nodeCoords:
            nodeIndex = self._findNode(x)
        else:
            self.addNode(x)
            nodeIndex = self._findNode(x)
            
        # index is what is used to look up, use one greater for the 
        self.nodes[nodeIndex].pointLoadIDs.append(loadID)
        if labelNode:
            self.nodes[nodeIndex].label = label
        
        nodeID = nodeIndex + 1    
        newLoad = PointLoad(pointLoad, x, nodeID, label)
        self.pointLoads.append(newLoad)                
         
    def addVerticalLoad(self, x:float, Py:float, label:str='', labelNode=False):
        """
        Adds a vertical load to the model at location x. If no node
        exists at position x, a new node is added.
        Old loads at this point are deleted.
        
        Parameters
        ----------
        x : float
            The x location to add force at.
        Py : float
            The magnitude of the vertical load to be added at x.
        label : str, optional
            The label of the input node. 
            labels are displayed in the plots. The default is ''.            
        labelNode : bool, optional
            A label that specifies if the node the force is assigned to 
            should also be labeled.
        """   
        if self._ndf == 3:
            pointLoad = np.array([0., Py, 0.])
        elif self._ndf == 6:
            pointLoad = np.array([0., Py, 0., 0., 0., 0.])
            
        self.addPointLoad(x, pointLoad, label, labelNode)
    # !!! TODO:
        # State which direction positive is.    
    def addMoment(self, x:float, M:float, label:str='', labelNode=False):
        """
        Adds a moment ot the model at location x. If no node
        exists at position x, a new node is added.
        Old loads at this point are deleted.

        
        Parameters
        ----------
        x : float
            The x location to add a moment at.
        M : float
            The magnitude of the moment to be added at x.
        label : str, optional
            The label of the input node. 
            labels are displayed in the plots. The default is ''.
        labelNode : bool, optional
            A label that specifies if the node the force is assigned to 
            should also be labeled.
        """        
        
        if self._ndf == 3:
            pointLoad = np.array([0.,0., M])
        elif self._ndf == 6:
            pointLoad = np.array([0., 0., 0., 0., 0., M])        
        
        self.addPointLoad(x, pointLoad, label, labelNode)     
        
    def addHorizontalLoad(self, x:float, Px:float, label:str='', labelNode=False):
        """
        Adds a horizontal point load at the model at location x. If no node
        exists at position x, a new node is added.
        Old loads are deleted.

        
        Parameters
        ----------
        x : float
            The x location to add force at.
        Px : float
            The magnitude of the vertical load to be added at x.        
        label : str, optional
            The label of the input node. 
            labels are displayed in the plots. The default is ''.
        labelNode : bool, optional
            A label that specifies if the node the force is assigned to 
            should also be labeled.
        """       
        
        if self._ndf == 3:
            pointLoad = np.array([Px, 0., 0.])
        elif self._ndf == 6:
            pointLoad = np.array([Px, 0., 0., 0., 0., 0.])              
        
        self.addPointLoad(x, pointLoad, label, labelNode)            
    
    #TODO: use a dictionary to speed this process up?!
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
            
    def addDistLoad(self, x1:float, x2:float, distLoad:float, label:str=''):
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
        distLoad : array
            The distributed load. 
            
            In 2D has the form [Fx (axial force), Fy (shear force)]
            
            In 3D has the form [Fx (axial force), Fy (shear force), Fz (shear force)]
        label : str
            A optional label for the force.
        """
        
        defaultFixity = np.zeros(self._ndf, int)
        distLoad = np.array(distLoad)
        
        if x1 not in self.nodeCoords:
            self.addNode(x1, defaultFixity)        
        if x2 not in self.nodeCoords:
            self.addNode(x2, defaultFixity)
        
        newEleLoad = EleLoadDist(x1, x2, distLoad, label)
        self.eleLoads.append(newEleLoad)

    def addDistLoadVertical(self, x1:float, x2:float, qy:float, label:str=''):
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
            A constantly distributed vertical force.
        label : str
            A optional label for the force.
        """

        if self._ndf == 3:
            distLoad = np.array([0., qy])
        if self._ndf == 6:
            distLoad = np.array([0., qy, 0.])
        self.addDistLoad(x1, x2, distLoad, label)

    def addDistLoadHorizontal(self, x1:float, x2:float, qx:float, label:str=''):
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
        label : str
            A optional label for the force.            
        """
        
        if self._ndf == 3:
            distLoad = np.array([qx, 0.])
        if self._ndf == 6:
            distLoad = np.array([qx, 0., 0.])
        self.addDistLoad(x1, x2, distLoad, label)    
    
    def addLinLoad(self, x1:float, x2:float, linLoad:list[list], label:str=''):
        """
        Adds a load that linearly varies between two input values. The load is 
        defined between two locations, x1 and x2. If nodes exist at these 
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
        linLoad : array
            The distributed load. The loads given are the maximum of the 
            distributed load
            
            In 2D has the form [[qx_start, qx_end], [qy_start, qy_end]],
            where x is an axial force and y is a shear force.
            
            In 3D has the form [[qx_start, qx_end], 
                                [qy_start, qy_end],
                                [qz_start, qz_end],]
            Where x is an axial force and y is shear force, and z is out of 
            plane shear force..
        label : str
            A optional label for the force.
            
        """
        
        defaultFixity = np.zeros(self._ndf, int)
        linLoad = np.array(linLoad)
        
        if x1 not in self.nodeCoords:
            self.addNode(x1, defaultFixity)        
        if x2 not in self.nodeCoords:
            self.addNode(x2, defaultFixity)
        
        newEleLoad = EleLoadLinear(x1, x2, linLoad, label)
        self.eleLoads.append(newEleLoad)

    def _checkForOutOfDateKwargs(self, kwargs):
        if 'isRightHigh' in kwargs:
            error = ("The kwarg 'isRightHigh' is depricated and will return" 
                + "an error in future versions. Instead pass a list of the two" 
                +   "values of the linearly distributed laod as a list.")
            raise Exception(error)

    def addLinLoadVertical(self, x1:float, x2:float, qy:list[float], label:str='',
                           **kwargs):
        """
        Adds a linear load to the model. The load is defined between two 
        locations in the model, x1 and x2. If nodes exist at these
        x1 or x2, then the load is definied between those existing nodes.
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
            The peak load for a linearly disributed vertical load.
        label : str
            A optional label for the force.        
        """

        self._checkForOutOfDateKwargs(kwargs)

        if self._ndf == 3:
            linLoad = np.array([[0.,0.], qy])
        if self._ndf == 6:
            linLoad = np.array([[0.,0.], qy, [0.,0.]])  
        self.addLinLoad(x1, x2, linLoad, label)

    def addLinLoadHorizontal(self, x1:float, x2:float, qx:list[float], label:str=''):
        """
        Adds a linear load to the model is defined between two locations, 
        x1 and x2, in the model. If nodes exist at these locations, then the 
        load is definied between those existing nodes.
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
            A list of y values to linearly distribute between.
        label : str
            A optional label for the force.
            
            
        """
        
        if self._ndf == 3:
            linLoad = np.array([qx, [0.,0.]])
        if self._ndf == 6:
            linLoad = np.array([qx, [0.,0.], [0.,0.]])        
            
        self.addLinLoad(x1, x2, linLoad, label)
        
        
    def Fmax(self, index):
        """
        get the maximum and minimum internal force for teh beam along the 
        appropriate axis. 0:x, 1:y, 2:z (In 3D, 3:rx, 4:ry, 5:rz)
        
        """
        Fmax = 0
        Fmin = 0
        for node in self.nodes:
            F1 = node.Fint[index]
            F2 = node.Fint[index + self._ndf]
            
            if F1 < Fmin or F2 < Fmin:
                Fmin = min(F1, F2)
            
            if Fmax < F1 or Fmax < F2:
                Fmax = max(F1, F2)
        return Fmin, Fmax

    def getNodes(self):
        return self.nodes



    def getMaterialPropreties(self):
        """
        Returns the material properties of a section.
        
        In 2D returns E, G, A, Iz
        
        In 3D returns E, G, A, Iy, Iz, J

        Returns
        -------
        list
            DESCRIPTION.

        """
        if self._dimension == '2D':
            return [self.section.E, self.section.G, 
                    self.section.A, self.section.Iz, 
                    self.section.Avx]    
        elif self._dimension == '3D': 
            # Area, E_mod, G_mod, Jxx, Iy, Iz,
            return [self.section.E, self.section.G, self.section.A,
                    self.section.Iz, self.section.Iy, self.section.J,
                    self.section.Avx, self.section.Avy]    


class Beam2D(Beam):
    def __post_init__(self):
        print('Beam2D is depricated and will return an error in future version. Use Beam instead.')

# =============================================================================
# 
# =============================================================================

def newEulerBeam(x2, x1 = 0, meshSize = 101, section=None, dimension = '2D'):
    """
    Initializes a new 2D Euler beam. The beam will have no fixities or labels.

    Parameters
    ----------
    x2 : float
        The end position of the beam. If no x1 is provided, this is also the
        length of the beam
    x1 : float, optional
        The start position of the beam. The default is 0.
    meshSize : int, optional
        The mesh size for the beam. This many nodes will be added between the 
        points x1 and x2. The default is 101, which divides the beam into
        100 even sections..
    section : Section2D, optional
        The section to use in the anaysis. The default uses SectionBasic2D().

    Returns
    -------
    EulerBeam2D : EulerBeam
        The beam intialized with the mesh of points between x1 and x2.
    """
    
    if x2 <= x1:
        raise Exception('x2 must be greater than x1')
    
    x = np.linspace(x1, x2, meshSize)  
    return EulerBeam(x, section=section, dimension = dimension)

def newEulerBeam2D(x2, x1 = 0, meshSize = 101, section=None):
    """
    Depricated, see newEulerBeam

    """
    
    print('newEulerBeam2D has been depricated and will return an error in the future. Use newEulerBeam instead.')
    
    return newEulerBeam(x2,x1,meshSize,section, '2D')


def newSimpleEulerBeam(x2, x1 = 0, meshSize = 101, q = 0, section=None, dimension = '2D'):
    """
    Initializes a new simply supported Euler beam with a distributed load. 
    The beam will have no fixities or labels.

    Parameters
    ----------
    x2 : float
        The end position of the beam. If no x1 is provided, this is also the
        length of the beam
    x1 : float, optional
        The start position of the beam. The default is 0.
    meshSize : int, optional
        The mesh size for the beam. This many nodes will be added between the 
        points x1 and x2. The default is 101, which divides the beam into
        100 even sections..
    q : float, optional
        The distributed load on the simply supported beam.
    section : Section2D, optional
        The section to use in the anaysis. The default uses SectionBasic2D().
        
    Returns
    -------
    EulerBeam2D : EulerBeam
        The beam intialized with the mesh of points between x1 and x2.
    """
    
    if x2 <= x1:
        raise Exception('x2 must be greater than x1')
    
    x = np.linspace(x1, x2, meshSize)  
    
    beam  = EulerBeam(x, dimension = '2D', section=section)
    beam.addNode(x1, [1,1,0])
    beam.addNode(x2, [0,1,0])
    if q != 0:
        beam.addDistLoadVertical(x1, x2, q)
    return beam


def newSimpleEulerBeam2D(x2, x1 = 0, meshSize = 101, q = 0, section=None):
    """
    Depricated, see newSimpleEulerBeam

    """
    print('newSimpleEulerBeam2D has been depricated and will return an error in the future. Use newSimpleEulerBeam instead.')

    return newSimpleEulerBeam(x2, x1, meshSize, q, section, dimension='2D')


class EulerBeam(Beam):
    """
    A creates a 2D/3D Euler beam. Information about the beam is stored in a mesh
    of nodes across the beam that are added by the user. Note that only output
    information at the nodes will be contained in the analysis. 
    
    The units of the beam must form a consistent unit base for FEM
    
    Inherits from the base :py:class:`Beam` class.
    
    
    Parameters
    ----------
    xcoords : list, optional
        The x coodinates of nodes along the beam the beam. The default is [],
        which starts with no nodes.
    fixity : list of Fixity, or list of lists
        A list of fixity objects, or A list of the input fixities for 
        each possible degree of freedom. 
        2D nodes have three degree of freedoms; [x, y, :math:`\\theta`]
        3D nodes have six degree of freedoms; [x, y, z, :math:`\\theta_x`, :math:`\\theta_y`, :math:`\\theta_z`]
        For each degree of freedom, 1 represents a fixed condition, 0 represents a free conditon. 
        e.x. 
        
        [1,1,0] - A 2D connection that's fixed in x/y but free in rotation.
        
        [1,1,0,0,0,1] - A 3D connection that's fixed in x/y and :math:`\\theta_z` .
    labels : list, optional
        A list of labels for each node. The default is [], which gives no label
        to each node.
    section : Section2D, optional
        The section to use in the anaysis. The default uses SectionBasic2D().
    """
    
    def __init__(self, xcoords:list = None, fixities:list = None, labels:list = None,
                 section = None, dimension = '2D'):
        # geomTransform has values 'Linear' or 'PDelta'
        self._initArrays()
        self._initDimensionVariables(dimension)
        self.nodes = []
        self.eleLoads = []
        
        if xcoords is None:
            xcoords = []
        if fixities is None:
            fixities = []
        if labels is None:
            labels = []
        if section is None:
            section = SectionBasic()
        
        NnewNodes = len(xcoords)
        fixities = self._initFixities(fixities, NnewNodes)
                
        if len(labels) == 0:
            labels = [None] * NnewNodes     
        
        if len(xcoords) != 0:
            self.addNodes(xcoords, fixities, labels)
        
        self.section = section
        self.d = 1
        self.plotter = None
      
    def _parseCoords(self, xcoords):
        if type(xcoords) == float:
            xcoords = [xcoords]
        if len(xcoords) == 1:
            xcoords = [0] + xcoords
               
    def _initFixities(self, fixities, NnewNodes):
        if len(fixities) == 0:
            name     = FixityTypes2D.releaseNames[0]
            fixities = [Fixity(name, np.zeros(self._ndf))] * NnewNodes
        if len(fixities) != NnewNodes:
            raise Exception('A fixity must be provided for each node.')
        return fixities

    def getMoment(self):
        """
        Depricated. See getBMD.

        Returns
        -------
        xcoords : array
            the x coordinants, has vale for x and y.
        Moment : array
            the output left and right moment at each node
        """
        print('getMoment has been depricated, and will return an error in, future releases. Use getBMD instead.')
        self.getBMD()

    
    def getBMD(self) -> list[list[float], list[float]]:
        """
        Returns the left and right bending moment at each node in the model. 
        Because the diagram is discrete, left and right forces must be used to 
        capture discontinuties.

        Returns
        -------
        xcoords : array
            the x coordinants, has vale for x and y.
        Moment : array
            the output left and right moment at each node
        """
        if self._dimension == '2D':
            M = self.getInternalForce(2)
        elif self._dimension == '3D':
            M = self.getInternalForce(5)
        return M



    def getSFD(self):
        """
        Returns the left and right shear force at each node in the model. 
        Because the diagram is discrete, left and right forces must be used to 
        capture discontinuties.

        Returns
        -------
        xcoords : array
            the x coordinants, has vale for x and y.
        Moment : array
            the output left and right moment at each node
        """
        return self.getInternalForce(1)

    def getInternalForce(self, index):
        """
        Returns the left and right internal forces each node in the model 
        for the input force type. Because the diagram is discrete, left and right
        forces must be used to capture discontinuties.

        Parameters
        ----------
        index : int
        The index of the force type to use
            0: axial force
            1: shear force
            2: bending

        Returns
        -------
        xcoords : array
            the x coordinants, has vale for x and y.
        force : array
            the output force at each node
        """

        xcoords = np.zeros(self.Nnodes*2)
        force = np.zeros(self.Nnodes*2) 
        for ii, node in enumerate(self.nodes):
            ind1 = 2*ii
            ind2 = ind1 + 2        
            xcoords[ind1:ind2]       = node.x
            force[ind1:ind2] = node.getInternalForces(index)    
        return xcoords, force

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
            if node.hasReaction:
                reactions.append(node.rFrc)
        return reactions
    
    @property
    def reactionDict(self):
        reactions = {}
        for node in self.nodes:
            if node.hasReaction:
                reactions[node.x] = node.rFrc
        return reactions




class TimoshenkoBeam(EulerBeam):
    """
    A creates a 2D/3D TimoshenkoBeam beam. Information about the beam is stored in a mesh
    of nodes across the beam that are added by the user. Note that only output
    information at the nodes will be contained in the analysis. 
    
    The units of the beam must form a consistent unit base for FEM
    
    Inherits from the base :py:class:`Beam` class.
    
    
    Parameters
    ----------
    xcoords : list, optional
        The x coodinates of nodes along the beam the beam. The default is [],
        which starts with no nodes.
    fixity : list of Fixity, or list of lists
        A list of fixity objects, or A list of the input fixities for 
        each possible degree of freedom. 
        2D nodes have three degree of freedoms; [x, y, :math:`\\theta`]
        3D nodes have six degree of freedoms; [x, y, z, :math:`\\theta_x`, :math:`\\theta_y`, :math:`\\theta_z`]
        For each degree of freedom, 1 represents a fixed condition, 0 represents a free conditon. 
        e.x. 
        
        [1,1,0] - A 2D connection that's fixed in x/y but free in rotation.
        
        [1,1,0,0,0,1] - A 3D connection that's fixed in x/y and :math:`\\theta_z` .
    labels : list, optional
        A list of labels for each node. The default is [], which gives no label
        to each node.
    section : Section2D, optional
        The section to use in the anaysis. The default uses SectionBasic2D().
    """




class EulerBeam2D(EulerBeam):
    def __post_init__(self):
        raise Exception('EulerBeam is depricated and will be removed in the next major update (1.3). Use EulerBeam instead.')




def newTimoshenkoBeam(x2, x1 = 0, meshSize = 101, 
                      section=None, dimension = '2D'):
    """
    Initializes a new TimoshenkoBeam beam. 
    The beam will have no fixities or labels.

    Parameters
    ----------
    x2 : float
        The end position of the beam. If no x1 is provided, this is also the
        length of the beam
    x1 : float, optional
        The start position of the beam. The default is 0.
    meshSize : int, optional
        The mesh size for the beam. This many nodes will be added between the 
        points x1 and x2. The default is 101, which divides the beam into
        100 even sections..
    section : Section2D, optional
        The section to use in the anaysis. The default uses SectionBasic2D().

    Returns
    -------
    timoshenkobeam : TimoshenkoBeam
        The beam intialized with the mesh of points between x1 and x2.
    """
    
    if x2 <= x1:
        raise Exception('x2 must be greater than x1')
    if dimension != '2D':
        raise Exception('The beam must be 2D.')
    
    x = np.linspace(x1, x2, meshSize)  
    return TimoshenkoBeam(x, section=section, dimension = dimension)


def newSimpleTimoshenkoBeam(x2, x1 = 0, meshSize = 101, q = 0, 
                            section=None, dimension = '2D'):
    """
    Initializes a new simply supported Timoshenko beam with a distributed load. 
    The beam will have no fixities or labels.

    Parameters
    ----------
    x2 : float
        The end position of the beam. If no x1 is provided, this is also the
        length of the beam
    x1 : float, optional
        The start position of the beam. The default is 0.
    meshSize : int, optional
        The mesh size for the beam. This many nodes will be added between the 
        points x1 and x2. The default is 101, which divides the beam into
        100 even sections..
    q : float, optional
        The distributed load on the simply supported beam.
    section : Section2D, optional
        The section to use in the anaysis. The default uses SectionBasic2D().
        
    Returns
    -------
    timoshenkobeam : TimoshenkoBeam
        The beam intialized with the mesh of points between x1 and x2.
    """
    
    if x2 <= x1:
        raise Exception('x2 must be greater than x1')
    if dimension != '2D':
        raise Exception('The beam must be 2D.')
    x = np.linspace(x1, x2, meshSize)  
    
    beam  = TimoshenkoBeam(x, dimension = '2D', section=section)
    beam.addNode(x1, [1,1,0])
    beam.addNode(x2, [0,1,0])
    if q != 0:
        beam.addDistLoadVertical(x1, x2, q)
    return beam





# =============================================================================
# 
# =============================================================================


@dataclass()
class EleLoad:
    """
    Depriciated, see EleLoadDist

    """    
    
    def __post_init__(self):
        raise Exception('EleLoad is depricated and will be removed in the next major update (1.3). Use EleLoadDist instead.')


@dataclass()
class EleLoadDist:
    """
    Representes a constantly distrubted element load between two points x1 x2. 
    For 2D elements, distributed loads can either px or py.

    Parameters
    ----------
    x1 : float
        The start position.
    x2 : float
        The end position.
    distLoad : list
        For 2D, a List of forces in [Px, Py].
    label : str, optional
        A label for the elment load. The default is ''.

    """    
        
    def __init__(self, x1:float, x2:float, distLoad:list, label:str = ''):

        self.x1 = x1
        self.x2 = x2
        self.P = distLoad
        self.label = label


@dataclass()
class EleLoadLinear:
    """
    Represents a linearly distrubted element load between two points x1 x2, 
    where the load increase from x1 to x2. The direction of the load can be 
    toggled so the high point is at x1 instead of x2.   

    Parameters
    ----------
    x1 : float
        The start position.
    x2 : float
        The end position.
    distLoad : list
        For 2D, a List of forces in [Px, Py].
    label : str, optional
        A label for the elment load. The default is ''.

        
    """    
        
    def __init__(self, x1:float, x2:float, linLoad:list, label:str = ''):

        self.x1 = x1
        self.x2 = x2
        self.P = linLoad
        self.label = label
        self.Lnet = x2 - x1
        
    def checkInRange(self, s):
        """
        Checks if a x value is in the range x1/x2 of the force.
        """
        
        if s < self.x1:
            raise Exception(r'First point range, must be greater than {x1}')
        
        if self.x2 < s:
            raise Exception(r'Second point range, must be less than {self.x2}')        

    def getLoadComponents(self, s1, s2, q):
        """
        Gets the load at two intermedia points, s1/s2.
        """
        self.checkInRange(s1)
        self.checkInRange(s2)
        s1 = (s1-self.x1)/self.Lnet         
        s2 = (s2-self.x1)/self.Lnet         
        
        m = q[1] - q[0]
        
        y1 = s1*m + q[0]
        y2 = s2*m + q[0]
        
        return y1, y2
    

@dataclass()
class PointLoad:
    """
    Representes a point load at locaiton x

    Parameters
    ----------
    P : list[float]
        List of forces. In 2D, as form [Px, Py, M].
    x : float
        The location of the point load.
    nodeID : int
        List of forces in [Px, Py].
    label : str, optional
        A label for the elment load. The default is ''.

    """        
    
    nodeID = None
    
    def __init__(self, P, x, nodeID = None, label = ''):
        self.P = P
        self.x = x
        self.nodeID = nodeID
        self.label = label
        self.loadPattern = None

    def _setID(self, newID):
        self.nodeID = newID
        
    def getPosition(self):
        return self.x
        
