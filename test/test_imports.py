# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian

Tests if the import structure still works, assuming that people are importing
functions directly.
In the future this structure may change, so this help confirm these functions
are working.
"""





def test_builder():
    from planesections.builder import (Section2D, SectionBasic2D, SectionRectangle,
                          Node2D, Beam2D, newEulerBeam2D, EulerBeam2D, EleLoad, PointLoad)
    assert True
        


def test_diagram():
    from planesections.diagram import plotBeamDiagram, BeamPlotter2D
    assert True
    
def test_Analysis():
    from planesections.analysis import (OutputRecorder2D, OpenSeesAnalyzer2D)
    assert True
    
# test_builder()
# test_Analysis()
# test_diagram()
