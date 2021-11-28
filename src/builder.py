import openseespy.opensees as op
import numpy as np
import matplotlib.pyplot as plt



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
    
    def _addedNodeMessage(self, x):
        print(f'New node added at: {x}')
    
    def addNode(self, x, fixity = np.array([0.,0.,0.]), pointLoad = np.array([0.,0.,0.]), ID = None):
        """
        Adds a new node to the model builder.

        Parameters
        ----------
        x : flaot
            The x coordinate of the node.
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
        
    def addNodes(self, xCoords, fixities = None, pointLoads = None ):
        
        
        
        newNoads = len(xCoords)
        self.Nnodes += newNoads
        
        if fixities == None:
            fixities = [np.array([0.,0.,0.])]*newNoads
            
        if pointLoads is None:
            pointLoads = [np.array([0.,0.,0.])]*newNoads
            
        # for ii in range(newNoads):
        #     self.addNode(xCoords[ii], fixities[ii], pointLoads[ii])    
        for ii in range(newNoads):
            newNode = Node(xCoords[ii], fixities[ii], pointLoads[ii], ii)
            self.nodes.append(newNode)
            self.nodeCoords.add(xCoords[ii])
            # self.addNode(xCoords[ii], fixities[ii], pointLoads[ii])        
    
    
    
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
        Old loads are deleted.
        
        Parameters
        ----------
        x : float
            The loaciton of the load.
        pointLoad : list
            A list of the forces in [Fx, Fy, M].

        """
        # Check if the node is in the list of coordinates used
        if x in self.nodeCoords:
            index = self._findNode(x)
            self.nodes[index].pointLoad = pointLoad
        else:
            fixity = np.array([0,0,0], int)
            self.addNode(x, fixity, pointLoad)
     
    def addPointLoads(self, x, pointLoad):
        pass

    
    def addVerticalLoad(self, x, Py):
        """
        Adds a vertical load to the model at location x.
        Old loads are deleted.
        """        

        pointLoad = np.array([0., Py, 0.])
        self.addPointLoad(x, pointLoad)
        
    def addMoment(self, x, M):
        """
        Adds a Moment ot the model at location x.
        Old loads are deleted.
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
             
    def _findNode(self, xInput):
        
        for ii, node in enumerate(self.nodes):
            if xInput == node.x:
                return ii
            
    def addDistLoad(self, x1, x2, distLoad):
        """
        
        Parameters
        ----------
        x1 : start point of distributed load
            DESCRIPTION.
        x2 : end point of distributed load
            DESCRIPTION.
        distLoad : 2D array
            DESCRIPTION.

        Returns
        -------
        None.

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

        distLoad = np.array([0., qy])
        
        self.addDistLoad(x1, x2, distLoad)

    def addDistLoadHorizontal(self, x1, x2, qx):

        distLoad = np.array([qx, 0.])
        genericFixity = np.array([0,0,0], int)
        genericPointLoad = np.array([0,0,0], float)
        
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


    @property
    def Mmax(self):
        return self.Fmax(2)


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

    @property
    def Vmax(self):
        return self.Fmax(1)


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

# =============================================================================
# 
# =============================================================================


#TODO: make intiail mesh
class EulerBeam(beamBuilder):

    def __init__(self, xcoords = [], fixities = [], E = 1., A=1., I=1., geomTransform = 'Linear'):
        
        # geomTransform has values 'Linear' or 'PDelta'
        self.nodes = []
        self.eleLoads = []
        self.nodeCoords = set()
        self.materialPropreties = [E, A, I]  
            
        self.Nnodes = 0
        NnewLoad = len(xcoords)
        pointLoad = [np.array([0., 0., 0.])] * NnewLoad
        
        
        if len(fixities) == 0:
            fixities = [np.array([0., 0., 0.])] * NnewLoad
        self.addNodes(xcoords, fixities, pointLoad)
        
        pointLoad = np.array([0., 0., 0.])
        # for ii in range(NnewLoad):
        #     self.addNode(xcoords[ii], fixities[ii], pointLoad)
        
        self.plotter = None
        
        self.geomTransform = geomTransform
        self.EleType = 'elasticBeamColumn'
    
    # def setReactionNodes:
        
    #     self.reactionNodes = []
    #     for node in self.nodes:
    #         if node.fixity !=


class Node():
       
    def __init__(self, x, fixity, pointLoad, ID):
        self.x = x
        self.pointLoad = pointLoad
        self.fixity = fixity
        self.ID = ID
        
        self.disp = None
        self.rFrc = None
        self.Fint = None
        
        self.hasReaction = False
        if np.any(fixity != [0,0,0]):
            self.hasReaction = True


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
    return plotInternalForce(beam, 2)
        
def plotShear(beam):
    return plotInternalForce(beam, 1)

def plotInternalForce(beam, index):
      
    xcoords = np.zeros(beam.Nnodes*2)
    moment = np.zeros(beam.Nnodes*2)
    for ii, node in enumerate(beam.nodes):
        xcoords[ii*2]       = node.x
        moment[ii*2]        = node.internalForce[index]
        xcoords[ii*2 + 1]   = node.x
        moment[ii*2 + 1]    = node.internalForce[index + 3]
        
        
    fig, ax = plt.subplots()
    line = plt.plot(xcoords, moment)     
    
    return fig, ax, line
  
         
        
def plotVertDisp(beam):
    return plotDisp(beam) 


# def plotVertDisp(beam):
#     return plotDisp() 


def plotDisp(beam, index=1):
    
    
    # Plotbeam....  
    xcoords = np.zeros(beam.Nnodes)
    moment = np.zeros(beam.Nnodes)
    for ii, node in enumerate(beam.nodes):
        xcoords[ii] = node.x
        moment[ii] = node.disps[index]
        # moment[ii] = 
    
    fig, ax = plt.subplots()
    line = plt.plot(xcoords,moment)     
    
    return fig, ax, line   
        