import numpy as np
import planesections.builder as bb 

from PyNite.FEModel3D import FEModel3D

from .recorder import OutputRecorder

class OutputRecorderPyNite2D(OutputRecorder):
    """
    An interface that can be used to get beam internal forces for each node
    in the model. 
    When called on a beam, it will get all internal forces for that beam.
    Information at each node in the model is stored in the beam.
    The recorder is only is not instantiated at the time of recording. 

    Parameters
    ----------
    beam : planesections Beam2D
        The beam whose data is being recorded.

    """
    lcName = 'Combo 1'
    def __init__(self, beam:bb.Beam, analysisBeam):       
        self.Nnodes = beam.Nnodes
        self.nodeID0 = 1
        self.nodeIDEnd = self.Nnodes
        self.ndf = beam._ndf        
        self.analysisBeam = analysisBeam
        for ii, ID in enumerate(analysisBeam.nodes.keys()):
            analysisNode = analysisBeam.nodes[ID]
            disps = [analysisNode.DX[self.lcName], analysisNode.DY[self.lcName], analysisNode.RZ[self.lcName]]
            rFrc  = [analysisNode.RxnFX[self.lcName], analysisNode.RxnFY[self.lcName], analysisNode.RxnMZ[self.lcName]]
            
            # assign values
            node = beam.nodes[ii]
            node.disps = np.array(disps)
            node.rFrc  = np.array(rFrc)
            node.Fint  = self.getEleInteralForce(ii)

    def _getFint(self, ele):
        PyL, PyR = ele.axial_array(2)[1]
        VyL, VyR = ele.shear_array('Fy', 2)[1]
        MyL, MyR = ele.moment_array('Mz', 2)[1]
        
        return np.array([PyL, VyL, MyL]), np.array([PyR, VyR, MyR])

    def getEleInteralForce(self, nodeID:int):
        """
        Gets the internal force at the left and right side of a node.
        The left and right side forces represent internal force at either side
        of a section cut.       
        
        """
        ndf = self.ndf
        Fint = np.zeros(ndf*2)
        
        nodeID += 1
        
        if nodeID == self.nodeID0: # Left most node
            eleRID = 'M' + str(nodeID)   
            eleR = self.analysisBeam.members[eleRID]
            # 0 is used to so that the plot "closes", i.e. starts at zero the goes up
            Fint[:ndf] =  0    

            FeleR_L, _ = self._getFint(eleR)
            Fint[ndf:] =  FeleR_L    # Left side forces for right side element
                                    
        elif nodeID == self.nodeIDEnd: # right side node
            eleLID = 'M' + str(int(nodeID - 1))   
            eleL = self.analysisBeam.members[eleLID]

            _, FeleL_R = self._getFint(eleL)
            Fint[:ndf] = FeleL_R # Right side forces
            Fint[ndf:] = 0   
                            # Left side forces
        else: # center nodes
        
            eleLID = 'M' + str(int(nodeID - 1))   
            eleRID = 'M' + str(int(nodeID))
            eleL = self.analysisBeam.members[eleLID]
            eleR = self.analysisBeam.members[eleRID]
            _, FeleL_R = self._getFint(eleL)
            FeleR_L, _ = self._getFint(eleR)


            Fint[:ndf] = FeleL_R # left entries
            Fint[ndf:] = FeleR_L # right entries
        
        return Fint


class PyNiteAnalyzer2D:
    """
    This class is used to  can be used to create and run an analysis of an 
    input 2D beam using OpenSeesPy. The nodes, elements, sections, and 
    forces for the beam are defined in the analysis model
    
    The PyNite solver makes use of a beam object, which is constructed and
    stored as a analysisBeam attribute
    
    Note, nodes and elements will both start at 0 instead of 1.
    
    For the PyNite beam, The 2D directions are X/Y
    
    Parameters
    ----------
    beam : planesections Beam2D
        The beam whose data is being recorded.
    recorder : planesections Recorder
        The recorder to use for the output beam.
    geomTransform: str, optional
        The OpenSees Geometry transform to use. Can be "Linear" or "PDelta"
    clearOld : bool, optional
        A flag that can be used to turn on or off clearing the old analysis
        when the beam is created.
        There are some very niche cases where users may want to have mutiple
        beams at once in the OpenSees model.
        However, this should remain true for nearly all analyses. 
        Do not turn on unless you know what you're doing.
        
    """
    def __init__(self, beam2D:bb.Beam, recorder = OutputRecorderPyNite2D):

        
        self.beam:bb.Beam = beam2D
        self._checkBeam(beam2D)
        
        self.Nnode = beam2D.Nnodes
        self.Nele = self.Nnode - 1
        self.recorder = recorder
        
        self.nodeAnalysisNames = []
        self.memberNames = []
        
        self.matName = 'baseMat'
    
    def _checkBeam(self, beam2D):
        if not beam2D._dimension:
            raise Exception("The beam has no dimension, something terrible has happened.")
        if beam2D._dimension != '2D':
            raise Exception(f"The beam has dimension of type {beam2D._dimension}, it should have type '2D'")
    
    def initModel(self):
        """
        Initializes the model. 

        Parameters
        ----------
        clearOld : bool, optional
            A flag that can be used to turn on or off clearing the old analysis
            when the beam is created.
            There are some very niche cases where users may want to have mutiple
            beams at once in the OpenSees model.
            However, this should remain true for nearly all analyses. 
            Do not turn on unless you know what you're doing.
        """
        
        self.analysisBeam = FEModel3D()
        
    
    def buildNodes(self):
        """
        Adds each node in the beam to the OpenSeesPy model, and assigns 
        that node a fixity.
        """
        analysisBeam = self.analysisBeam


        for ii, node in enumerate(self.beam.nodes):
            name = 'N' + str(node.ID)
            self.nodeAnalysisNames.append(name)
            analysisBeam.add_node(name, node.x, 0, 0)
            
            if node.hasReaction:
                f1, f2, f3 = node.fixity.fixityValues
                analysisBeam.def_support(name, f1, f2, True, True, False, f3)
        
    def buildEulerBeams(self):
        """
        Creates an elastic Euler beam between each node in the model.
        """        
        beam = self.beam
        nodeAnalysisNames = self.nodeAnalysisNames
        E, G, A, Iz = beam.getMaterialPropreties()
        
        memberNames = []
        # this is sloppy, we supply empty values
        self.analysisBeam.add_material(self.matName, E, G, 0.3, 8000)
        for ii in range(self.Nele):
            memberName = 'M' + str(int(ii+1))
            N1 = nodeAnalysisNames[ii]
            N2 = nodeAnalysisNames[ii+1]            
            self.analysisBeam.add_member(memberName, N1, N2, self.matName, 1., Iz, 1., A)
            memberNames.append(memberName)
        self.memberNames = memberNames
           
    
    def _buildPointLoads(self, pointLoads):
        for load in pointLoads:
            node = 'N' + str(load.nodeID)
            Fx, Fy, M = load.P
            self.analysisBeam.add_node_load(node, 'FY', Fy)
            self.analysisBeam.add_node_load(node, 'FX', Fx)
            self.analysisBeam.add_node_load(node, 'MZ', M)
            
    def buildPointLoads(self):
        """
        Applies point loads to the appropriate nodes in the model.
        """        
        self._buildPointLoads(self.beam.pointLoads)       
    
    def analyze(self):
        """
        Analyzes the model once and records outputs.
        """
        self.analysisBeam.analyze(check_statics=False)
    
    def buildEleLoads(self):
        """
        Applies element loads to the appropriate elements in the model.
        """
        
        for eleload in self.beam.eleLoads:
            N1 = self.beam._findNode(eleload.x1) + 1
            N2 = self.beam._findNode(eleload.x2) + 1
            build = self._selectLoad(eleload)
            build([N1, N2], eleload)
            
    def _selectLoad(self, eleload):
        if isinstance(eleload, bb.EleLoadDist):
            return self._buildDistLoad
        if isinstance(eleload, bb.EleLoadLinear):
            return self._buildLinLoad
    
    def _buildDistLoad(self, Nodes:list[int], eleload:bb.EleLoadDist):
        N1, N2 = Nodes
        memberNames = self.memberNames
        q = eleload.P
        
        # We subtract one because node names are the index +1
        for ii in range(N1-1, N2-1):
            memberName = memberNames[ii]
            self.analysisBeam.add_member_dist_load(memberName, 'Fy', q[1], q[1])
            self.analysisBeam.add_member_dist_load(memberName, 'Fx', q[0], q[0])
    
    def _buildLinLoad(self, Nodes:list[int], eleload:bb.EleLoadLinear):
        N1, N2 = Nodes
        memberNames = self.memberNames
        q = eleload.P
        for ii in range(N1-1, N2-1): # shift one back because indicies are one less
            memberName = memberNames[ii] 
            
            Node1 = self.beam.nodes[ii]
            Node2 = self.beam.nodes[ii + 1]
            
            qx1, qx2 = eleload.getLoadComponents(Node1.x, Node2.x, q[0])
            qy1, qy2 = eleload.getLoadComponents(Node1.x, Node2.x, q[1]) 
            
            self.analysisBeam.add_member_dist_load(memberName, 'Fy', qy1, qy2)
            self.analysisBeam.add_member_dist_load(memberName, 'Fx', qx1, qx2)
    
    def _getBeam(self):
        return self.analysisBeam
    
    def runAnalysis(self, recordOutput = True):
        """
        Makes and analyzes the beam with PyNite.

        Returns
        -------
        None.

        """
        
        self.initModel()
        self.buildNodes()   
        self.buildEulerBeams()
        self.buildPointLoads()
        self.buildEleLoads()   
        self.analyze()
                
        if recordOutput == True:
            self.recorder(self.beam, self.analysisBeam)


