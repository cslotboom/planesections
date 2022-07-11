# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian
Tests if the diagram unit environment is being loaded correctly.
"""

# import planesections as ps

from planesections.environment import diagramUnits

def test_print():
    """
    Sees if the environment prints
    """
    print(diagramUnits)
    diagramUnits.print()
    
    assert True

def test_setEnv():
    """
    Checks if a different environment gets set.
    """
    diagramUnits.setEnvironment('imperial_ftkip')
    print(diagramUnits.env)
    check1 = diagramUnits.env['distance'].unit == 'ft'
    check2 = diagramUnits.env['moment'].unit == 'kip-ft'
    
    assert check1 and check2
    
def test_read_custom_File():
    pass

def test_modify_single():
    """
    Sees if the units can be modified correctly.
    """
    modValue = {'unit':'kNcm', 'scale':100, 'Ndecimal' : 1}
    dictVal = 'distForce'
    diagramUnits.modifyEnvironment(dictVal, modValue)
    
    # print(ps.diagramUnits.env[dictVal])
    check1 = diagramUnits.env[dictVal].unit == 'kNcm'
    check2 = diagramUnits.env[dictVal].scale == 100
    check3 = diagramUnits.env[dictVal].Ndecimal == 1
    print(diagramUnits.env)
    assert check1 and check2 and check3

def test_modify_multiple():
    """
    Sees if the units can be modified correctly.
    """
    modValues = [{'unit':'cm', 'scale':100, 'Ndecimal' : 1}, 
                {'unit':'kNm', 'scale':1, 'Ndecimal' : 10}]
    dictVals = ['distance', 'distForce']
    diagramUnits.modifyEnvironment(dictVals, modValues)
    
    # print(ps.diagramUnits.env)
    check1 = diagramUnits.env[dictVals[0]].unit == 'cm'
    check2 = diagramUnits.env[dictVals[0]].scale == 100
    check3 = diagramUnits.env[dictVals[1]].Ndecimal == 10
    print(diagramUnits.env)
    assert check1 and check2 and check3
    
def test_modify_multiple2():
    """
    Sees if the units can be modified correctly.
    """
    modValues = [{'unit':'cm', 'scale':100, 'Ndecimal' : 1}, 
                {'unit':'kNm', 'scale':1, 'Ndecimal' : 10}]
    dictVals = ['distance', 'distForce']
    diagramUnits.modifyEnvironment(dictVals, modValues)
    
    # print(ps.diagramUnits.env)
    check1 = diagramUnits.env[dictVals[0]].unit == 'cm'
    check2 = diagramUnits.env[dictVals[0]].scale == 100
    check3 = diagramUnits.env[dictVals[1]].Ndecimal == 10
    # print(diagramUnits.env)
    # print(diagramUnits.env)
    assert check1 and check2 and check3

def test_resetEnv():
    """
    Checks if a different environment gets set.
    """
    diagramUnits.setEnvironment('imperial_ftkip')
    print(diagramUnits.env)
    check1 = diagramUnits.env['distance'].unit == 'ft'
    check2 = diagramUnits.env['distForce'].scale == 0.001
    
    assert check1 and check2
    


# test_print()
# test_setEnv()
# test_modify_single()
# test_modify_multiple()
# test_resetEnv()
# print(ps.diagramUnits)
# print(diagramUnits.env)
