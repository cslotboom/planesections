import openseespy.opensees as op
import numpy as np
import matplotlib.pyplot as plt



# =============================================================================
# Future additons:
#  - plotting features
#  - Timoshenko beams
#  - Mass for dynamic analysis
#  - web interface
# =============================================================================




# =============================================================================
# Problems:
# =============================================================================
# Summarize Nodes?
# Summarize Loads?

class beamBuilder():
       
    def sortNodes(self):
        """
        Sorts and renames the nodes based on their x coordinate.
        """        
        
        xcoords = np.zeros(self.Nnodes)
        for ii, node in enumerate(self.nodes):
            xcoords[ii] = node.x
            
        sortedInd = np.argsort(xcoords)
        sortedNodes = np.array(self.nodes)[sortedInd]
        
        self.nodes = list(sortedNodes)
        
        self.relabelNodes()
        
    def relabelNodes(self):
        """
        renames all the nodes based on their position in the list.
        """
        for ii, node in enumerate(self.nodes):
            node.ID = int(ii + 1)
    
    def addNode(self, x, fixity = np.array([0.,0.,0.]), pointLoad = np.array([0.,0.,0.]), ID = None):
        """
        Adds a new node to the model builder.

        Parameters
        ----------
        x : flaot
            DESCRIPTION.
        fixity : np.array
            The fixity array. Contains 3 values, one for each dof in order
            x, y, rotation. 1 means the system is fixed at said node, 
            0 means their is no fixity conditon.
        pointLoad : np.array
            The array of loads applied ot the system. Contains 3 values, 
            ne for each dof in order Px, Py, Moment.
        ID : int, optional
            The ID of the node in question. Nodes are ordered by position,
            starting at the left most node and ending with the right most node.
            1 --- 2 ---3 - 4 ------- ... -- N

        Returns
        -------
        None.

        """

        self.Nnodes += 1
        
        if ID == None:
            ID = self.Nnodes
        
        newNode = Node(x, fixity, pointLoad, ID)
        self.nodes.append(newNode)
        self.nodeCoords.add(x)
        
        self.sortNodes()
    
    
    def setFixity(self, x, fixity):
        index = self._findNode(x)
        
        if x in self.nodeCoords:
            index = self._findNode(x)
            self.nodes[index].fixity = fixity
        else:
            self.addNode(x, fixity)        
        
    
    
    def addNodes(self, xCoords, fixities = [], pointLoads = [] ):
        
        newNoads = len(xCoords)
        if fixities == []:
            fixities = [np.array([0.,0.,0.])]*newNoads
            
        if pointLoads == []:
            pointLoads = [np.array([0.,0.,0.])]*newNoads
            
        for ii in range(newNoads):
            self.addNode(xCoords[ii], fixities[ii], pointLoads[ii])
                            
    
    def addPointLoads(self, x, pointLoad):
        """
        Adds a load ot the model at location x.
        Old loads are deleted
        """
        # Check if the node is in the list of coordinates used
        if x in self.nodeCoords:
            index = self._findNode(x)
            self.nodes[index].pointLoad = pointLoad
            
        else:
            fixity = np.array([0,0,0], int)
            self.addNode(x, fixity, pointLoad)
            
    def addVerticalLoad(self, x, Py):
        pointLoads = np.array([0., Py, 0.])
        self.addPointLoads(x, pointLoads)
        
    def addMoment(self, x, M):
        pointLoads = np.array([0.,0., M])
        self.addPointLoads(x, pointLoads)     
        
    def addHorizontalLoad(self, x, Px):
        pointLoads = np.array([Px, 0., 0.])
        self.addPointLoads(x, pointLoads)            
             
    def _findNode(self, xInput):
        
        for ii, node in enumerate(self.nodes):
            if xInput == node.x:
                return ii
            
    def addDistLoads(self, x1, x2, distLoad):
        """
        
        Parameters
        ----------
        x1 : float
            DESCRIPTION.
        x2 : float
            DESCRIPTION.
        distLoad : 2D array
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        genericFixity = np.array([0,0,0], int)
        genericPointLoad = np.array([0,0,0], int)
        
        if x1 not in self.nodeCoords:
            self.addNode(x1, genericFixity, genericPointLoad)        
        if x2 not in self.nodeCoords:
            self.addNode(x2, genericFixity, genericPointLoad)
        
        newEleLoad = EleLoad(x1, x2, distLoad)
        self.eleLoads.append(newEleLoad)

    def addDistLoadVertical(self, x1, x2, qy):

        distLoad = np.array([0., qy])
        
        self.addDistLoads(self, x1, x2, distLoad)

    def addDistLoadHorizontal(self, x1, x2, qx):

        distLoad = np.array([qx, 0.])
        genericFixity = np.array([0,0,0], int)
        genericPointLoad = np.array([0,0,0], int)
        
        if x1 not in self.nodeCoords:
            self.addNode(x1, genericFixity, genericPointLoad)        
        if x2 not in self.nodeCoords:
            self.addNode(x2, genericFixity, genericPointLoad)
        
        newEleLoad = EleLoad(x1, x2, distLoad)
        self.eleLoads.append(newEleLoad)

    def plot(self):
        xcoords = np.array(list(self.nodeCoords))
        y = np.zeros_like(xcoords)
        plt.plot(xcoords, y)
        plt.plot(xcoords, y, '.')

# =============================================================================
# 
# =============================================================================







class EulerBeam(beamBuilder):

    def __init__(self, E = 1., A=1., I=1., xcoords = [], fixities = [], geomTransform = 'Linear'):
        
        # geomTransform has values 'Linear' or 'PDelta'
        self.nodes = []
        self.eleLoads = []
        self.nodeCoords = set()
        
        self.materialPropreties = [E, A, I]  
            
        self.Nnodes = 0
        newNoads = len(xcoords)
        pointLoad = np.array([0., 0., 0.])
        for ii in range(newNoads):
            self.addNode(xcoords[ii], fixities[ii], pointLoad)
        
        self.plotter = None
        
        self.geomTransform = geomTransform
        self.EleType = 'elasticBeamColumn'


class Node():
       
    def __init__(self, x, fixity, pointLoad, ID):
        self.x = x
        self.pointLoad = pointLoad
        self.fixity = fixity
        self.ID = ID
        
        self.disp = None
        self.reaction = None
        self.internalForce = None


# class Element():
       
#     def __init__(self, endNodes, eleLoad, ID):
#         self.endNodes = endNodes
#         self.eleLoad = eleLoad
#         self.ID = ID



class EleLoad():
    def __init__(self, x1, x2, distLoad):
        self.x1 = x1
        self.x2 = x2
        self.load = distLoad




class PointLoad():
    P = np.array([0.,0.,0.])
    x = 0.
    
    def __init__(self, P):
        pass

class DistLoad():
    
    def __init__(self, ):
    
        pass
       
    
class PlotBeam():

    def __init__(self):
        pass
    
    def initBeamPlot(self):
        fig, ax = plt.subplots()
    
    


def plotMoment(beam):
    
    
    # Plotbeam....
    
    
    xcoords = np.zeros(beam.Nnodes)
    moment = np.zeros(beam.Nnodes)
    for ii, node in enumerate(beam.nodes):
        xcoords[ii] = node.x
        moment[ii] = node.internalForce[2]
        # moment[ii] = 
    
    fig, ax = plt.subplots()
    plt.plot(xcoords,moment)
        
        
def plotShear(beam):
    
    
    # Plotbeam....
    
    
    xcoords = np.zeros(beam.Nnodes)
    moment = np.zeros(beam.Nnodes)
    for ii, node in enumerate(beam.nodes):
        xcoords[ii] = node.x
        moment[ii] = node.internalForce[1]
        # moment[ii] = 
    
    fig, ax = plt.subplots()
    plt.plot(xcoords,moment)     
    
    
    
    
    
        
