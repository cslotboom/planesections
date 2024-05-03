import numpy as np
from .parse import _getForceValues

def _get_discontinuity_inds(force, tol = 10e-6):
    
    force2D = force.reshape(-1,2)
    indDisTmp = np.where(tol < np.abs(np.diff(force2D)))[0]
    indDisTmp   = np.concatenate((indDisTmp*2, indDisTmp*2 + 1))
    # indDis      = indDisTmp[1:-1]
    return indDisTmp

def _valsInPercentTol(y1, y2, tolPercent = 10e-4):
    if abs((y1/y2) - 1) < tolPercent:
        return True
    return False

def valRelativelyNearZero(val, referenceMax, tolPercent = 10e-9):
    """
    Remove The final point if it is close to zero.
    We do some gymnastics here because we don't know the scale of the plot.
    """
    return (abs(val / referenceMax) < tolPercent)
    
   
    
def _getLabelInds(xcoords:list, force:list, labels:list):
    nonNoneLabels   = np.array(labels) != None
    nonEmptyLabels  = np.array(labels) != ''

    indLabelTmp = np.where(nonNoneLabels*nonEmptyLabels)[0]
    
    indLabelTmp = indLabelTmp*2
    indLabelTmp = np.array([indLabelTmp, indLabelTmp + 1]).T

    # If the label index is at a discontinous point, get both sides of the point.
    indLabel = []
    tol = 10e-6
    for ind1, ind2 in indLabelTmp:
        xcoordEqual     = (xcoords[ind1] == xcoords[ind2])
        ycoordUnequal   = tol < abs(force[ind1]/force[ind2] - 1) 
        if xcoordEqual and ycoordUnequal:
            indLabel += [ind1, ind2]
        else:
            indLabel.append(ind1)
    return indLabel
   
    
def _getLabelIndsDisp(xcoords:list, force:list, labels:list):
    nonNoneLabels   = np.array(labels) != None
    nonEmptyLabels  = np.array(labels) != ''

    indLabelTmp = np.where(nonNoneLabels*nonEmptyLabels)[0]
    indLabel = np.array(indLabelTmp,dtype =int)

    return indLabel

def _processPOIDictInputs(poiOptions):
    
    if 'showLabels' not in poiOptions:
        poiOptions['showLabels'] = True
    
    if 'showDiscontinutiy' not in poiOptions:
        poiOptions['showDiscontinutiy'] = True        
    
    if 'showMax' not in poiOptions:
        poiOptions['showMax'] = True
 

    return poiOptions



def _getPOIIndsForce(xcoords, ycoords, labels, ycordsSecondary, poiOptions):

    # Get Label Inds
    indLabel = []
    if poiOptions['showLabels'] == True:
        indLabel = _getLabelInds(xcoords, ycoords, labels)

    # Get Discontinuity Indicies
    indDis = []
    if poiOptions['showDiscontinutiy'] == True:
        indDis   = _get_discontinuity_inds(ycoords)
    
    # If it's a moment plot, catch points of shear discontinuty.
    indDisShear = []
    if ycordsSecondary is not None:
        indDisShear   = _get_discontinuity_inds(ycordsSecondary)

    # Get Max/min Indicies
    maxMinInds = []
    if poiOptions['showMax'] == True:
        indMax  = np.argmax(ycoords)
        indMin  = np.argmin(ycoords)
        maxMinInds = [indMax, indMin]

    return np.concatenate((indDis, indDisShear,  np.array(indLabel, dtype=int), maxMinInds))



def _getPOIIndsDisp(xcoords, ycoords, labels, ycordsSecondary, poiOptions):

    # Get Label Inds
    indLabel = []
    if poiOptions['showLabels'] == True:
        indLabel = _getLabelIndsDisp(xcoords, ycoords, labels)

    # Get Max/min Indicies
    maxMinInds = []
    if poiOptions['showMax'] == True:
        indMax  = np.argmax(ycoords)
        indMin  = np.argmin(ycoords)
        maxMinInds = [indMax, indMin]

    return np.concatenate((np.array(indLabel, dtype=int), maxMinInds))



def findBeamForcePOI(beam, index, POIOptions):
    """
    Gets the Force indicies of all the points of interest for the input beam.

    Parameters
    ----------
    beam : ndarray
        The input beam.
    index : int
        The type of response to plot, can have value 
        
        In 2D has values:
            [0:Fx, 1: Fy, 2: M]
            
        In 3D has values:
            [0:Fx, 1: Fy, 2: Fz, 3: Mx, 4: Mx, 5: Mz]
            

    POIOptions : dict, optional
        The options to use for the POI labels. There are several flags that 
        have values true or false which can be used to turn on or off certain
        points of interst. Notably:
            
            showLabels: this flag turns on or off 
            
            showDiscontinutiy: this flag turns on labeling points of discontinuity
            
            showMax: this turns on or off
        
        The default is None, which sets all flags to true

    Returns
    -------
    poiInd : list[int]
        The list of indexes for each point of interest.

    """    
    
    xcoords, force, labels = _getForceValues(beam, index)
    shear = None
    if index ==2:
        _, shear, _ = _getForceValues(beam, index)
    
    candidatePOI    = findAllPOI(xcoords, force, labels, shear, POIOptions)
    return removeFalsePOI(candidatePOI, force)



def findAllPOI(xcoords, ycoords, labels, ysecondary=None, POIOptions:dict = None):
    """
    Gets the indicies of all the points of interest for the input beam.

    Parameters
    ----------
    xcoords : ndarray
        The input x coordinant array.
    ycoords : ndarray
        The input y coordinant array.
    labels : list
        The input list of labels for each node.
    ysecondary : TYPE, optional
        A secondary array that can be used to find discontinous points. 
        The default is None.
    POIOptions : dict, optional
        The options to use for the POI labels. There are several flags that 
        have values true or false which can be used to turn on or off certain
        points of interst. Notably:
            showLabels: this flag turns on or off 
            showDiscontinutiy: this flag turns on labeling points of discontinuity
            showMax: this turns on or off
        
        The default is None, which sets all flags to true

    Returns
    -------
    poiInd : list[int]
        The list of indexes for each point of interest.

    """
    
    # Prevent the options from having no value.
    if POIOptions == None:
        POIOptions = {}
        
    # add default values if they aren't included
    POIOptions = _processPOIDictInputs(POIOptions)
    
    # Check if the 
    if len(ycoords) == len(labels):
        union = _getPOIIndsDisp(xcoords, ycoords, labels, ysecondary, POIOptions)
    else:
        union = _getPOIIndsForce(xcoords, ycoords, labels, ysecondary, POIOptions)
    
    poiInd  = list(union)
    poiInd  = [int(ind) for ind in poiInd]
    return poiInd

# =============================================================================
# 
# =============================================================================


def _findCloseDiscontinousPoints(force, ind, poiInd):
    """
    This will remove discontinous points picked up in the shear force diagram.
    
    We only filter out the left most point, otherwise we would end up filtering
    both points out.
    
    """
    # Combine discontinuous points that are within a tolerance of eachother
    leftAdjecentPointExists = False
    for indOther in poiInd:
        if (indOther - 1 == ind ):
            leftAdjecentPointExists = True
            break
    
    # don't add the point if it is next to another point and close in value
    if leftAdjecentPointExists and _valsInPercentTol(force[ind], force[indOther]):
        return True
    else:
        return False

def removeFalsePOI(candidatePOI, force):
    """
    Do a final pruning of points


    Parameters
    ----------
    beam : TYPE
        DESCRIPTION.
    forceInd : TYPE
        DESCRIPTION.
    candidatePOI : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    # get the forces again
    absMax = np.max(np.abs(force))

    # removeThe end points
    end = len(force) - 1
    start = 0
    if end in candidatePOI:
        candidatePOI.remove(end)
    if start in candidatePOI:
        candidatePOI.remove(start)
    
    # make a list of the second from last points. 
    # If these are close to zero we will remove them later.
    candidateEndPoints = [1, len(force) - 2]
    
    filteredPoiInd = []
    poiInd = [int(ind) for ind in candidatePOI]
    for ind in poiInd:
        ind = int(ind)
    
        if _findCloseDiscontinousPoints(force, ind, poiInd):
            continue
    
        # Values 
        if ind in candidateEndPoints and valRelativelyNearZero(force[ind], absMax):
            continue
        
        filteredPoiInd.append(ind)
    filteredPoiInd = set(filteredPoiInd)
    return filteredPoiInd



# =============================================================================
# 
# =============================================================================
