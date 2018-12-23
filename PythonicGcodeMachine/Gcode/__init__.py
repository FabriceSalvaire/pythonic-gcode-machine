####################################################################################################
#
# PythonicGcodeMachine - @licence_header_description@
# Copyright (C) 2018 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

"""Module to implement the G-code language.

History
-------

The G-code language, also called RS-274, is a programming language for numerical control.  It was
developed by the EIA in the early 1960s, and finally standardised by ISO in February 1980 as RS274D
/ ISO 6983.

The G-code language has several flavours and historical versions. A list of reference documents
follows :

* The NIST RS274NGC Interpreter - Version 3, T. Kramer, F. Proctor, E. Messina, National Institute
  of Standards and Technology, NISTIR 6556, August 17, 2000
* The documentation of the `Linux CNC <http://linuxcnc.org>`_ project, formerly Enhanced Machine
  Controller developed at NIST,
* EIA Standard RS-274-D Interchangeable Variable Block Data Format for Positioning, Contouring, and
  Contouring/Positioning Numerically Controlled Machines, 2001 Eye Street, NW, Washington,
  D.C. 20006: Electronic Industries Association, February 1979

Overview
--------

The RS274/NGC language is based on lines of code. Each line (also called a “block”) may include
commands to a machining center to do several different things.

A typical line of code consists of an optional line number at the beginning followed by one or more
“words.” A word consists of a letter followed by a number (or something that evaluates to a
number). A word may either give a command or provide an argument to a command. For example,
:code:`G1 X3` is a valid line of code with two words. :code:`G1` is a command meaning “move in a
straight line at the programmed feed rate,” and :code:`X3` provides an argument value (the value of
X should be 3 at the end of the move). Most RS274/NGC commands start with either G or M (for
miscellaneous). The words for these commands are called “G codes” and “M codes.”

Language View of a Machining Center
-----------------------------------

Parameters
~~~~~~~~~~

In the RS274/NGC language view, a machining center maintains an array of 5400 numerical
parameters. Many of them have specific uses. The parameter array should persist over time, even if
the machining center is powered down.

Coordinate Systems
~~~~~~~~~~~~~~~~~~

In the RS274/NGC language view, a machining center has an absolute coordinate system and nine
program coordinate systems.

You can set the offsets of the nine program coordinate systems using G10 L2 Pn (n is the number of
the coordinate system) with values for the axes in terms of the absolute coordinate system.

You can select one of the nine systems by using G54, G55, G56, G57, G58, G59, G59.1, G59.2, or
G59.3. It is not possible to select the absolute coordinate system directly. You can offset the
current coordinate system using G92 or G92.3. This offset will then apply to all nine program
coordinate systems. This offset may be cancelled with G92.1 or G92.2.

You can make straight moves in the absolute machine coordinate system by using G53 with either G0 or
G1.

Data for coordinate systems is stored in parameters.

During initialization, the coordinate system is selected that is specified by parameter 5220. A
value of 1 means the first coordinate system (the one G54 activates), a value of 2 means the second
coordinate system (the one G55 activates), and so on. It is an error for the value of parameter 5220
to be anything but a whole number between one and nine.

Format of a Line
----------------

A permissible line of input RS274/NGC code consists of the following, in order, with the restriction
that there is a maximum (currently 256) to the number of characters allowed on a line.

#. an optional block delete character, which is a slash :code:`/` .
#. an optional line number.
#. any number of words, parameter settings, and comments.
#. an end of line marker (carriage return or line feed or both).

Spaces and tabs are allowed anywhere on a line of code and do not change the meaning of the line,
except inside comments. This makes some strange-looking input legal. The line :code:`g0x +0. 12 34y
7` is equivalent to :code:`g0 x+0.1234 y7`, for example.

Blank lines are allowed in the input. They are to be ignored.

Input is case insensitive, except in comments, i.e., any letter outside a comment may be in upper or
lower case without changing the meaning of a line.

Line Number
~~~~~~~~~~~

A line number is the letter :code:`N` followed by an integer (with no sign) between 0 and 99999
written with no more than five digits (000009 is not OK, for example). Line numbers may be repeated
or used out of order, although normal practice is to avoid such usage. Line numbers may also be
skipped, and that is normal practice. A line number is not required to be used, but must be in the
proper place if used.

Word
~~~~

A word is a letter other than :code:`N` followed by a real value.

Words may begin with any of the letters shown in the following table. The table includes :code:`N`
for completeness, even though, as defined above, line numbers are not words. Several letters
(:code:`I`, :code:`J, K`, :code:`L`, :code:`P`, :code:`R`) may have different meanings in different
contexts.

Table. Linux CNC Words and their meanings Letter

====== =====================================================
Letter 	Meaning
====== =====================================================
A       A axis of machine
B       B axis of machine
C       C axis of machine
D       Tool radius compensation number
F       Feed rate
G       General function (See table Modal Groups)
H       Tool length offset index
I       X offset for arcs and G87 canned cycles
J       Y offset for arcs and G87 canned cycles
K       Z offset for arcs and G87 canned cycles.
        Spindle-Motion Ratio for G33 synchronized movements.
L       Generic parameter word for G10, M66 and others
M       Miscellaneous function (See table Modal Groups)
N       Line number
P       Dwell time in canned cycles and with G4.
        Key used with G10.
Q       Feed increment in G73, G83 canned cycles
R       Arc radius or canned cycle plane
S       Spindle speed
T       Tool selection
U       U axis of machine
V       V axis of machine
W       W axis of machine
X       X axis of machine
Y       Y axis of machine
Z       Z axis of machine
====== =====================================================

A real value is some collection of characters that can be processed to come up with a number. A real
value may be an explicit number (such as 341 or -0.8807), a parameter value, an expression, or a
unary operation value.

Number
~~~~~

The following rules are used for (explicit) numbers. In these rules a digit is a single character
between 0 and 9.

* A number consists of (1) an optional plus or minus sign, followed by (2) zero to many digits,
  followed, possibly, by (3) one decimal point, followed by (4) zero to many digits — provided that
  there is at least one digit somewhere in the number.
* There are two kinds of numbers: integers and decimals. An integer does not have a decimal point in
  it; a decimal does.
* Numbers may have any number of digits, subject to the limitation on line length.
* A non-zero number with no sign as the first character is assumed to be positive.  Notice that
  initial (before the decimal point and the first non-zero digit) and trailing (after the decimal
  point and the last non-zero digit) zeros are allowed but not required. A number written with
  initial or trailing zeros will have the same value when it is read as if the extra zeros were not
  there.

Parameter Value
~~~~~~~~~~~~~~~

A parameter value is the pound character :code:`#` followed by a real value. The real value must
evaluate to an integer between 1 and 5399. The integer is a parameter number, and the value of the
parameter value is whatever number is stored in the numbered parameter.

The :code:`#` character takes precedence over other operations, so that, for example, :code:`#1+2`
means the number found by adding 2 to the value of parameter 1, not the value found in parameter
3. Of course, :code:`#[1+2]` does mean the value found in parameter 3. The :code:`#` character may
be repeated; for example :code:`##2` means the value of the parameter whose index is the (integer)
value of parameter 2.

Expressions and Binary Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An expression is a set of characters starting with a left bracket :code:`[` and ending with a
balancing right bracket :code:`]`. In between the brackets are numbers, parameter values,
mathematical operations, and other expressions. An expression may be evaluated to produce a
number. The expressions on a line are evaluated when the line is read, before anything on the line
is executed. An example of an expression is :code:`[ 1 + acos[0] - [#3 ** [4.0/2]]]`.

Binary operations appear only inside expressions. Nine binary operations are defined. There are four
basic mathematical operations: addition :code:`+`, subtraction :code:`-`, multiplication :code:`*`,
and division :code:`/`. There are three logical operations: non-exclusive or :code:`OR`, exclusive
or :code:`XOR`, and logical and :code:`AND`. The eighth operation is the modulus operation
:code:`MOD`. The ninth operation is the “power” operation :code:`**` of raising the number on the
left of the operation to the power on the right.  The binary operations are divided into three
groups. The first group is: power. The second group is: multiplication, division, and modulus. The
third group is: addition, subtraction, logical non- exclusive or, logical exclusive or, and logical
and. If operations are strung together (for example in the expression :code:`[2.0 / 3 * 1.5 - 5.5 /
11.0]`), operations in the first group are to be performed before operations in the second group and
operations in the second group before operations in the third group. If an expression contains more
than one operation from the same group (such as the first / and * in the example), the operation on
the left is performed first. Thus, the example is equivalent to: :code:`[((2.0 / 3) * 1.5) - (5.5 /
11.0)]`, which simplifies to :code:`[1.0 - 0.5]`, which is 0.5.

The logical operations and modulus are to be performed on any real numbers, not just on integers.
The number zero is equivalent to logical false, and any non-zero number is equivalent to logical
true.

Unary Operation Value
~~~~~~~~~~~~~~~~~~~~~

A unary operation value is either :code:`ATAN` followed by one expression divided by another
expression (for example :code:`ATAN[2]/[1+3]`) or any other unary operation name followed by an
expression (for example :code:`SIN[90]`). The unary operations are: :code:`ABS` (absolute value),
:code:`ACOS` (arc cosine), :code:`ASIN` (arc sine), :code:`ATAN` (arc tangent), :code:`COS`
(cosine), :code:`EXP` (e raised to the given power), :code:`FIX` (round down), :code:`FUP` (round
up), :code:`LN` (natural logarithm), :code:`ROUND` (round to the nearest whole number), :code:`SIN`
(sine), :code:`SQRT` (square root), and :code:`TAN` (tangent). Arguments to unary operations which
take angle measures (:code:`COS`, :code:`SIN`, and :code:`TAN`) are in degrees. Values returned by
unary operations which return angle measures (:code:`ACOS`, :code:`ASIN`, and :code:`ATAN`) are also
in degrees.

The :code:`FIX` operation rounds towards the left (less positive or more negative) on a number line,
so that :code:`FIX[2.8] = 2` and :code:`FIX[-2.8] = -3`, for example. The :code:`FUP` operation
rounds towards the right (more positive or less negative) on a number line; :code:`FUP[2.8] = 3` and
:code:`FUP[-2.8] = -2`, for example.

Parameter Setting
~~~~~~~~~~~~~~~~~

A parameter setting is the following four items one after the other: (1) a pound character
:code:`#`, (2) a real value which evaluates to an integer between 1 and 5399, (3) an equal sign
:code:`=`, and (4) a real value. For example :code:`#3 = 15` is a parameter setting meaning “set
parameter 3 to 15.”

A parameter setting does not take effect until after all parameter values on the same line have
been found. For example, if parameter 3 has been previously set to 15 and the line :code:`#3=6 G1
x#3` is interpreted, a straight move to a point where x equals 15 will occur and the value of
parameter 3 will be 6.

Comments and Messages
~~~~~~~~~~~~~~~~~~~~~

Printable characters and white space inside parentheses is a comment. A left parenthesis always
starts a comment. The comment ends at the first right parenthesis found thereafter. Once a left
parenthesis is placed on a line, a matching right parenthesis must appear before the end of the
line.  Comments may not be nested; it is an error if a left parenthesis is found after the start of
a comment and before the end of the comment. Here is an example of a line containing a comment:
:code:`G80 M5 (stop motion)`. Comments do not cause a machining center to do anything.

.. A comment contains a message if “MSG,” appears after the left parenthesis and before any other
  printing characters. Variants of “MSG,” which include white space and lower case characters are
  allowed. The rest of the characters before the right parenthesis are considered to be a message.
  Messages should be displayed on the message display device. Comments not containing messages need
  not be displayed there.

Item Repeats
~~~~~~~~~~~~

A line may have any number of :code:`G` words, but two :code:`G` words from the same modal group may
not appear on the same line.

A line may have zero to four :code:`M` words. Two :code:`M` words from the same modal group may not
appear on the same line.

For all other legal letters, a line may have only one word beginning with that letter.

If a parameter setting of the same parameter is repeated on a line, :code:`#3=15 #3=6`, for example,
only the last setting will take effect. It is silly, but not illegal, to set the same parameter
twice on the same line.

If more than one comment appears on a line, only the last one will be used; each of the other
comments will be read and its format will be checked, but it will be ignored thereafter. It is
expected that putting more than one comment on a line will be very rare.

Item order
~~~~~~~~~~

The three types of item whose order may vary on a line (as given at the beginning of this section)
are word, parameter setting, and comment. Imagine that these three types of item are divided into
three groups by type.

The first group (the words) may be reordered in any way without changing the meaning of the line.

If the second group (the parameter settings) is reordered, there will be no change in the meaning of
the line unless the same parameter is set more than once. In this case, only the last setting of the
parameter will take effect. For example, after the line :code:`#3=15 #3=6` has been interpreted, the
value of parameter 3 will be 6. If the order is reversed to :code:`#3=6 #3=15` and the line is
interpreted, the value of parameter 3 will be 15.

If the third group (the comments) contains more than one comment and is reordered, only the last
comment will be used.

If each group is kept in order or reordered without changing the meaning of the line, then the three
groups may be interleaved in any way without changing the meaning of the line. For example, the line
:code:`g40 g1 #3=15 (foo) #4=-7.0` has five items and means exactly the same thing in any of the 120
possible orders (such as :code:`#4=-7.0 g1 #3=15 g40 (foo)`) for the five items.

Commands and Machine Modes
~~~~~~~~~~~~~~~~~~~~~~~~~~

In RS274/NGC, many commands cause a machining center to change from one mode to another, and the
mode stays active until some other command changes it implicitly or explicitly. Such commands are
called “modal”. For example, if coolant is turned on, it stays on until it is explicitly turned
off. The :code:`G` codes for motion are also modal. If a :code:`G1` (straight move) command is given
on one line, for example, it will be executed again on the next line if one or more axis words is
available on the line, unless an explicit command is given on that next line using the axis words or
cancelling motion.

“Non-modal” codes have effect only on the lines on which they occur. For example, :code:`G4` (dwell)
is non-modal.

Modal Groups
------------

Modal commands are arranged in sets called “modal groups”, and only one member of a modal group may
be in force at any given time. In general, a modal group contains commands for which it is logically
impossible for two members to be in effect at the same time — like measure in inches vs. measure in
millimeters. A machining center may be in many modes at the same time, with one mode from each modal
group being in effect.

.. The modal groups are shown in Table 4.

For several modal groups, when a machining center is ready to accept commands, one member of the
group must be in effect. There are default settings for these modal groups. When the machining
center is turned on or otherwise re-initialized, the default values are automatically in effect.

Group 1, the first group on the table, is a group of :code:`G` codes for motion. One of these is
always in effect. That one is called the current motion mode.

It is an error to put a G-code from group 1 and a G-code from group 0 on the same line if both of
them use axis words. If an axis word-using G-code from group 1 is implicitly in effect on a line (by
having been activated on an earlier line), and a group 0 G-code that uses axis words appears on the
line, the activity of the group 1 G-code is suspended for that line. The axis word-using G-codes
from group 0 are :code:`G10`, :code:`G28`, :code:`G30`, and :code:`G92`.

G and Input Codes
-----------------

See ...

..
  G codes of the RS274/NGC language are shown in Table 5 and described following that.

  In the command prototypes, three dots (...) stand for a real value. As described earlier, a real
  value may be (1) an explicit number, 4, for example, (2) an expression, :code:`[2+2]`, for example,
  (3) a parameter value, #88, for example, or (4) a unary function value, :code:`acos[0]`, for
  example.  In most cases, if axis words (any or all of X..., Y..., Z..., A..., B..., C...) are given,
  they specify a destination point. Axis numbers are in the currently active coordinate system, unless
  explicitly described as being in the absolute coordinate system. Where axis words are optional, any
  omitted axes will have their current value. Any items in the command prototypes not explicitly
  described as optional are required. It is an error if a required item is omitted.

  In the prototypes, the values following letters are often given as explicit numbers. Unless stated
  otherwise, the explicit numbers can be real values. For example, :code:`G10 L2` could equally well
  be written :code:`G[2*5] L[1+1]`. If the value of parameter 100 were 2, :code:`G10 L#100` would also
  mean the same. Using real values which are not explicit numbers as just shown in the examples is
  rarely useful.

  If L... is written in a prototype the “...” will often be referred to as the “L number”. Similarly the
  “...” in H... may be called the “H number”, and so on for any other letter.

Order of Execution
------------------

The order of execution of items on a line is critical to safe and effective machine operation. Items
are executed in a particular order if they occur on the same line.

"""
