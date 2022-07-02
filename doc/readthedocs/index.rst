.. Hysteresis documentation master file, created by
   sphinx-quickstart on Thu Dec 31 18:57:31 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PlaneSections Documentation
======================================
PlaneSections is a lightweight beam bending library built on [OpenSeesPy](https://github.com/zhuminjie/OpenSeesPy).
The goal of PlaneSections is to quickly run beam anayses, and create outputs to document structural calculations.

The following website documents all classes and functions the user can access in PlaneSections.
The core of the program is the beam class in the builder module. This classes will encapuslate all of the contains all information for loading serve as interfaces for class is the beam, 
and the user interacts with this class to run their analysis.

The Builder module is used to create the beam and 
The Analysis module is used to analyze the beam using OpenSeesPy and document the results.
The Diagram module is used to plot representations of the beam.
The Postprocess module is used to plot outputs of the analysis, including force diagrams and deflections

Note that the core classes and API are complete, but development is still in progress. Expect some sytax changes before final release, however deprication warnings
will be given for breaking changes.

Install using:


