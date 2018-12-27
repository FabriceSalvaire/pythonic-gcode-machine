CNC Machine Overview
====================

This section gives a brief description of how a CNC machine is viewed from the input and output ends
of the Interpreter.

Mechanical Components
---------------------

A CNC machine has many mechanical components that may be controlled or may affect the way in which
control is exercised. This section describes the subset of those components that interact with the
Interpreter.  Mechanical components that do not interact directly with the Interpreter, such as the
jog buttons, are not described here, even if they affect control.

Axes
~~~~

Any CNC machine has one or more Axes. Different types of CNC machines have different
combinations. For instance, a '4-axis milling machine' may have XYZA or XYZB axes. A lathe typically
has XZ axes. A foam-cutting machine may have XYUV axes. In LinuxCNC, the case of a XYYZ 'gantry'
machine with two motors for one axis is better handled by kinematics rather than by a second linear
axis.  ^([`1 <#_footnote_1>`__])

Primary Linear Axes

The X, Y, and Z axes produce linear motion in three mutually orthogonal directions.

Secondary Linear Axes

The U, V, and W axes produce linear motion in three mutually orthogonal directions. Typically, X and
U are parallel, Y and V are parallel, and Z and W are parallel.

Rotational Axes

The A, B and C axes produce angular motion (rotation). Typically, A rotates around a line parallel
to X, B rotates around a line parallel to Y, and C rotates around a line parallel to Z.

Spindle
~~~~~~~

A CNC machine typically has a spindle which holds one cutting tool, probe, or the material in the
case of a lathe. The spindle may or may not be controlled by the CNC software. LinuxCNC offers
suport for up to 8 spindles, which can be individually controlled and can run simultaneously at
different speeds and in different directions.

Coolant
~~~~~~~

If a CNC machine has components to provide mist coolant and/or flood coolant they can be controlled
by G codes.

Feed and Speed Override
~~~~~~~~~~~~~~~~~~~~~~~

A CNC machine can have separate feed and speed override controls, which let the operator specify
that the actual feed rate or spindle speed used in machining at some percentage of the programmed
rate.

Block Delete Switch
~~~~~~~~~~~~~~~~~~~

A CNC machine can have a block delete switch. See the `Block Delete <#sub:block-delete-switch>`__
Section.

Optional Program Stop Switch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A CNC machine can have an optional program stop switch. See the `Optional Program Stop
<#sub:optional-program-stop>`__ Section.

Control and Data Components
---------------------------

Linear Axes
~~~~~~~~~~~

The X, Y, and Z axes form a standard right-handed coordinate system of orthogonal linear
axes. Positions of the three linear motion mechanisms are expressed using coordinates on these axes.

The U, V and W axes also form a standard right-handed coordinate system.  X and U are parallel, Y
and V are parallel, and Z and W are parallel (when A, B, and C are rotated to zero).

Rotational Axes
~~~~~~~~~~~~~~~

The rotational axes are measured in degrees as wrapped linear axes in which the direction of
positive rotation is counterclockwise when viewed from the positive end of the corresponding X, Y,
or Z-axis. By 'wrapped linear axis', we mean one on which the angular position increases without
limit (goes towards plus infinity) as the axis turns counterclockwise and deceases without limit
(goes towards minus infinity) as the axis turns clockwise. Wrapped linear axes are used regardless
of whether or not there is a mechanical limit on rotation.

Clockwise or counterclockwise is from the point of view of the workpiece. If the workpiece is
fastened to a turntable which turns on a rotational axis, a counterclockwise turn from the point of
view of the workpiece is accomplished by turning the turntable in a direction that (for most common
machine configurations) looks clockwise from the point of view of someone standing next to the
machine.  ^([`2 <#_footnote_2>`__])

Controlled Point
~~~~~~~~~~~~~~~~

The controlled point is the point whose position and rate of motion are controlled. When the tool
length offset is zero (the default value), this is a point on the spindle axis (often called the
gauge point) that is some fixed distance beyond the end of the spindle, usually near the end of a
tool holder that fits into the spindle. The location of the controlled point can be moved out along
the spindle axis by specifying some positive amount for the tool length offset. This amount is
normally the length of the cutting tool in use, so that the controlled point is at the end of the
cutting tool. On a lathe, tool length offsets can be specified for X and Z axes, and the controlled
point is either at the tool tip or slightly outside it (where the perpendicular, axis-aligned lines
touched by the 'front' and 'side' of the tool intersect).

Coordinated Linear Motion
~~~~~~~~~~~~~~~~~~~~~~~~~

To drive a tool along a specified path, a machining center must often coordinate the motion of
several axes. We use the term 'coordinated linear motion' to describe the situation in which,
nominally, each axis moves at constant speed and all axes move from their starting positions to
their end positions at the same time. If only the X, Y, and Z axes (or any one or two of them) move,
this produces motion in a straight line, hence the word 'linear' in the term. In actual motions, it
is often not possible to maintain constant speed because acceleration or deceleration is required at
the beginning and/or end of the motion. It is feasible, however, to control the axes so that, at all
times, each axis has completed the same fraction of its required motion as the other axes. This
moves the tool along same path, and we also call this kind of motion coordinated linear motion.

Coordinated linear motion can be performed either at the prevailing feed rate, or at traverse rate,
or it may be synchronized to the spindle rotation. If physical limits on axis speed make the desired
rate unobtainable, all axes are slowed to maintain the desired path.

Feed Rate
~~~~~~~~~

The rate at which the controlled point moves is nominally a steady rate which may be set by the
user. In the Interpreter, the feed rate is interpreted as follows (unless 'inverse time feed' or
'feed per revolution' modes are being used, in which case see Section `G93-G94-G95-Mode,G93 G94 G95
<#gcode:g93-g94-g95>`__).

#. If any of XYZ are moving, F is in units per minute in the XYZ cartesian system, and all other
   axes (ABCUVW) move so as to start and stop in coordinated fashion.

#. Otherwise, if any of UVW are moving, F is in units per minute in the UVW cartesian system, and
   all other axes (ABC) move so as to start and stop in coordinated fashion.

#. Otherwise, the move is pure rotary motion and the F word is in rotary units in the ABC
   'pseudo-cartesian' system.

.. _coolant-1:

Coolant
~~~~~~~

Flood coolant and mist coolant may each be turned on independently. The RS274/NGC language turns
them off together see Section `M7 M8 M9 <#mcode:m7-m8-m9>`__.

Dwell
~~~~~

A machining center may be commanded to dwell (i.e., keep all axes unmoving) for a specific amount of
time. The most common use of dwell is to break and clear chips, so the spindle is usually turning
during a dwell. Regardless of the Path Control Mode (see Section `Path Control
<#sec:path-control-mode>`__) the machine will stop exactly at the end of the previous programmed
move, as though it was in exact path mode.

Units
~~~~~

Units used for distances along the X, Y, and Z axes may be measured in millimeters or inches. Units
for all other quantities involved in machine control cannot be changed. Different quantities use
different specific units. Spindle speed is measured in revolutions per minute. The positions of
rotational axes are measured in degrees. Feed rates are expressed in current length units per
minute, or degrees per minute, or length units per spindle revolution, as described in Section `G93
G94 G95 <#gcode:g93-g94-g95>`__.

Current Position
~~~~~~~~~~~~~~~~

The controlled point is always at some location called the 'current position', and the controller
always knows where that is. The numbers representing the current position must be adjusted in the
absence of any axis motion if any of several events take place:

#. Length units are changed.
#. Tool length offset is changed.
#. Coordinate system offsets are changed.

Selected Plane
~~~~~~~~~~~~~~

There is always a 'selected plane', which must be the XY-plane, the
YZ-plane, or the XZ-plane of the machining center. The Z-axis is, of
course, perpendicular to the XY-plane, the X-axis to the YZ-plane, and
the Y-axis to the XZ-plane.

Tool Carousel
~~~~~~~~~~~~~

Zero or one tool is assigned to each slot in the tool carousel.

Tool Change
~~~~~~~~~~~

A machining center may be commanded to change tools.

Pallet Shuttle
~~~~~~~~~~~~~~

The two pallets may be exchanged by command.

Path Control Mode
~~~~~~~~~~~~~~~~~

The machining center may be put into any one of three path control modes: (1) exact stop mode, (2)
exact path mode, or (3) continuous mode with optional tolerance. In exact stop mode, the machine
stops briefly at the end of each programmed move. In exact path mode, the machine follows the
programmed path as exactly as possible, slowing or stopping if necessary at sharp corners of the
path. In continuous mode, sharp corners of the path may be rounded slightly so that the feed rate
may be kept up (but by no more than the tolerance, if specified). See Sections `G61/G61.1
<#gcode:g61-g61.1>`__ and `G64 <#gcode:g64>`__.

Interpreter Interaction with Switches
-------------------------------------

The Interpreter interacts with several switches. This section describes
the interactions in more detail. In no case does the Interpreter know
what the setting of any of these switches is.

Feed and Speed Override Switches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Interpreter will interpret RS274/NGC commands which enable 'M48' or disable 'M49' the feed and
speed override switches. For certain moves, such as the traverse out of the end of a thread during a
threading cycle, the switches are disabled automatically.

LinuxCNC reacts to the speed and feed override settings when these switches are enabled.

See the `M48 M49 Override <#mcode:m48-m49>`__ section for more information.

.. _block-delete-switch-1:

Block Delete Switch
~~~~~~~~~~~~~~~~~~~

If the block delete switch is on, lines of G code which start with a slash (the block delete
character) are not interpreted. If the switch is off, such lines are interpreted. Normally the block
delete switch should be set before starting the NGC program.

.. _optional-program-stop-switch-1:

Optional Program Stop Switch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If this switch is on and an M1 code is encountered, program execution is paused.

Tool Table
----------

A tool table is required to use the Interpreter. The file tells which tools are in which tool
changer slots and what the size and type of each tool is. The name of the tool table is defined in
the ini file:

::

   [EMCIO]

   # tool table file
   TOOL_TABLE = tooltable.tbl

The default filename probably looks something like the above, but you may prefer to give your
machine its own tool table, using the same name as your ini file, but with a tbl extension:

::

   TOOL_TABLE = acme_300.tbl

or

::

   TOOL_TABLE = EMC-AXIS-SIM.tbl

For more information on the specifics of the tool table format, see the `Tool Table Format
<#sec:tool-table>`__ Section.

Parameters
----------

In the RS274/NGC language view, a machining center maintains an array of numerical parameters
defined by a system definition (RS274NGC_MAX_PARAMETERS). Many of them have specific uses especially
in defining coordinate systems. The number of numerical parameters can increase as development adds
support for new parameters. The parameter array persists over time, even if the machining center is
powered down.  LinuxCNC uses a parameter file to ensure persistence and gives the Interpreter the
responsibility for maintaining the file. The Interpreter reads the file when it starts up, and
writes the file when it exits.

All parameters are available for use in G code programs.

The format of a parameter file is shown in the following table. The file consists of any number of
header lines, followed by one blank line, followed by any number of lines of data. The Interpreter
skips over the header lines. It is important that there be exactly one blank line (with no spaces or
tabs, even) before the data. The header line shown in the following table describes the data
columns, so it is suggested (but not required) that that line always be included in the header.

The Interpreter reads only the first two columns of the table. The third column, 'Comment', is not
read by the Interpreter.

Each line of the file contains the index number of a parameter in the first column and the value to
which that parameter should be set in the second column. The value is represented as a
double-precision floating point number inside the Interpreter, but a decimal point is not required
in the file. All of the parameters shown in the following table are required parameters and must be
included in any parameter file, except that any parameter representing a rotational axis value for
an unused axis may be omitted. An error will be signaled if any required parameter is missing. A
parameter file may include any other parameter, as long as its number is in the range 1 to 5400. The
parameter numbers must be arranged in ascending order. An error will be signaled if not. Any
parameter included in the file read by the Interpreter will be included in the file it writes as it
exits. The original file is saved as a backup file when the new file is written. Comments are not
preserved when the file is written.

================ =============== ==========
Parameter Number Parameter Value Comment
================ =============== ==========
5161             0.0             G28 Home X
5162             0.0             G28 Home Y
================ =============== ==========

See the `Parameters <#gcode:parameters>`__ section for more information.

--------------

`1 <#_footnoteref_1>`__. If the motion of mechanical components is not independent, as with hexapod
machines, the RS274/NGC language and the canonical machining functions will still be usable, as long
as the lower levels of control know how to control the actual mechanisms to produce the same
relative motion of tool and workpiece as would be produced by independent axes. This is called
'kinematics'.

`2 <#_footnoteref_2>`__. If the parallelism requirement is violated, the system builder will have to
say how to distinguish clockwise from counterclockwise.
