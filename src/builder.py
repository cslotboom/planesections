import numpy as np
from dataclasses import dataclass
from abc import ABC, abstractproperty, abstractmethod

# =============================================================================
# Future additons:
#  - plotting features
#  - Timoshenko beams
#  - Mass for dynamic analysis
#  - web interface
#  - beam summary?
# =============================================================================



class Section2D():
    E:None
    A:None
    Ixx:None
    Iyy:None
    


@dataclass
class SectionBasic2D(Section2D):
    """
    A basic section that contains the global propreties of the beam section,
    without any geometry. It's assume the section is elastic.
    """
    E:float = 1
    A:float = 1
    Ixx:float = 1
    Iyy:float = 1


@dataclass
class SectionRectangle(Section2D):
    """
    Represents a elastic Rectangular section. Ixx and A are calcualted using 
    the beam width and height.
    """
    
    E:float = 200*10**9
    d:float = 1
    w:float = 1
    units:str='m'
    
    def __post_init__(self):
        self.A = self.d*self.w
        self.Ixx = self.d**3*self.w / 12
        self.Ixx = self.w**3*self.d / 12




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

        
class Node2D(NodeArchetype):
    """
    Represents a node.
    Nodes have labels and IDs. 
    The Labe is a name the user assigns to the node and will be displayed
    in plots.
    
    The ID is a unique name that OpenSees will read. ID - 1 will be the 
    position in the beam node array. As new nodes are added, the IDs will be 
    sorted and updated so that they are always increasing from left to right.

    Parameters
    ----------
    x : float
        The postion of the node.
    fixity : list
        A list of the input fixities for each possible degree of freedom. 
        Each node will have three degree of freedoms; [x, y, :math:`\\theta`]
        1 represents a fixed condition, 0 represents a free conditon. 
        e.x. [1,1,0]
        A pin conneciton that's fixed in x/y but free in rotation.
    label : str, optional
        A name for the node. This can be displayed in the plots. The default is ''.
    """    
    
    _dimension = '2D'
    
    def __init__(self, x, fixity, label = ''):
        
        self.x = x
        self.fixity = fixity
        self.ID = None        
        self.label = label
        self.labelIsPlotted = False
        
        self.pointLoadIDs = []
        
        self.disp = None
        self.rFrc = None
        self.Fint = None

        self.hasReaction = False
        if np.any(fixity != [0,0,0]):
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
        return f'Node object at {self.x}'

    def getFixityType(self):
        """
        Returns the type of beam fixity for supported 2D fixities.
        Currently only free, roller, pinned, and fixed are supported.

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
    
    def getInternalForces(self, ind):
        """
        Returns the left and right internal forces each node has for the input
        force type:
            0: axial force
            1: shear force
            2: bending
        """
        
        return self.Fint[[ind,ind+3]]



# =============================================================================
# 
# =============================================================================

class Beam2D():
    """
    A representation of a beam object, that can be used to define information
    about basic beams. Units must form a consist unit basis for FEM analysis.
    """

    def _initArrays(self):
        self.nodeLabels = {}
        self.nodes = []
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
    
    def addNode(self, x, fixity = np.array([0.,0.,0.], int), label = '', sort = True):
        """
        Adds a new node to the beam. Keyword arguments are passed to the node.
        See :py:class:`Node2D` for more details

        Parameters
        ----------
        x : float
            The x coordinate of the node.
        fixity : list
            A list of the input fixities for each possible degree of freedom. 
            Each node will have three degree of freedoms; [x, y, :math:`\\theta`]
            1 represents a fixed condition, 0 represents a free conditon. 
            e.x. [1,1,0]
            A pin conneciton that's fixed in x/y but free in rotation.
        label : str, optional
            A name for the node. This can be displayed in the plots. The default is ''.

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
            newNode._setID(nodeID)
            
            if label is not None:
                newNode.label = label
            
            self.nodes[index] = newNode
            return 0
        else:
            # print(newNode)
            self._addNewNode(newNode, sort)
            return 1
        return -1


    def addLabel(self, x, label, sort = True):
        """
        Adds a label to the beam at the coordinate in question. If a node exists
        at this location the label is added to it. 
        If no node exists at location x, a new node is added.
        The new node will have default fixity.

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

        fixity = np.array([0.,0.,0.], int)
        newNode = Node2D(x, fixity, label)
        if x in self.nodeCoords:
            index = self._findNode(x)
            self.nodes[index].label = label
            return 0
        else:
            self._addNewNode(newNode, sort)
            return 1
        return -1



    def _addNewNode(self, newNode:Node2D, sort=True):
        self.Nnodes += 1
        newNode._setID(self.Nnodes)
        self.nodes.append(newNode)
        self.nodeCoords.add(newNode.x)
        if sort:
            self._sortNodes()
        

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

        label : list[str], optional
            A list of the labels for each node. 
            labels are displayed in the plots. The default is ''.

        """
               
        newNoads = len(xCoords)       
        if fixities == None:
            fixities = [np.array([0.,0.,0.])]*newNoads
                        
        if labels is None:
            labels = [None]*newNoads
            
        sort = False #only sort at the end!
        for ii in range(newNoads):
            self.addNode(xCoords[ii], fixities[ii], labels[ii], sort)     

        self._sortNodes()
        
    def _checkfixityInput(self, fixity):
        
        """
        Confirms that the appropriate input has been supplied to the fixity
        vector.
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

    def setFixity(self, x, fixity, label = None):
        """
        Sets the the model fixity at locaiton x. If the node exists, update it. If the node doesn't
        exist, then a new node will be added

        Parameters
        ----------
        x : float
            The x coordinant of the noded to be modified/added.
        fixity : list
            A list of the input fixities for each possible degree of freedom. 
            Each node will have three degree of freedoms; [x, y, :math:`\\theta`]
            1 represents a fixed condition, 0 represents a free conditon. 
            e.x. [1,1,0]
            A pin conneciton that's fixed in x/y but free in rotation.
        label : str, optional
            The label of the input node. 
            labels are displayed in the plots. The default is ''.
        """

        fixity = self._convertFixityInput(fixity)
        self._checkfixityInput(fixity)
        
        if x in self.nodeCoords:
            index = self._findNode(x)
            self.nodes[index].fixity = fixity
            self.nodes[index].hasReaction = True 
            if label:
                self.nodes[index].label = label 
        else:
            self.addNode(x, fixity, label)        
                 
    def addPointLoad(self, x, pointLoad, label = None):
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
        label : str, optional
            The label of the input node. 
            labels are displayed in the plots. The default is ''.        
        
        """
        
        if hasattr(pointLoad, '__iter__') == False:
            raise Exception('Point load vector must be a list of Numpy array.')
            
        loadID = len(self.pointLoads) + 1
        # Add the load ID to the node in question. Make a node if no ID.
        if x in self.nodeCoords:
            nodeIndex = self._findNode(x)
        else:
            self.addNode(x)
            nodeIndex = self._findNode(x)
        nodeID = nodeIndex + 1
            
        self.nodes[nodeIndex].pointLoadIDs.append(loadID)
        if label:
            self.nodes[nodeIndex].label = label
            
        newLoad = PointLoad(pointLoad, x, nodeID)
        self.pointLoads.append(newLoad)                
         
    def addVerticalLoad(self, x, Py, label=''):
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
            
        """   

        pointLoad = np.array([0., Py, 0.])
        self.addPointLoad(x, pointLoad, label)
        
    def addMoment(self, x, M, label=''):
        """
        Adds a moment ot the model at location x. If no node
        exists at position x, a new node is added.
        Old loads at this point are deleted.
        TODO:
            State which direction positive is.
        
        Parameters
        ----------
        x : float
            The x location to add a moment at.
        M : float
            The magnitude of the moment to be added at x.
        label : str, optional
            The label of the input node. 
            labels are displayed in the plots. The default is ''.
        """        
        pointLoad = np.array([0.,0., M])
        self.addPointLoad(x, pointLoad, label)     
        
    def addHorizontalLoad(self, x, Px, label=''):
        """
        Adds a horizontal point load at the model at location x. If no node
        exists at position x, a new node is added.
        Old loads are deleted.
        x : float
            The x location to add force at.
        Px : float
            The magnitude of the vertical load to be added at x.        
        label : str, optional
            The label of the input node. 
            labels are displayed in the plots. The default is ''.          
        """       
        
        pointLoads = np.array([Px, 0., 0.])
        self.addPointLoad(x, pointLoads, label)            
             
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
        
        defaultFixity = np.array([0,0,0], int)
        # genericPointLoad = np.array([0.,0.,0.], float)
        distLoad = np.array(distLoad)
        
        if x1 not in self.nodeCoords:
            self.addNode(x1, defaultFixity)        
        if x2 not in self.nodeCoords:
            self.addNode(x2, defaultFixity)
        
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

    

    """OuputPropreties"""
    
    
    def Fmax(self, index):
        """
        get the maximum and minimum internal force for teh beam along the 
        appropriate axis. 0:x, 1:y, 2:z
        
        """
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
    
    # def getMaxDisp(self):
    #     disps = [None]*self.Nnodes*2
    #     for ii in self.Nnodes:
    #         disps[ii:ii+1] = self.nodes[ii].disp
    #         node.
    #     return 

# =============================================================================
# 
# =============================================================================




def newEulerBeam2D(x2, x1 = 0, meshSize = 101):
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

    Returns
    -------
    EulerBeam2D : EulerBeam2D
        The the beam intialized with the mesh of points between x1 and x2.
    """
    
    if x2 <= x1:
        raise Exception('x2 must be greater than x1')
    
    x = np.linspace(x1, x2, meshSize)  
    
    return EulerBeam2D(x)

def newSimpleEulerBeam2D(x2, x1 = 0, meshSize = 101, q = 0):
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
        The simply supported



    Returns
    -------
    EulerBeam2D : EulerBeam2D
        The the beam intialized with the mesh of points between x1 and x2.
    """
    
    if x2 <= x1:
        raise Exception('x2 must be greater than x1')
    
    x = np.linspace(x1, x2, meshSize)  
    
    beam  = EulerBeam2D(x)
    beam.addNode(x1, [1,1,0])
    beam.addNode(x2, [0,1,0])
    if q != 0:
        beam.addDistLoad(x1, x2, q)
    return beam



class EulerBeam2D(Beam2D):
    """
    A creates a 2D Euler beam. Information about the beam is stored in a mesh
    of nodes across the beam that are added by the user. Note that only output
    information at the nodes will be contained in the analysis. 
    
    The units of the beam must form a consistent unit base for FEM
    
    Inherits from the base :py:class:`Beam2D` class.
    
    
    Parameters
    ----------
    xcoords : list, optional
        The x coodinates of nodes along the beam the beam. The default is [],
        which starts with no nodes.
    fixity : list
        A list of fixities for the beam. Each fizity is a list of the input 
        fixities for each possible degree of freedom. 
        Each node will have three degree of freedoms; [x, y, :math:`\\theta`]
        1 represents a fixed condition, 0 represents a free conditon. 
        e.x. [1,1,0]
        A pin conneciton that's fixed in x/y but free in rotation.
    labels : list, optional
        A list of labels for each node. The default is [], which gives no label
        to each node.
    section : Section2D, optional
        The section to use in the anaysis. The default uses SectionBasic2D().
    """
    
    # TODO: this is somewhat problematic as beam references the same list..
    def __init__(self, xcoords:list = None, fixities:list = None, labels:list = None,
                 section = None):
        # geomTransform has values 'Linear' or 'PDelta'
        self._initArrays()
        self.nodes = []
        self.eleLoads = []
        
        if xcoords is None:
            xcoords = []
        if fixities is None:
            fixities = []
        if labels is None:
            labels = []
        if section is None:
            section = SectionBasic2D()
        
        self.Nnodes = 0
        NnewNodes = len(xcoords)
        
        fixities = self._initFixities(fixities, NnewNodes)
                
        if len(labels) == 0:
            labels = [None] * NnewNodes     
        
        if len(xcoords) != 0:
            self.addNodes(xcoords, fixities, labels)
        
        self.section = section
        self.d = 1
        self.materialPropreties = [section.A, section.E, section.Ixx]        
        self.plotter = None
        self.EleType = 'elasticBeamColumn'
      
    def _parseCoords(self, xcoords):
        if type(xcoords) == float:
            xcoords = [xcoords]
        if len(xcoords) == 1:
            xcoords = [0] + xcoords
               
      
    def _initFixities(self, fixities, NnewNodes):
        if len(fixities) == 0:
            fixities = [np.array([0., 0., 0.])] * NnewNodes
        if len(fixities) != NnewNodes:
            raise Exception('A fixity must be provided for each node.')
        return fixities
            
    
    def getMoment(self):
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
        return self.getInternalForce(2)
        
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
            # print(node.hasReaction)
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

@dataclass()
class EleLoad:
    """
    Representes a distrubted element load between two points x1 x2. 
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
    
    
    def __init__(self, x1, x2, distLoad, label = ''):

        self.x1 = x1
        self.x2 = x2
        self.P = distLoad
        self.label = label



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
    
    P = np.array([0.,0.,0.])
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
        
