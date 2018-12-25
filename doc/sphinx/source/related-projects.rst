.. include:: abbreviation.txt

.. _related-projects-page:

==================
 Related Projects
==================

G-code Tools
------------

* `pygcode <https://github.com/fragmuffin/pygcode>`_ — G-code parser for Python

CAM / Computer Aided Manufacturing
----------------------------------

* `PyCAM <http://pycam.sourceforge.net>`_ is a toolpath generator for 3-axis CNC machining. It loads
  3D models in STL format or 2D contour models from DXF or SVG files. The resulting G-Code can be
  used with LinuxCNC or any other machine controller.

* `simple-gcode-generators <https://github.com/LinuxCNC/simple-gcode-generators>`_ — Simple LinuxCNC
  G-Code Generators written in Python

  This repository contains a collection of Python scrips that generate simple G-Code for LinuxCNC. 

CNC / Control Machine
---------------------

* |MachineKit|_ — platform for machine control applications (LinuxCNC fork)

  Machinekit is portable across a wide range of hardware platforms and real-time environments, and
  delivers excellent performance at low cost. It is based on the HAL component architecture, an
  intuitive and easy to use circuit model that includes over 150 building blocks for digital logic,
  motion, control loops, signal processing, and hardware drivers. Machinekit supports local and
  networked UI options, including ubiquitous platforms like phones or tablets.

* |LinuxCNC|_ — platform for machine control applications

  Forked by Machinekit, LinuxCNC was formerly called Enhanced Machine Controller or EMC2, a software
  project developed by |NIST|_.

* `PyCNC <https://github.com/Nikolay-Kha/PyCNC>`_ — Python CNC machine controller for Raspberry Pi and other ARM Linux boards

  PyCNC is a free open-source high-performance G-code interpreter and CNC/3D-printer controller. It
  can run on a variety of Linux-powered ARM-based boards, such as Raspberry Pi, Odroid, Beaglebone
  and others. This gives you a flexibility to pick a board you are most familiar with, and use
  everything Linux has to offer, while keeping all your G-code runtime on the same board without a
  need to have a separate microcontroller for real-time operation. Our choice of Python as main
  programming language significantly reduces code base compared to C/C++ projects, reduces
  boilerplate and microcontroller-specific code, and makes the project accessible to a broader
  audience to tinker with.
