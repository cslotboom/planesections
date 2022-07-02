# PlaneSections
A lightweight beam bending library built on [OpenSeesPy](https://github.com/zhuminjie/OpenSeesPy).
There was no package for beam bending in python that worked to my satisfaction, hence this package.
Being built on OpenSees, the structural results are reliable, and there is lots of room to build more complex models.
While OpenSees can analyze nearly anything, the emphasis is on providing a quick way to analyze beams.

The core classes and API are complete, but development is still in progress. Expect some sytax changes before final release.

## Installation
Package is installable through pip
```
pip install planesections
```

## Documentation
All major functions and classes are documenteted on read-the-docs: https://planesections.readthedocs.io/en/latest/

## Simple API
Easily make changes with the beam object


## Beam Diagrams and Result Plots
The PlaneSections can plot representations that can be used in documentation.
It's also possible to get the output bening moment, shear force, rotation, and deflection diagrams.

**Future code example**

<p align="center">
  <img src="doc/img/Beam Image 2.png">
  <img src="doc/img/Beam Image 2 SFD.png">
  <img src="doc/img/Beam Image 2 BMD.png">
</p>

## 1.0 Work Status
Currently a work in progress. To be compeleted before intial release:

*Analysis and API*:
- [x] fancy plots (distributed Load)
- [x] Better deflection plots (distributed Load)

*Infacstructure*:
- [x] pip package
  - [x] setup on pypi: complete, package is installable with "pip install planesections"
  - [ ] Add requirements
- [ ] Document code
  - [ ] Finish all class docstrings.
  - [ ] Add Sphinx docs.
  - [ ] Add read the docs website.
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

