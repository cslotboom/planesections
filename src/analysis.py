import openseespy.opensees as op
import numpy as np
import matplotlib.pyplot as plt

        
class OutputRecorder2D():
      
    
    def __init__(self, beam):
        # Nnodes = beam.Nnodes
        # dispOut = np.zeros((Nnodes,3))
        # reactOut = 
        
        self.Nnodes = beam.Nnodes
        self.nodeID0 = 1
        self.nodeIDEnd = self.Nnodes
        # self.Nele = beam.Nnodes - 1
        
        # endNode = beam.Nnodes
        for ii, node in enumerate(beam.nodes):
            ID = node.ID
            # print(ID)
            
            node.disps = np.array(op.nodeDisp(ID))
            node.rFrc  = np.array(op.nodeReaction(ID))
            node.Fint = self.getEleInteralForce(ID)

    def getEleInteralForce(self, nodID):
        """
        
        Gets the internal force at the left and right side of a node.
        
         N-1  L R  N
        .------.------.
        N-1    N      N+1
        
        
        """

        Fint = np.zeros(6)
        
        if nodID == self.nodeID0: # Left most node
        
            eleR = nodID      
        
            # 0 is used to so that the plot "closes", i.e. starts at zero the goes up
            Fint[:3] =  0                                   # Left side forces
            Fint[3:] =  op.eleForce(eleR)[:3]             # Right side forces
            # Fint[3:] = op.eleForce(nodeID)[:3] # Right side forces
            # Fint[:3] = Fint[3:]                # Left side forces
            
        #Direct Check, this is scary.
        elif nodID == self.nodeIDEnd: # right side node
            eleL = nodID - 1
            Fint[:3] = -np.array(op.eleForce(eleL)[3:]) # Right side forces
            Fint[3:] = 0                               # Left side forces
        else: # center nodes
        
            eleL = nodID - 1
            eleR = nodID      

            Fint[:3] = -np.array(op.eleForce(eleL)[3:]) # left entries
            Fint[3:] =  np.array(op.eleForce(eleR)[:3]) # right entries
        
        return Fint
        
            

        
class OpenSeesAnalyzer2D():
    """
    Builds the beam in OpenSees
    
    Note, nodes and elements will both start at 0 instead of 1.
    
    """
    def __init__(self, beam2D, recorder = OutputRecorder2D):
        """
        
        Parameters
        ----------
         : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.beam = beam2D
        
        self.Nnode = beam2D.Nnodes
        self.Nele = self.Nnode - 1
        self.recorder = OutputRecorder2D
        
    def initModel(self):
        op.wipe()
        op.model('Basic' , '-ndm',  2)
        op.geomTransf(self.beam.geomTransform, 1)
        
    
    def buildNodes(self):
        """
        Adds the nodes to the OpenSeesPy model.
        """

        for node in self.beam.nodes:
            op.node(int(node.ID), float(node.x), 0.)
            # OpenSees is very finicky with these inputs, so I'm individually inting them
            f1, f2, f3 = node.fixity
            op.fix(node.ID, int(f1), int(f2), int(f3))
        
    def buildEulerBeams(self):
        beam = self.beam
        matPropreties = beam.materialPropreties
        for ii in range(self.Nele):
            # ID = ii
            ID = ii + 1
            eleID = int(ID)
            Ni = int(ID)
            Nj = int(ID + 1)
            op.element(beam.EleType,  eleID , Ni, Nj , *matPropreties, 1)

    
    # def buildPointLoads(self):
    #     op.timeSeries('Linear',1)
    #     op.pattern('Plain', 1, 1)
    #     for node in self.beam.nodes:
    #         op.load(node.ID, *node.pointLoad)
            
    
    def buildPointLoads(self):
        op.timeSeries('Linear',1)
        op.pattern('Plain', 1, 1)
        for load in self.beam.pointLoads:
            op.load(int(load.nodeID), *load.P)            
            
    
    def buildAnalysisPropreties(self):
        # op.constraints("Transformation")
        op.constraints("Lagrange")
        op.numberer("Plain")
        op.system('BandGeneral')
        op.test('NormDispIncr',  1.*10**-8, 40, 0 , 2)
        # op.algorithm('Newton')
        op.algorithm('Linear')
        op.integrator('LoadControl',1.)
        op.analysis('Static')

    def analyze(self):
        # opp.plot_model('nodes')
        ok = op.analyze(1)
        op.reactions()   
        
    
    def buildEleLoads(self):
        op.timeSeries('Linear',2)
        op.pattern('Plain', 2, 2)
        
        for eleload in self.beam.eleLoads:
            # print(load.x1, load.x2)
            N1 = self.beam._findNode(eleload.x1) + 1
            N2 = self.beam._findNode(eleload.x2) + 1
            
            load = eleload.load
            
            for ii in range(N1, N2):                
                op.eleLoad('-ele', int(ii), '-type', '-beamUniform', load[1], load[0])
    
    
    def runAnalysis(self, recordOutput = True):
        """
        Makes the beam in OpenSees.

        Returns
        -------
        None.

        """
        
        self.initModel()
        self.buildNodes()   
        self.buildEulerBeams()
        self.buildPointLoads()
        self.buildEleLoads()   
        self.buildAnalysisPropreties()
        self.analyze()
        
        
        if recordOutput == True:
            self.recorder(self.beam)


            