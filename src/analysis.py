import openseespy.opensees as op
import openseespy.postprocessing.Get_Rendering as opp
import numpy as np
import matplotlib.pyplot as plt


        
class OpenSeesAnalyzer():
    """
    Builds the beam in OpenSees
    """
    def __init__(self, beam):
        """
        
        Parameters
        ----------
         : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.beam = beam
        
        self.Nnode = beam.Nnodes
        self.Nele = self.Nnode - 1
        
    def initModel(self):
        op.wipe()
        op.model('Basic' , '-ndm',  2)
        
        op.geomTransf(self.beam.geomTransform, 1)
        
    
    def buildNodes(self):
        """
        Adds the nodes to the domain
        """

        for node in self.beam.nodes:
            op.node(node.ID, float(node.x), 0.)
            # OpenSees is very finicky with these inputs, so I'm individually
            # converting to int.
            f1, f2, f3 = node.fixity
            op.fix(node.ID, int(f1), int(f2), int(f3))
        
    def buildEulerBeams(self):
        beam = self.beam
        matPropreties = beam.materialPropreties
        for ii in range(self.Nele):
            ID = ii + 1
            eleID = int(ID)
            Ni = int(ID)
            Nj = int(ID + 1)
            op.element(beam.EleType,  ID , Ni, Nj , *matPropreties, 1)

    
    def buildPointLoads(self):
        op.timeSeries('Linear',1)
        op.pattern('Plain', 1, 1)
        for node in self.beam.nodes:
            op.load(node.ID, *node.pointLoad)
    
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
    
    
    def runAnalysis(self):
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
        
        
class RecordOutput():
    
    def __init__(self, beam):
        # Nnodes = beam.Nnodes
        # dispOut = np.zeros((Nnodes,3))
        # reactOut = 
        
        endNode = beam.Nnodes
        for ii, node in enumerate(beam.nodes):
            ID = node.ID
            node.disps = np.array(op.nodeDisp(ID))
            node.react = np.array(op.nodeReaction(ID))
            
            # If we aren't the last entry
            if  ii + 1 != endNode:
                node.internalForce = np.array(op.eleForce(ID)[:3])
            else:
                node.internalForce = -np.array(op.eleForce(ID-1)[:3])
            
            
    