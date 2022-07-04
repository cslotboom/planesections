# PlaneSections
A lightweight beam bending library built on [OpenSeesPy](https://github.com/zhuminjie/OpenSeesPy).
The goal of PlaneSections is to make easy-to-use beam anayses, which can be used to quickly document structural calculations.
Being built on OpenSees, the structural results are reliable, and there is lots of room to build more complex models.

The core classes and API are complete, but development is still in progress. Expect some sytax changes before final release, however deprication warnings
will be given for breaking changes.

**NOTE:**
Units for force and length must be applied to the beam in a [consistent unit base for FEM](https://femci.gsfc.nasa.gov/units/index.html).
PlaneSections has been design with Metric units in mind in terms of scaling diagrams. For those using imperial units, results will work with a consitent unit basis, but the scale of the digrams may be off.

## Contents
* [Installation](https://github.com/cslotboom/planesections#Installation)
* [Documentation](https://github.com/cslotboom/planesections#Documentation)
* [Demo](https://github.com/cslotboom/planesections#Demo)
* [Work Status](https://github.com/cslotboom/planesections#Status)


## Installation
Package is installable through pip
```
pip install planesections
```

## Documentation
All major functions and classes are documented on read-the-docs: https://planesections.readthedocs.io/en/latest/

## Demo
The PlaneSections can plot representations that can be used in documentation.
It's also possible to get the output bening moment, shear force, rotation, and deflection diagrams.

``` Python

import planesections as ps

# Define node locations, and support conditions
L = 5
beam = ps.newEulerBeam2D(L)

# Define beam and fixities
pinned = [1,1,0]
beam.setFixity(L*0.1, pinned, label = '1')
beam.setFixity(L*0.9, pinned)

# Define loads
Pz = -1
beam.addVerticalLoad(0, Pz, label = 'A')
beam.addVerticalLoad(L*0.5, 2*Pz, label = 'B')
beam.addVerticalLoad(L, Pz, label = 'C')
beam.addDistLoadVertical(0, L, Pz)
beam.addDistLoadVertical(1, L*0.3, 5*Pz)

# Plot the beam diagram
ps.plotBeamDiagram(beam)

# Run the analysis
analysis = ps.OpenSeesAnalyzer2D(beam)
analysis.runAnalysis()

# Plot the SFD and BMD
ps.plotShear2D(beam)
ps.plotMoment2D(beam)
```

<p align="center">
  <img src="doc/img/Beam-Image-2.png" width="500">
</p>
<p align="center">
  <img src="doc/img/Beam-Image-2-SFD.png" width="500">
</p>  
<p align="center">
  <img src="doc/img/Beam-Image-2-BMD.png" width="500">
</p>  

## Further Examples
See the examples folder for


## Status
Before the first beta release, the following will be completed.

*Analysis and API*:
- [x] fancy plots (distributed Load)
- [x] Better deflection plots (distributed Load)

*Infacstructure*:
- [x] pip package
  - [x] setup on pypi: complete, package is installable with "pip install planesections"
  - [x] Add requirements
- [x] Document code
  - [x] Finish all class docstrings.
  - [x] Add Sphinx docs.
  - [x] Add read the docs website.
- [ ] Examples
  - [ ] Finish landing page with code examples and figures.
  - [ ] Compare simple cases with analytic equations.
  - [ ] Compare complex cases with sap/rfem/etc.


# Post 1.0 release
*Analysis and API*:
- [ ] plot labels



Future work:
 - 3D beams
 - Timoshenko beams
 - Nonlinear beams analysis
 - One-way Slabs?
 - Two-way Slabs?
 - Orthtropic Slabs?
 - Basic simple frame analysis?
 - Basic Nonlinear frame analysis?

