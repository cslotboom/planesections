# -*- coding: utf-8 -*-
"""

@author: Christian


Tests if nodes are assigned fixities properly
"""

from planesections import  FixityTypes2D, Node2D
from planesections.builder import  _convertFixityInput2D


fixed = FixityTypes2D.getFixed()
free = FixityTypes2D.getFree()

fixedNode   = Node2D(0, fixed)
freeNode    = Node2D(0, free)

def hasReaction():
    assert fixedNode.hasReaction == True
    assert freeNode.hasReaction == False



if __name__ == '__main__':
    hasReaction()
    # test_fixityHasSameObjects()
    # test_fixity_stringCorrect()
    # test_fixity_stringFail()
    # test_fixity_listCorrect()
    # test_fixity_listFail()
    # test_fixity_inporperObject()
    