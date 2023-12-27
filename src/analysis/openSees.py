
import numpy as np
import planesections.builder as bb 

try:
    import openseespy.opensees as op
except:
    raise Exception('OpenSeespy has not been installed. First include optional depependancy with "pip -m install planesections[opensees]"')


from .recorder import OutputRecorder
        
class OutputRecorderOpenSees(OutputRecorder):
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
    def __init__(self, beam:bb.Beam):

        
        self.Nnodes = beam.Nnodes
        self.nodeID0 = 1
        self.nodeIDEnd = self.Nnodes
        self.ndf = beam._ndf
        
        for ii, node in enumerate(beam.nodes):
            ID = node.ID            
            node.disps = np.array(op.nodeDisp(ID))
            node.rFrc  = np.array(op.nodeReaction(ID))
            node.Fint  = self.getEleInteralForce(ID)

    def getEleInteralForce(self, nodID:int):
        """
        Gets the internal force at the left and right side of a node.
        The left and right side forces represent internal force at either side
        of a section cut.       
        
        """
        ndf = self.ndf
        Fint = np.zeros(ndf*2)
        if nodID == self.nodeID0: # Left most node
            eleR = nodID      
            # 0 is used to so that the plot "closes", i.e. starts at zero the goes up
            Fint[:ndf] =  0                                   # Left side forces
            Fint[ndf:] =  op.eleForce(eleR)[:ndf]             # Right side forces
            
        #Direct Check, this is scary.
        elif nodID == self.nodeIDEnd: # right side node
            eleL = nodID - 1
            Fint[:ndf] = -np.array(op.eleForce(eleL)[ndf:]) # Right side forces
            Fint[ndf:] = 0                               # Left side forces
        else: # center nodes
            eleL = nodID - 1
            eleR = nodID      

            Fint[:ndf] = -np.array(op.eleForce(eleL)[ndf:]) # left entries
            Fint[ndf:] =  np.array(op.eleForce(eleR)[:ndf]) # right entries
        
        return Fint


class OutputRecorder2D(OutputRecorderOpenSees):
        
    def __post_init__(self):
        print('OutputRecorder2D is depcricated and will be removed in a next release. Use OutputRecorder instead')
        


class OpenSeesAnalyzer2D:
    """
    This class is used to  can be used to create and run an analysis of an 
    input 2D beam using OpenSeesPy. The nodes, elements, sections, and 
    forces for the beam are defined in the analysis model
    
    Note, nodes and elements will both start at 0 instead of 1.        
    
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
    def __init__(self, beam2D:bb.Beam, recorder = OutputRecorderOpenSees, 
                 geomTransform = 'Linear', clearOld = True):

        self.beam:bb.Beam = beam2D
        self._checkBeam(beam2D)
        
        self.Nnode = beam2D.Nnodes
        self.Nele = self.Nnode - 1
        self.recorder = recorder
        self.geomTransform = geomTransform
        self.clearOld = clearOld
    
    def _checkBeam(self, beam2D):
        if not beam2D._dimension:
            raise Exception("The beam has no dimension, something terible has happened.")
        if beam2D._dimension != '2D':
            raise Exception(f"The beam has dimension of type {beam2D._dimension}, it should have type '2D'")
    
    def initModel(self, clearOld = True):
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
        
        if clearOld:
            op.wipe()
        op.model('Basic' , '-ndm',  2)
        op.geomTransf(self.geomTransform, 1)
        
    
    def buildNodes(self):
        """
        Adds each node in the beam to the OpenSeesPy model, and assigns 
        that node a fixity.
        """

        for node in self.beam.nodes:
            op.node(int(node.ID), float(node.x), 0.)
            
            # OpenSees is very finicky with these inputs, int them for saftey.
            f1, f2, f3 = node.fixity.fixityValues
            op.fix(node.ID, int(f1), int(f2), int(f3))
        
    def buildEulerBeams(self):
        """
        Creates an elastic Euler beam between each node in the model.
        """        
        beam = self.beam
        E, G, A, Iz = beam.getMaterialPropreties()
        for ii in range(self.Nele):
            ID = ii + 1
            eleID = int(ID)
            Ni = int(ID)
            Nj = int(ID + 1)
            # elasticBeamColumn eleTag iNode $jNode $A $E $Iz $transfTag <-release $relcode> <-mass $massDens> <-cMass>
            op.element(beam.EleType, eleID , Ni, Nj, A, E, Iz, 1)
           
    
    def _buildPointLoads(self, pointLoads):
        for load in pointLoads:
            op.load(int(load.nodeID), *load.P)
            
            
    def buildPointLoads(self):
        """
        Applies point loads to the appropriate nodes in the model.
        """        
        op.timeSeries('Linear',1)
        op.pattern('Plain', 1, 1)
        self._buildPointLoads(self.beam.pointLoads)       
    
    def buildAnalysisPropreties(self):
        """
        Typical openSeesPy propreties that should work for any linear beam.
        A linear algorithm is used because there is no nonlienarity in the beam.
        """
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
        """
        Analyzes the model once and records outputs.
        """
        ok = op.analyze(1)
        op.reactions()   
        return ok
    
    def buildEleLoads(self):
        """
        Applies element loads to the appropriate elements in the model.
        """
        op.timeSeries('Linear',2)
        op.pattern('Plain', 2, 2)
        
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
    
    def _buildDistLoad(self, Nodes:list[int], eleload:bb.EleLoadLinear):
        load = eleload.P
        N1, N2 = Nodes[0], Nodes[1]
        for ii in range(N1, N2):                
            op.eleLoad('-ele', int(ii), 
                       '-type', '-beamUniform', load[1], load[0])   
    
    def _buildLinLoad(self, Nodes:list[int], eleload:bb.EleLoadLinear):
        load = eleload.P
        N1, N2 = Nodes[0], Nodes[1]
        for ii in range(N1, N2):                
            Node1 = self.beam.nodes[ii - 1]
            Node2 = self.beam.nodes[ii]
            qx1, qx2 = eleload.getLoadComponents(Node1.x, Node2.x, load[0])
            qy1, qy2 = eleload.getLoadComponents(Node1.x, Node2.x, load[1]) 

            aOverL = 0.
            bOverL = 1.
            op.eleLoad('-ele',int(ii),
                        '-type','beamUniform',
                        qy1, qx1, aOverL, bOverL, qy2, qx2)       
    
    def runAnalysis(self, recordOutput = True):
        """
        Makes and analyzes the beam in OpenSees.

        Returns
        -------
        None.

        """
        
        self.initModel(self.clearOld)
        self.buildNodes()   
        self.buildEulerBeams()
        self.buildPointLoads()
        self.buildEleLoads()   
        self.buildAnalysisPropreties()
        self.analyze()
        
        if recordOutput == True:
            self.recorder(self.beam)

                  
class OpenSeesAnalyzer3D:
    """
    This class is used to  can be used to create and run an analysis of an 
    input 2D beam using OpenSeesPy. The nodes, elements, sections, and 
    forces for the beam are defined in the analysis model
    
    Note, nodes and elements will both start at 0 instead of 1.        
    
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

    def __init__(self, beam3D:bb.Beam, recorder = OutputRecorderOpenSees, 
                 geomTransform = 'Linear', clearOld = True):

        self.beam = beam3D
        self._checkBeam(beam3D)
        
        self.Nnode = beam3D.Nnodes
        self.Nele = self.Nnode - 1
        self.recorder = OutputRecorderOpenSees
        self.geomTransform = geomTransform
        self.clearOld = clearOld
    
    def _checkBeam(self, beam3D):
        if not beam3D._dimension:
            raise Exception("The beam has no dimension, something terible has happened.")
        if beam3D._dimension != '3D':
            raise Exception(f"The beam has dimension of type {beam3D._dimension}, it should have type '3D'")
    
    def initModel(self, clearOld = True):
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
        
        if clearOld:
            op.wipe()
        op.model('Basic' , '-ndm',  3)
        # see https://opensees.berkeley.edu/wiki/index.php/PDelta_Transformation
        op.geomTransf(self.geomTransform, 1, *[0, 0, 1])
        
    
    def buildNodes(self):
        """
        Adds each node in the beam to the OpenSeesPy model, and assigns 
        that node a fixity.
        """

        for node in self.beam.nodes:
            op.node(int(node.ID), float(node.x), 0., 0.)
            
            # OpenSees is very finicky with these inputs, int them for saftey.
            f1, f2, f3, f4, f5, f6 = node.fixity.fixityValues
            op.fix(node.ID, int(f1), int(f2), int(f3), int(f4), int(f5), int(f6))
        
    def buildEulerBeams(self):
        """
        Creates an elastic Euler beam between each node in the model.
        """        
        beam = self.beam
        E, G, A, Iz, Iy, J = beam.getMaterialPropreties()
        for ii in range(self.Nele):
            ID = ii + 1
            eleID = int(ID)
            Ni = int(ID)
            Nj = int(ID + 1)
            # element('elasticBeamColumn', eleTag, *eleNodes, Area, E_mod, G_mod, Jxx, Iy, Iz, transfTag, <'-mass', mass>, <'-cMass'>)
            op.element(beam.EleType,  eleID , Ni, Nj , A, E, G, J, Iy, Iz, 1)
    
    def buildPointLoads(self):
        """
        Applies point loads to the appropriate nodes in the model.
        """        
        op.timeSeries('Linear',1)
        op.pattern('Plain', 1, 1)
        for load in self.beam.pointLoads:
            op.load(int(load.nodeID), *load.P)            
            
    
    def buildAnalysisPropreties(self):
        """
        Typical openSeesPy propreties that should work for any linear beam.
        A linear algorithm is used because there is no nonlienarity in the beam.
        """
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
        """
        Analyzes the model once and records outputs.
        """
        ok = op.analyze(1)
        op.reactions()   
        
    
    def buildEleLoads(self):
        """
        Applies element loads to the appropriate elements in the model.
        """
        op.timeSeries('Linear',2)
        op.pattern('Plain', 2, 2)
        
        for eleload in self.beam.eleLoads:
            N1 = self.beam._findNode(eleload.x1) + 1
            N2 = self.beam._findNode(eleload.x2) + 1
            load = eleload.P
            
            for ii in range(N1, N2):     
                # eleLoad('-ele', *eleTags, '-range', eleTag1, eleTag2, '-type', '-beamUniform', Wy, <Wz>, Wx=0.0, '-beamPoint',Py,<Pz>,xL,Px=0.0,'-beamThermal',*tempPts)
                op.eleLoad('-ele', int(ii), '-type', '-beamUniform', load[1], load[2], load[0])   
    
    def runAnalysis(self, recordOutput = True):
        """
        Makes and analyzes the beam in OpenSees.

        Returns
        -------
        None.

        """
        
        self.initModel(self.clearOld)
        self.buildNodes()   
        self.buildEulerBeams()
        self.buildPointLoads()
        self.buildEleLoads()   
        self.buildAnalysisPropreties()
        self.analyze()
        
        if recordOutput == True:
            self.recorder(self.beam) 