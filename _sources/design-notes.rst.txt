.. include:: abbreviation.txt

.. _design-note-page:

==============
 Design Notes
==============

G-Code Parser
=============

The RS-274 parser is generated automatically from the grammar defined in the paper |NIST-RS-274|_
(Appendix E) using the generator `PLY <https://www.dabeaz.com/ply/ply.html>`_ which implement a
LALR(1) parser similar to the tools **lex** and **yacc**.

The parser construct an `abstract syntax tree (AST)
<https://en.wikipedia.org/wiki/Abstract_syntax_tree>`_ during the parsing.

User can subclass this parser to support a derived G-code flavour.

G-code flavours
===============

The different flavours are partly handled in |YAML|_ files.


G-code Generation and Simulation
================================

Computational Geometry Engine
=============================

The computational geometry engine requires these features :

* import standard 2D object file, e.g. SVG and DXF
* import standard 3D object file, e.g. STL
* 2D path erosion and dilation, e.g. to compute cutter radius compensation
* 2D/3D Minkowski sum along a path
* 3D extrusion
* 3D Boolean operation : object - tool path

List of the Main Open Source Computational Geometry Algorithms Libraries
------------------------------------------------------------------------

The Computational Geometry Algorithms Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`CGAL <https://www.cgal.org>`_ is a software project that provides easy access to efficient and
reliable geometric algorithms in the form of a C++ library. CGAL is used in various areas needing
geometric computation, such as geographic information systems, computer aided design, molecular
biology, medical imaging, computer graphics, and robotics.

CGAL is used in:

* many academic projects
* `OpenSCAD <http://www.openscad.org>`_

Git repository and Python binding:

* https://github.com/CGAL/cgal
* https://github.com/CGAL/cgal-swig-bindings
* https://github.com/sciencectn/cgal-bindings

STL (STereoLithography) format support:

* https://en.wikipedia.org/wiki/STL_(file_format)
* https://doc.cgal.org/latest/Polyhedron/classCGAL_1_1Polyhedron__incremental__builder__3.html

  * include/CGAL/IO/Polyhedron_builder_from_STL.h

* https://github.com/CGAL/cgal/blob/master/Polyhedron/demo/Polyhedron/Plugins/IO/STL_io_plugin.cpp

  * demo/Polyhedron/Plugins/IO/STL_io_plugin.cpp

* https://github.com/CGAL/cgal/blob/master/Polyhedron_IO/include/CGAL/IO/STL_reader.h

  * include/CGAL/IO/STL_reader.h
  * include/CGAL/IO/STL_writer.h

Open CASCADE
~~~~~~~~~~~~

* https://www.opencascade.com
* `Open CASCADE Community Edition <https://github.com/tpaviot/oce>`_
* https://github.com/tpaviot/pythonocc-core — python wrapper

Open CASCADE is used in:

* `Salome <http://www.salome-platform.org>`_
* `FreeCAD <https://freecadweb.org>`_
.. `code_aster <https://www.code-aster.org>`_


G-code Visualisation
====================

The open source `Qt <https://www.qt.io>`_ framework provide a multi-platform User Interface framework with 3D support.

* `Qt 3D <https://doc.qt.io/qt-5/qt3d-index.html>`_

  Qt 3D provides functionality for near-realtime simulation systems with support for 2D and 3D rendering in both Qt C++ and Qt Quick applications.

* `QMesh Class <https://doc.qt.io/qt-5/qt3drender-qmesh.html>`_

  QMesh supports the following formats:

  * Wavefront OBJ
  * Stanford Triangle Format PLY
  * STL (STereoLithography)
  * Autodesk FBX if the SDK is installed
