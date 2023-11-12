# -*- coding: utf-8 -*-
"""

@author: Christian

Tests if teh post-processor functions are correctly returning values.
"""


import planesections as ps
import numpy as np
import hysteresis as hys
import textalloc as ta

x1 = 0
x2 = 1
offset = x2/20

x      = np.linspace(0, x2, 80)
fixed  = np.array([1, 1, 0])
roller = np.array([0, 1, 0])

P = np.array([0., 1000.,0.])
q = np.array([0.,-1000.])

beam = ps.EulerBeam2D(x)
beam.setFixity(x1, fixed)
beam.setFixity(x2, fixed)
beam.setFixity(x2/3, roller)

beam.addVerticalLoad(offset, -1000.)
beam.addVerticalLoad(x2/2, -1000.)
beam.addVerticalLoad(x2 - offset, -1000.)
beam.addDistLoad(0,x2,q) 
# beam.addLabel(0, label='A') 
# beam.addLabel(x2, label='B') 

analysis = ps.OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()


xcoords, force, labels = ps.postprocess.plot._getForceValues(beam, 1)

# Get Label Inds
indLabelTmp = np.where((np.array(labels) != None)*(np.array(labels) != ''))[0]
indLabelTmp = indLabelTmp*2
indLabelTmp = np.array([indLabelTmp, indLabelTmp + 1]).T

# If the label index is discontinous, get both points.
indLabel = []
for ind1, ind2 in indLabelTmp:
    if (xcoords[ind1] == xcoords[ind2]):
        indLabel += [ind1, ind2]
    else:
        indLabel.append(ind1)
# Get Discontinuity Indicies
tol = 10e-6
force2D = force.reshape(-1,2)
indDisTmp = np.where(tol < np.abs(np.diff(force2D)))[0]
indDisTmp   = np.concatenate((indDisTmp*2, indDisTmp*2 + 1))
indDis      = indDisTmp[1:-1]

# Get Max/min Indicies
indMax  = np.argmax(force)
indMin  = np.argmin(force)

# Find Union of all points
union = np.concatenate((indDis, np.array(indLabel, dtype=int), [indMax, indMin]))
pointsOfInterestInd = set(union)

print(pointsOfInterestInd)


    

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
plt.plot(xcoords, force)



xmin, xmax = ax.get_xlim()
dx = xmax - xmin
ymin, ymax = ax.get_ylim()
dy = ymax - ymin

labelX = []
labelY = []
labelText = []
for ind in pointsOfInterestInd:
    x0 = xcoords[ind]
    y0 = force[ind]
    xlabel = x0 + dx*0.015
    ylabel = y0 - dy*0.015 * 4
    xcoord = 'a'
    xOut = round(x0,2)
    yOut = round(y0,1)
    textX = f'x = {xOut}\n'
    textY = f'y = {yOut}'
    text = textX + textY
    labelX.append(x0)
    labelY.append(y0)
    labelText.append(text)
    # ax.text(xlabel, ylabel, text, fontsize=6)


ta.allocate_text(fig, ax, labelX, labelY, labelText,textsize=6,x_scatter=labelX, y_scatter=labelY)

pointsOfInterestInd = np.array(list((pointsOfInterestInd)))
# plt.plot(xcoords[pointsOfInterestInd], force[pointsOfInterestInd], marker='x', linewidth=0)

class PlotPointOfInterest:
    
    pointTypes  = ['label', 'globalMax', 'discontinuity']
    def __init__(self, ind, offsets):
        self.ind = ind
        self.labelOffsets = []
        
    def plot():
        pass



class POIFactory():
    
    def __init__(self, xcoords, ycoords, setLabels= True, setMax=True, 
                 setDiscontinuity = True):
        self.set_offsets(xcoords, ycoords)
        
    def _set_offsets(self, x, y):
        pass

    def setPOI(self):
        
        pass
        

class POILabel(PlotPointOfInterest):
    
    def __init__(self, ind, offsets):
        pass


class POIMax(PlotPointOfInterest):
    
    def __init__(self, ind, offsets):
        pass
    

class POIDiscontinuity(PlotPointOfInterest):
    pass
    

