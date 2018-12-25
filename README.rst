.. -*- Mode: rst -*-

.. -*- Mode: rst -*-

..
   |PythonicGcodeMachineUrl|
   |PythonicGcodeMachineHomePage|_
   |PythonicGcodeMachineDoc|_
   |PythonicGcodeMachine@github|_
   |PythonicGcodeMachine@readthedocs|_
   |PythonicGcodeMachine@readthedocs-badge|
   |PythonicGcodeMachine@pypi|_

.. |ohloh| image:: https://www.openhub.net/accounts/230426/widgets/account_tiny.gif
   :target: https://www.openhub.net/accounts/fabricesalvaire
   :alt: Fabrice Salvaire's Ohloh profile
   :height: 15px
   :width:  80px

.. |PythonicGcodeMachineUrl| replace:: https://github.com/FabriceSalvaire/pythonic-gcode-machine

.. |PythonicGcodeMachineHomePage| replace:: PythonicGcodeMachine Home Page
.. _PythonicGcodeMachineHomePage: https://github.com/FabriceSalvaire/pythonic-gcode-machine

.. |PythonicGcodeMachine@readthedocs-badge| image:: https://readthedocs.org/projects/PythonicGcodeMachine/badge/?version=latest
   :target: http://PythonicGcodeMachine.readthedocs.org/en/latest

.. |PythonicGcodeMachine@github| replace:: https://github.com/FabriceSalvaire/PythonicGcodeMachine
.. .. _PythonicGcodeMachine@github: https://github.com/FabriceSalvaire/PythonicGcodeMachine

.. |PythonicGcodeMachine@pypi| replace:: https://pypi.python.org/pypi/PythonicGcodeMachine
.. .. _PythonicGcodeMachine@pypi: https://pypi.python.org/pypi/PythonicGcodeMachine

.. |Build Status| image:: https://travis-ci.org/FabriceSalvaire/PythonicGcodeMachine.svg?branch=master
   :target: https://travis-ci.org/FabriceSalvaire/PythonicGcodeMachine
   :alt: PythonicGcodeMachine build status @travis-ci.org

.. |Pypi Version| image:: https://img.shields.io/pypi/v/PythonicGcodeMachine.svg
   :target: https://pypi.python.org/pypi/PythonicGcodeMachine
   :alt: PythonicGcodeMachine last version

.. |Pypi License| image:: https://img.shields.io/pypi/l/PythonicGcodeMachine.svg
   :target: https://pypi.python.org/pypi/PythonicGcodeMachine
   :alt: PythonicGcodeMachine license

.. |Pypi Python Version| image:: https://img.shields.io/pypi/pyversions/PythonicGcodeMachine.svg
   :target: https://pypi.python.org/pypi/PythonicGcodeMachine
   :alt: PythonicGcodeMachine python version

..  coverage test
..  https://img.shields.io/pypi/status/Django.svg
..  https://img.shields.io/github/stars/badges/shields.svg?style=social&label=Star
.. -*- Mode: rst -*-

.. |Python| replace:: Python
.. _Python: http://python.org

.. |PyPI| replace:: PyPI
.. _PyPI: https://pypi.python.org/pypi

.. |Numpy| replace:: Numpy
.. _Numpy: http://www.numpy.org

.. |IPython| replace:: IPython
.. _IPython: http://ipython.org

.. |Sphinx| replace:: Sphinx
.. _Sphinx: http://sphinx-doc.org

.. |NIST-RS-274| replace:: The NIST RS274NGC Interpreter — Version 3
.. _NIST-RS-274: https://www.nist.gov/publications/nist-rs274ngc-interpreter-version-3

.. |LinuxCNC| replace:: Linux CNC
.. _LinuxCNC: http://linuxcnc.org/docs/2.7/html/gcode/overview.html

.. |Machinekit| replace:: Machinekit
.. _Machinekit: http://www.machinekit.io

.. |YAML| replace:: YAML
.. _YAML: https://yaml.org

============================
 The Pythonic Gcode Machine
============================

|Pypi License|
|Pypi Python Version|

|Pypi Version|

* Quick Link to `Production Branch <https://github.com/FabriceSalvaire/PythonicGcodeMachine/tree/master>`_
* Quick Link to `Devel Branch <https://github.com/FabriceSalvaire/PythonicGcodeMachine/tree/devel>`_

Overview
========

What is PythonicGcodeMachine ?
------------------------------

.. free and open source

PythonicGcodeMachine is a Python toolkit to work with RS-274 / ISO G-Code.

.. -*- mode: rst -*-

PythonicGcodeMachine features:

* a compliant RS-274 / ISO G-code parser which is automatically generated from grammar and easy to
  derivate to support other flavours,
* an abstract syntax tree (AST) API,
* some G-code flavour aspects are handled by YAML files for maximum flexibility,
* tools to manipulate and validate G-code,
* and more ..

PythonicGcodeMachine supports these G-code flavours:

* RS-274 **(full support)**
* Fanuc *(partially)*
* Heidenhain *(partially)*
* LinuxCNC *(partially)*

Where is the Documentation ?
----------------------------

The documentation is available on the |PythonicGcodeMachineHomePage|_.

What are the main features ?
----------------------------

* to be completed

How to install it ?
-------------------

Look at the `installation <@project_url@/installation.html>`_ section in the documentation.

Credits
=======

Authors: `Fabrice Salvaire <http://fabrice-salvaire.fr>`_

News
====

.. -*- Mode: rst -*-


.. no title here

V0 2018-12-22
-------------

Started project
