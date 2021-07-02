# planesections
A lightweight beam bending library built on [OpenSeesPy](https://github.com/zhuminjie/OpenSeesPy).
There was no package for beam bending in python that worked to my satisfaction, hence this package.
Being built on OpenSees, the structural results are reliable, and there is lots of room to build more complex models.
While OpenSees can analyze nearly anything, the emphasis is on providing a quick way to analyze beams.

Expect sytax changes before final release, use with caution.

Currently a work in progress. To be compeleted before intial release:
- [x] pip package
  -  complete, can install with "pip install planesections"
- [ ] Document code
  - [ ] Finish all class docstrings.
  - [ ] Add Sphinx docs.
  - [ ] Add read the docs website.
- [ ] Examples
  - [ ] Finish landing page with code examples and figures.
  - [ ] Compare simple cases with analytic equations.
  - [ ] Compare complex cases with sap/rfem/etc.

Future work:
 - Timoshenko beams
 - Nonlinear beams analysis
 - One-way Slabs?
 - Two-way Slabs?
 - Orthtropic Slabs?
 - Basic simple frame analysis?
 - Basic Nonlinear frame analysis?


