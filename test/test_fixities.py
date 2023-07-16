# -*- coding: utf-8 -*-
R"""
Created on Sun May 23 01:00:41 2021

@author: Christian
"""

from planesections import  FixityTypes2D
from planesections.builder import  _convertFixityInput2D

def test_fixityHasSameObjects():
    f1 = FixityTypes2D.getFixed()
    f2 = FixityTypes2D.getFixed()
    assert f1 is f2

def test_fixity_stringCorrect():
    
    pinned = _convertFixityInput2D('pinned')
    assert pinned.fixityValues == [1,1,0]
    assert pinned.name == 'pinned'


def test_fixity_stringFail():
    try:
        _convertFixityInput2D('test')
        assert False
    except:
        assert True


def test_fixity_listCorrect():
    
    pinned = _convertFixityInput2D([1,1,1])
    assert pinned.fixityValues == [1,1,1]
    assert pinned.name == 'fixed'


def test_fixity_listFail():
    try:
        _convertFixityInput2D([0,0,1])
        assert False
    except:
        assert True


def test_fixity_inporperObject():
    try:
        _convertFixityInput2D((0))
        assert False
    except:
        assert True



if __name__ == '__main__':
    test_fixityHasSameObjects()
    test_fixity_stringCorrect()
    test_fixity_stringFail()
    test_fixity_listCorrect()
    test_fixity_listFail()
    test_fixity_inporperObject()
    