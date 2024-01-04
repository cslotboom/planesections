# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian

Tests if the import structure still works, assuming that people are importing
functions directly.
In the future this structure may change, so this help confirm these functions
are working.
"""


def test_section():
    from planesections import Section, SectionBasic, SectionRectangle
    
    assert True

def test_builder():
    from planesections import (
                          Node2D, Beam, newEulerBeam, EulerBeam, EleLoad, PointLoad)
    assert True
            
def test_diagram():
    from planesections import plotBeamDiagram, BeamPlotter2D
    assert True

def _OpenseesInstalled():
    try:
        import openseespy.opensees as op
    except:
        return False
    return True

def test_Analysis():
    if _OpenseesInstalled():
        from planesections import (OutputRecorder, OpenSeesAnalyzer2D)
        
    assert True
