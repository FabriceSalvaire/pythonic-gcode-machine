####################################################################################################
#
# PythonicGcodeMachine - A Python G-code Toolkit
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

####################################################################################################
#
#                                       G-code documentation
#
# Note: This file contains only doc strings for G-codes.
#       Each G-code has a corresponding class with a doc string.
#       See also class name format, cf. supra.
#       For simplicity, doc strings are stored in a Python file instead of a YAML file.
#       But this documentation can be converted to HTML and stored in a JSON file, if needed for
#       other purposes.
#
####################################################################################################

"""G-code documentation from NIST paper, see :ref:`rs-274-reference-page`.

.. warning::
   Must be checked for PDF to rST errors.

.. note::
   Class Name Format:

    * G1_G2 for G1 and G2,
    * G1_1 for G1.1,
    * G1_to_G10 for G1 to G10.

G codes of the RS274/NGC language are shown in Table 5 and described following that.

In the command prototypes, three dots (…) stand for a real value. As described earlier, a real value
may be (1) an explicit number, 4, for example, (2) an expression, [2+2], for example, (3) a
parameter value, #88, for example, or (4) a unary function value, acos[0], for example.

In most cases, if axis words (any or all of X…, Y…, Z…, A…, B…, C…) are given, they specify a
destination point. Axis numbers are in the currently active coordinate system, unless explicitly
described as being in the absolute coordinate system. Where axis words are optional, any omitted
axes will have their current value. Any items in the command prototypes not explicitly described as
optional are required. **It is an error if a required item is omitted.**

In the prototypes, the values following letters are often given as explicit numbers. Unless stated
otherwise, the explicit numbers can be real values. For example, G10 L2 could equally well be
written G[2*5] L[1+1]. If the value of parameter 100 were 2, G10 L#100 would also mean the
same. Using real values which are not explicit numbers as just shown in the examples is rarely
useful.

If L… is written in a prototype the “…” will often be referred to as the “L number”. Similarly the
“…” in H… may be called the “H number”, and so on for any other letter.

"""

####################################################################################################

class G0:

    """**Rapid Linear Motion — G0**

    For rapid linear motion, program G0 X… Y… Z… A… B… C…, where all the axis words are optional,
    except that at least one must be used. The G0 is optional if the current motion mode is G0. This
    will produce coordinated linear motion to the destination point at the current traverse rate (or
    slower if the machine will not go that fast). It is expected that cutting will not take place
    when a G0 command is executing.

    **It is an error if:**

    * all axis words are omitted.

    If cutter radius compensation is active, the motion will differ from the above; see Appendix
    B. If G53 is programmed on the same line, the motion will also differ; see Section 3.5.12.

    """

####################################################################################################

class G1:

    """**Linear Motion at Feed Rate — G1**

    For linear motion at feed rate (for cutting or not), program G1 X… Y… Z…  A… B… C…, where all
    the axis words are optional, except that at least one must be used. The G1 is optional if the
    current motion mode is G1. This will produce coordinated linear motion to the destination point
    at the current feed rate (or slower if the machine will not go that fast).

    **It is an error if:**

    * all axis words are omitted.

    If cutter radius compensation is active, the motion will differ from the above; see Appendix
    B. If G53 is programmed on the same line, the motion will also differ; see Section 3.5.12.

    """

####################################################################################################

class G2_G3:

    """**Arc at Feed Rate — G2 and G3**

    A circular or helical arc is specified using either G2 (clockwise arc)
    or G3 (counterclockwise arc).

    The axis of the circle or helix must be parallel to the X, Y, or Z-axis of the machine
    coordinate system. The axis (or, equivalently, the plane perpendicular to the axis) is selected
    with G17 (Z-axis, XY-plane), G18 (Y-axis, XZ-plane), or G19 (X-axis, YZ-plane). If the arc is
    circular, it lies in a plane parallel to the selected plane.

    If a line of RS274/NGC code makes an arc and includes rotational axis motion, the rotational
    axes turn at a constant rate so that the rotational motion starts and finishes when the XYZ
    motion starts and finishes. Lines of this sort are hardly ever programmed.

    If cutter radius compensation is active, the motion will differ from what is described here. See
    Appendix B.

    Two formats are allowed for specifying an arc. We will call these the center format and the
    radius format. In both formats the G2 or G3 is optional if it is the current motion mode.

    *Radius Format Arc*

    In the radius format, the coordinates of the end point of the arc in the selected plane are
    specified along with the radius of the arc. Program G2 X… Y… Z… A… B… C… R… (or use G3 instead
    of G2). R is the radius. The axis words are all optional except that at least one of the two
    words for the axes in the selected plane must be used. The R number is the radius.  A positive
    radius indicates that the arc turns through 180 degrees or less, while a negative radius
    indicates a turn of 180 degrees to 359.999 degrees. If the arc is helical, the value of the end
    point of the arc on the coordinate axis parallel to the axis of the helix is also specified.

    **It is an error if:**

    * both of the axis words for the axes of the selected plane are omitted,
    * the end point of the arc is the same as the current point.

    It is not good practice to program radius format arcs that are nearly full circles or are
    semicircles (or nearly semicircles) because a small change in the location of the end point will
    produce a much larger change in the location of the center of the circle (and, hence, the middle
    of the arc).

    The magnification effect is large enough that rounding error in a number can produce
    out-of-tolerance cuts. Nearly full circles are outrageously bad, semicircles (and nearly so) are
    only very bad. Other size arcs (in the range tiny to 165 degrees or 195 to 345 degrees) are OK.

    Here is an example of a radius format command to mill an arc: G17 G2 x 10 y 15 r 20 z 5.

    That means to make a clockwise (as viewed from the positive Z-axis) circular or helical arc
    whose axis is parallel to the Z-axis, ending where X=10, Y=15, and Z=5, with a radius of 20. If
    the starting value of Z is 5, this is an arc of a circle parallel to the XY-plane; otherwise it
    is a helical arc.

    *Center Format Arc*

    In the center format, the coordinates of the end point of the arc in the selected plane are
    specified along with the offsets of the center of the arc from the current location. In this
    format, it is OK if the end point of the arc is the same as the current point.

    **It is an error if:**

    * when the arc is projected on the selected plane, the distance from the current point to the
      center differs from the distance from the end point to the center by more than 0.0002 inch (if
      inches are being used) or 0.002 millimeter (if millimeters are being used).

    When the XY-plane is selected, program G2 X… Y… Z… A… B… C… I… J… (or use G3 instead of G2). The
    axis words are all optional except that at least one of X and Y must be used. I and J are the
    offsets from the current location (in the X and Y directions, respectively) of the center of the
    circle. I and J are optional except that at least one of the two must be used.

    **It is an error if:**

    * X and Y are both omitted,
    * I and J are both omitted.

    When the XZ-plane is selected, program G2 X… Y… Z… A… B… C… I… K… (or use G3 instead of G2). The
    axis words are all optional except that at least one of X and Z must be used. I and K are the
    offsets from the current location (in the X and Z directions, respectively) of the center of the
    circle. I and K are optional except that at least one of the two must be used.

    **It is an error if:**

    * X and Z are both omitted,
    * I and K are both omitted.

    When the YZ-plane is selected, program G2 X… Y… Z… A… B… C… J… K… (or use G3 instead of G2). The
    axis words are all optional except that at least one of Y and Z must be used. J and K are the
    offsets from the current location (in the Y and Z directions, respectively) of the center of the
    circle. J and K are optional except that at least one of the two must be used.

    **It is an error if:**

    * Y and Z are both omitted,
    * J and K are both omitted.

    Here is an example of a center format command to mill an arc: G17 G2 x 10 y 16 i 3 j 4 z 9.

    That means to make a clockwise (as viewed from the positive z-axis) circular or helical arc
    whose axis is parallel to the Z-axis, ending where X=10, Y=16, and Z=9, with its center offset
    in the X direction by 3 units from the current X location and offset in the Y direction by 4
    units from the current Y location. If the current location has X=7, Y=7 at the outset, the
    center will be at X=10, Y=11. If the starting value of Z is 9, this is a circular arc; otherwise
    it is a helical arc. The radius of this arc would be 5.

    In the center format, the radius of the arc is not specified, but it may be found easily as the
    distance from the center of the circle to either the current point or the end point of the arc.

    """

####################################################################################################

class G4:

    """**Dwell — G4**

    For a dwell, program G4 P… . This will keep the axes unmoving for the period of time in seconds
    specified by the P number.

    **It is an error if:**

    * the P number is negative.

    """

####################################################################################################

class G10:

    """**Set Coordinate System Data — G10**

    The RS274/NGC language view of coordinate systems is described in Section 3.2.2.

    To set the coordinate values for the origin of a coordinate system, program G10 L2 P … X… Y… Z…
    A…  B… C…, where the P number must evaluate to an integer in the range 1 to 9 (corresponding to
    G54 to G59.3) and all axis words are optional. The coordinates of the origin of the coordinate
    system specified by the P number are reset to the coordinate values given (in terms of the
    absolute coordinate system). Only those coordinates for which an axis word is included on the
    line will be reset.

    **It is an error if:**

    * the P number does not evaluate to an integer in the range 1 to 9.  If origin offsets (made by
      G92 or G92.3) were in effect before G10 is used, they will continue to be in effect
      afterwards.

    The coordinate system whose origin is set by a G10 command may be active or inactive at the time
    the G10 is executed.

    Example: G10 L2 P1 x 3.5 y 17.2 sets the origin of the first coordinate system (the one selected
    by G54) to a point where X is 3.5 and Y is 17.2 (in absolute coordinates). The Z coordinate of
    the origin (and the coordinates for any rotational axes) are whatever those coordinates of the
    origin were before the line was executed.

    """

####################################################################################################

class G17_G18_G19:

    """**Plane Selection — G17, G18, and G19**

    Program G17 to select the XY-plane, G18 to select the XZ-plane, or G19 to select the YZ-plane.

    The effects of having a plane selected are discussed in Section 3.5.3 and Section 3.5.16.

    """

####################################################################################################

class G20_G21:

    """**Length Units — G20 and G21**

    Program G20 to use inches for length units. Program G21 to use millimeters.

    It is usually a good idea to program either G20 or G21 near the beginning of a program before
    any motion occurs, and not to use either one anywhere else in the program.  It is the
    responsibility of the user to be sure all numbers are appropriate for use with the current
    length units.

    """

####################################################################################################

class G28_G30:

    """**Return to Home — G28 and G30**

    Two home positions are defined (by parameters 5161-5166 for G28 and parameters 5181-5186 for
    G30). The parameter values are in terms of the absolute coordinate system, but are in
    unspecified length units.

    To return to home position by way of the programmed position, program G28 X… Y… Z… A…  B… C… (or
    use G30). All axis words are optional. The path is made by a traverse move from the current
    position to the programmed position, followed by a traverse move to the home position. If no
    axis words are programmed, the intermediate point is the current point, so only one move is
    made.

    """

####################################################################################################

class G38_2:

    """**Straight Probe — G38.2**

    *The Straight Probe Command*

    Program G38.2 X… Y… Z… A… B… C… to perform a straight probe operation.  The rotational axis
    words are allowed, but it is better to omit them. If rotational axis words are used, the numbers
    must be the same as the current position numbers so that the rotational axes do not move. The
    linear axis words are optional, except that at least one of them must be used. The tool in the
    spindle must be a probe.

    **It is an error if:**

    * the current point is less than 0.254 millimeter or 0.01 inch from the programmed point.
    * G38.2 is used in inverse time feed rate mode,
    * any rotational axis is commanded to move,
    * no X, Y, or Z-axis word is used.

    In response to this command, the machine moves the controlled point (which should be at the end
    of the probe tip) in a straight line at the current feed rate toward the programmed point. If
    the probe trips, the probe is retracted slightly from the trip point at the end of command
    execution. If the probe does not trip even after overshooting the programmed point slightly, an
    error is signalled.

    After successful probing, parameters 5061 to 5066 will be set to the coordinates of the location
    of the controlled point at the time the probe tripped.

    *Using the Straight Probe Command*

    Using the straight probe command, if the probe shank is kept nominally parallel to the Z-axis
    (i.e., any rotational axes are at zero) and the tool length offset for the probe is used, so
    that the controlled point is at the end of the tip of the probe:

    * without additional knowledge about the probe, the parallelism of a face of a part to the
      XY-plane may, for example, be found.

    * if the probe tip radius is known approximately, the parallelism of a face of a part to the YZ
      or XZ-plane may, for example, be found.

    * if the shank of the probe is known to be well-aligned with the Z-axis and the probe tip radius
      is known approximately, the center of a circular hole, may, for example, be found.

    * if the shank of the probe is known to be well-aligned with the Z-axis and the probe tip radius
      is known precisely, more uses may be made of the straight probe command, such as finding the
      diameter of a circular hole.

    If the straightness of the probe shank cannot be adjusted to high accuracy, it is desirable to
    know the effective radii of the probe tip in at least the +X, -X, +Y, and -Y directions. These
    quantities can be stored in parameters either by being included in the parameter file or by
    being set in an RS274/NGC program.

    Using the probe with rotational axes not set to zero is also feasible.  Doing so is more complex
    than when rotational axes are at zero, and we do not deal with it here.

    *Example Code*

    As a usable example, the code for finding the center and diameter of a circular hole is shown in
    Table 6. For this code to yield accurate results, the probe shank must be well-aligned with the
    Z-axis, the cross section of the probe tip at its widest point must be very circular, and the
    probe tip radius (i.e., the radius of the circular cross section) must be known precisely. If
    the probe tip radius is known only approximately (but the other conditions hold), the location
    of the hole center will still be accurate, but the hole diameter will not.

    In Table 6, an entry of the form *description of number* is meant to be replaced by an actual
    number that matches the *description of number*. After this section of code has executed, the
    X-value of the center will be in parameter 1041, the Y-value of the center in parameter 1022,
    and the diameter in parameter 1034. In addition, the diameter parallel to the X-axis will be in
    parameter 1024, the diameter parallel to the Y-axis in parameter 1014, and the difference (an
    indicator of circularity) in parameter 1035. The probe tip will be in the hole at the XY center
    of the hole.

    The example does not include a tool change to put a probe in the spindle. Add the tool change
    code at the beginning, if needed.

    """

####################################################################################################

class G40_G41_G42:

    """**Cutter Radius Compensation — G40, G41, and G42**

    To turn cutter radius compensation off, program G40. It is OK to turn compensation off when it
    is already off.

    Cutter radius compensation may be performed only if the XY-plane is active.

    To turn cutter radius compensation on left (i.e., the cutter stays to the left of the programmed
    path

    **Table 6. Code to Probe Hole**

    .. code::

        N010 (probe to find center and diameter of circular hole)
        N020 (This program will not run as given here. You have to)
        N030 (insert numbers in place of <description of number>.)
        N040 (Delete lines N020, N030, and N040 when you do that.)
        N050 G0 Z <Z-value of retracted position> F <feed rate>
        N060 #1001=<nominal X-value of hole center>
        N070 #1002=<nominal Y-value of hole center>
        N080 #1003=<some Z-value inside the hole>
        N090 #1004=<probe tip radius>
        N100 #1005=[<nominal hole diameter>/2.0 - #1004]
        N110 G0 X#1001 Y#1002 (move above nominal hole center)
        N120 G0 Z#1003 (move into hole - to be cautious, substitute G1 for G0 here)
        N130 G38.2 X[#1001 + #1005] (probe +X side of hole)
        N140 #1011=#5061 (save results)
        N150 G0 X#1001 Y#1002 (back to center of hole)
        N160 G38.2 X[#1001 - #1005] (probe -X side of hole)
        N170 #1021=[[#1011 + #5061] / 2.0] (find pretty good X-value of hole center)
        N180 G0 X#1021 Y#1002 (back to center of hole)
        N190 G38.2 Y[#1002 + #1005] (probe +Y side of hole)
        N200 #1012=#5062 (save results)
        N210 G0 X#1021 Y#1002 (back to center of hole)
        N220 G38.2 Y[#1002 - #1005] (probe -Y side of hole)
        N230 #1022=[[#1012 + #5062] / 2.0] (find very good Y-value of hole center)
        N240 #1014=[#1012 - #5062 + [2 \* #1004]] (find hole diameter in Y-direction)
        N250 G0 X#1021 Y#1022 (back to center of hole)
        N260 G38.2 X[#1021 + #1005] (probe +X side of hole)
        N270 #1031=#5061 (save results)
        N280 G0 X#1021 Y#1022 (back to center of hole)
        N290 G38.2 X[#1021 - #1005] (probe -X side of hole)
        N300 #1041=[[#1031 + #5061] / 2.0] (find very good X-value of hole center)
        N310 #1024=[#1031 - #5061 + [2 \* #1004]] (find hole diameter in X-direction)
        N320 #1034=[[#1014 + #1024] / 2.0] (find average hole diameter)
        N330 #1035=[#1024 - #1014] (find difference in hole diameters)
        N340 G0 X#1041 Y#1022 (back to center of hole)
        N350 M2 (that’s all, folks)

    when the tool radius is positive), program G41 D… . To turn cutter radius compensation on right
    (i.e., the cutter stays to the right of the programmed path when the tool radius is positive),
    program G42 D… . The D word is optional; if there is no D word, the radius of the tool currently
    in the spindle will be used. If used, the D number should normally be the slot number of the
    tool in the spindle, although this is not required. It is OK for the D number to be zero; a
    radius value of zero will be used.

    **It is an error if:**

    * the D number is not an integer, is negative or is larger than the number of carousel slots,
    * the XY-plane is not active,
    * cutter radius compensation is commanded to turn on when it is already on.

    The behavior of the machining center when cutter radius compensation is on is described in
    Appendix B.

    """

####################################################################################################

class G43_G49:

    """**Tool Length Offsets — G43 and G49**

    To use a tool length offset, program G43 H…, where the H number is the desired index in the tool
    table. It is expected that all entries in this table will be positive.  The H number should be,
    but does not have to be, the same as the slot number of the tool currently in the spindle. It is
    OK for the H number to be zero; an offset value of zero will be used.

    **It is an error if:**

    * the H number is not an integer, is negative, or is larger than the number of carousel slots.

    To use no tool length offset, program G49.

    It is OK to program using the same offset already in use. It is also OK to program using no tool
    length offset if none is currently being used.

    """

####################################################################################################

class G53:

    """**Move in Absolute Coordinates — G53**

    For linear motion to a point expressed in absolute coordinates, program G1 G53 X… Y… Z…  A… B…
    C…  (or use G0 instead of G1), where all the axis words are optional, except that at least one
    must be used. The G0 or G1 is optional if it is the current motion mode. G53 is not modal and
    must be programmed on each line on which it is intended to be active.  This will produce
    coordinated linear motion to the programmed point. If G1 is active, the speed of motion is the
    current feed rate (or slower if the machine will not go that fast). If G0 is active, the speed
    of motion is the current traverse rate (or slower if the machine will not go that fast).

    **It is an error if:**

    * G53 is used without G0 or G1 being active,
    * G53 is used while cutter radius compensation is on.

    See Section 3.2.2 for an overview of coordinate systems.

    """

####################################################################################################

class G54_to_G59_3:

    """**Select Coordinate System — G54 to G59.3**

    To select coordinate system 1, program G54, and similarly for other coordinate systems. The
    system-number—G-code pairs are: (1—G54), (2—G55), (3—G56), (4—G57), (5—G58), (6—G59), (7—G59.1),
    (8—G59.2), and (9—G59.3).

    **It is an error if:**

    * one of these G-codes is used while cutter radius compensation is on.

    See Section 3.2.2 for an overview of coordinate systems.

    """

####################################################################################################

class G61_G61_1_G64:

    """**Set Path Control Mode — G61, G61.1, and G64**

    Program G61 to put the machining center into exact path mode, G61.1 for exact stop mode, or G64
    for continuous mode. It is OK to program for the mode that is already active. See Section
    2.1.2.16 for a discussion of these modes.

    """

####################################################################################################

class G80:

    """**Cancel Modal Motion — G80**

    Program G80 to ensure no axis motion will occur.

    **It is an error if:**

    * Axis words are programmed when G80 is active, unless a modal group 0 G code is programmed
      which uses axis words.

    """

####################################################################################################

class G81_to_G89:

    """**Canned Cycles — G81 to G89**

    The canned cycles G81 through G89 have been implemented as described in this section. Two
    examples are given with the description of G81 below.

    All canned cycles are performed with respect to the currently selected plane. Any of the three
    planes (XY, YZ, ZX) may be selected. Throughout this section, most of the descriptions assume
    the XY-plane has been selected. The behavior is always analogous if the YZ or XZ-plane is
    selected.

    Rotational axis words are allowed in canned cycles, but it is better to omit them. If rotational
    axis words are used, the numbers must be the same as the current position numbers so that the
    rotational axes do not move.

    All canned cycles use X, Y, R, and Z numbers in the NC code. These numbers are used to determine
    X, Y, R, and Z positions. The R (usually meaning retract) position is along the axis
    perpendicular to the currently selected plane (Z-axis for XY-plane, X-axis for YZ-plane, Y-axis
    for XZ-plane). Some canned cycles use additional arguments.

    For canned cycles, we will call a number “sticky” if, when the same cycle is used on several
    lines of code in a row, the number must be used the first time, but is optional on the rest of
    the lines.

    Sticky numbers keep their value on the rest of the lines if they are not explicitly programmed
    to be different. The R number is always sticky.

    In incremental distance mode: when the XY-plane is selected, X, Y, and R numbers are treated as
    increments to the current position and Z as an increment from the Z-axis position before the
    move involving Z takes place; when the YZ or XZ-plane is selected, treatment of the axis words
    is analogous. In absolute distance mode, the X, Y, R, and Z numbers are absolute positions in
    the current coordinate system.

    The L number is optional and represents the number of repeats. L=0 is not allowed. If the repeat
    feature is used, it is normally used in incremental distance mode, so that the same sequence of
    motions is repeated in several equally spaced places along a straight line. In absolute distance
    mode, L > 1 means “do the same cycle in the same place several times,” Omitting the L word is
    equivalent to specifying L=1. The L number is not sticky.

    When L>1 in incremental mode with the XY-plane selected, the X and Y positions are determined by
    adding the given X and Y numbers either to the current X and Y positions (on the first go-
    around) or to the X and Y positions at the end of the previous go-around (on the
    repetitions). The R and Z positions do not change during the repeats.

    The height of the retract move at the end of each repeat (called “clear Z” in the descriptions
    below) is determined by the setting of the retract mode: either to the original Z position (if
    that is above the R position and the retract mode is G98, OLD_Z), or otherwise to the R
    position. See Section 3.5.20

    **It is an error if:**

    * X, Y, and Z words are all missing during a canned cycle,
    * a P number is required and a negative P number is used,
    * an L number is used that does not evaluate to a positive integer,
    * rotational axis motion is used during a canned cycle,
    * inverse time feed rate is active during a canned cycle,
    * cutter radius compensation is active during a canned cycle.

    When the XY plane is active, the Z number is sticky, and **it is an error if:**

    * the Z number is missing and the same canned cycle was not already active,
    * the R number is less than the Z number.

    When the XZ plane is active, the Y number is sticky, and **it is an error if:**

    * the Y number is missing and the same canned cycle was not already active,
    * the R number is less than the Y number.

    When the YZ plane is active, the X number is sticky, and **it is an error if:**

    * the X number is missing and the same canned cycle was not already active,
    * the R number is less than the X number.

    *Preliminary and In-Between Motion*

    At the very beginning of the execution of any of the canned cycles, with the XY-plane selected,
    if the current Z position is below the R position, the Z-axis is traversed to the R
    position. This happens only once, regardless of the value of L.

    In addition, at the beginning of the first cycle and each repeat, the following one or two moves
    are made:

    1. a straight traverse parallel to the XY-plane to the given XY-position,

    2. a straight traverse of the Z-axis only to the R position, if it is not already at the R
    position.

    If the XZ or YZ plane is active, the preliminary and in-between motions are analogous.

    *G81 Cycle*

    The G81 cycle is intended for drilling. Program G81 X… Y… Z… A… B… C… R…  L…

    0. Preliminary motion, as described above.
    1. Move the Z-axis only at the current feed rate to the Z position.
    2. Retract the Z-axis at traverse rate to clear Z.

    **Example 1**

    Suppose the current position is (1, 2, 3) and the XY-plane has been selected, and the following
    line of NC code is interpreted.

    G90 G81 G98 X4 Y5 Z1.5 R2.8

    This calls for absolute distance mode (G90) and OLD_Z retract mode (G98) and calls for the G81
    drilling cycle to be performed once. The X number and X position are 4.  The Y number and Y
    position are 5. The Z number and Z position are 1.5. The R number and clear Z are 2.8. Old Z is
    3.

    The following moves take place.

    1. a traverse parallel to the XY-plane to (4,5,3)
    2. a traverse parallel to the Z-axis to (4,5,2.8)
    3. a feed parallel to the Z-axis to (4,5,1.5)
    4. a traverse parallel to the Z-axis to (4,5,3)

    **Example 2**

    Suppose the current position is (1, 2, 3) and the XY-plane has been selected, and the following
    line of NC code is interpreted.

    G91 G81 G98 X4 Y5 Z-0.6 R1.8 L3

    This calls for incremental distance mode (G91) and OLD_Z retract mode (G98) and calls for the
    G81 drilling cycle to be repeated three times. The X number is 4, the Y number is 5, the Z
    number is -0.6 and the R number is 1.8. The initial X position is 5 (=1+4), the initial Y
    position is 7 (=2+5), the clear Z position is 4.8 (=1.8+3), and the Z position is 4.2
    (=4.8-0.6). Old Z is 3.

    The first move is a traverse along the Z-axis to (1,2,4.8), since old Z < clear Z.

    The first repeat consists of 3 moves.

    1. a traverse parallel to the XY-plane to (5,7,4.8)
    2. a feed parallel to the Z-axis to (5,7, 4.2)
    3. a traverse parallel to the Z-axis to (5,7,4.8)

    The second repeat consists of 3 moves. The X position is reset to 9 (=5+4) and the Y position to
    12 (=7+5).

    1. a traverse parallel to the XY-plane to (9,12,4.8)
    2. a feed parallel to the Z-axis to (9,12, 4.2)
    3. a traverse parallel to the Z-axis to (9,12,4.8)

    The third repeat consists of 3 moves. The X position is reset to 13 (=9+4) and the Y position to
    17 (=12+5).

    1. a traverse parallel to the XY-plane to (13,17,4.8)
    2. a feed parallel to the Z-axis to (13,17, 4.2)
    3. a traverse parallel to the Z-axis to (13,17,4.8)

    *G82 Cycle*

    The G82 cycle is intended for drilling. Program G82 X… Y… Z… A… B… C… R…  L… P…

    0. Preliminary motion, as described above.
    1. Move the Z-axis only at the current feed rate to the Z position.
    2. Dwell for the P number of seconds.
    3. Retract the Z-axis at traverse rate to clear Z.

    *G83 Cycle*

    The G83 cycle (often called peck drilling) is intended for deep drilling or milling with chip
    breaking. The retracts in this cycle clear the hole of chips and cut off any long stringers
    (which are common when drilling in aluminum). This cycle takes a Q number which represents a
    “delta” increment along the Z-axis. Program G83 X… Y… Z… A… B… C… R… L… Q…

    0. Preliminary motion, as described above.
    1. Move the Z-axis only at the current feed rate downward by delta or to the Z position,
       whichever is less deep.
    2. Rapid back out to the clear_z.
    3. Rapid back down to the current hole bottom, backed off a bit.
    4. Repeat steps 1, 2, and 3 until the Z position is reached at step 1.
    5. Retract the Z-axis at traverse rate to clear Z.

    **It is an error if:**

    * the Q number is negative or zero.

    *G84 Cycle*

    The G84 cycle is intended for right-hand tapping with a tap tool.

    Program G84 X… Y… Z… A… B… C… R… L…

    0. Preliminary motion, as described above.
    1. Start speed-feed synchronization.
    2. Move the Z-axis only at the current feed rate to the Z position.
    3. Stop the spindle.
    4. Start the spindle counterclockwise.
    5. Retract the Z-axis at the current feed rate to clear Z.
    6. If speed-feed synch was not on before the cycle started, stop it.
    7. Stop the spindle.
    8. Start the spindle clockwise.

    The spindle must be turning clockwise before this cycle is used. **It is an error if:**

    * the spindle is not turning clockwise before this cycle is executed.

    With this cycle, the programmer must be sure to program the speed and feed in the correct
    proportion to match the pitch of threads being made. The relationship is that the spindle speed
    equals the feed rate times the pitch (in threads per length unit). For example, if the pitch is
    2 threads per millimeter, the active length units are millimeters, and the feed rate has been
    set with the command F150, then the speed should be set with the command S300, since 150 x 2 =
    300.

    If the feed and speed override switches are enabled and not set at 100%, the one set at the
    lower setting will take effect. The speed and feed rates will still be synchronized.

    *G85 Cycle*

    The G85 cycle is intended for boring or reaming, but could be used for drilling or milling.

    Program G85 X… Y… Z… A… B… C… R… L…

    0. Preliminary motion, as described above.
    1. Move the Z-axis only at the current feed rate to the Z position.
    2. Retract the Z-axis at the current feed rate to clear Z.

    *G86 Cycle*

    The G86 cycle is intended for boring. This cycle uses a P number for the number of seconds to
    dwell. Program G86 X… Y… Z… A… B… C… R… L… P…

    0. Preliminary motion, as described above.
    1. Move the Z-axis only at the current feed rate to the Z position.
    2. Dwell for the P number of seconds.
    3. Stop the spindle turning.
    4. Retract the Z-axis at traverse rate to clear Z.
    5. Restart the spindle in the direction it was going.

    The spindle must be turning before this cycle is used. **It is an error if:**

    * the spindle is not turning before this cycle is executed.

    *G87 Cycle*

    The G87 cycle is intended for back boring.

    Program G87 X… Y… Z… A… B… C… R… L… I… J… K…

    The situation, as shown in Figure 1, is that you have a through hole and you want to counterbore
    the bottom of hole. To do this you put an L-shaped tool in the spindle with a cutting surface on
    the UPPER side of its base. You stick it carefully through the hole when it is not spinning and
    is oriented so it fits through the hole, then you move it so the stem of the L is on the axis of
    the hole, start the spindle, and feed the tool upward to make the counterbore.  Then you stop
    the tool, get it out of the hole, and restart it.

    This cycle uses I and J numbers to indicate the position for inserting and removing the tool. I
    and J will always be increments from the X position and the Y position, regardless of the
    distance mode setting. This cycle also uses a K number to specify the position along the Z-axis
    of the controlled point top of the counterbore. The K number is a Z-value in the current
    coordinate system in absolute distance mode, and an increment (from the Z position) in
    incremental distance mode.

    0. Preliminary motion, as described above.
    1. Move at traverse rate parallel to the XY-plane to the point indicated by I and J.
    2. Stop the spindle in a specific orientation.
    3. Move the Z-axis only at traverse rate downward to the Z position.
    4. Move at traverse rate parallel to the XY-plane to the X,Y location.
    5. Start the spindle in the direction it was going before.
    6. Move the Z-axis only at the given feed rate upward to the position indicated by K.
    7. Move the Z-axis only at the given feed rate back down to the Z position.
    8. Stop the spindle in the same orientation as before.
    9. Move at traverse rate parallel to the XY-plane to the point indicated by I and J.
    10. Move the Z-axis only at traverse rate to the clear Z.
    11. Move at traverse rate parallel to the XY-plane to the specified X,Y location.
    12. Restart the spindle in the direction it was going before.

    When programming this cycle, the I and J numbers must be chosen so that when the tool is stopped
    in an oriented position, it will fit through the hole. Because different cutters are made
    differently, it may take some analysis and/or experimentation to determine appropriate values
    for I and J.

    *G88 Cycle*

    The G88 cycle is intended for boring. This cycle uses a P word, where P specifies the number of
    seconds to dwell. Program G88 X… Y… Z… A… B… C… R… L… P…

    0. Preliminary motion, as described above.
    1. Move the Z-axis only at the current feed rate to the Z position.
    2. Dwell for the P number of seconds.
    3. Stop the spindle turning.

    **Figure 1. G87 Cycle**

    The eight subfigures are labelled with the steps from the description above.

    4. Stop the program so the operator can retract the spindle manually.
    5. Restart the spindle in the direction it was going.

    *G89 Cycle*

    The G89 cycle is intended for boring. This cycle uses a P number, where P specifies the number
    of seconds to dwell. program G89 X… Y… Z… A… B… C… R… L… P…

    0. Preliminary motion, as described above.
    1. Move the Z-axis only at the current feed rate to the Z position.
    2. Dwell for the P number of seconds.
    3. Retract the Z-axis at the current feed rate to clear Z.

    """

####################################################################################################

class G90_G91:

    """**Set Distance Mode — G90 and G91**

    Interpretation of RS274/NGC code can be in one of two distance modes: absolute or incremental.

    To go into absolute distance mode, program G90. In absolute distance mode, axis numbers (X, Y,
    Z, A, B, C) usually represent positions in terms of the currently active coordinate system. Any
    exceptions to that rule are described explicitly in this Section 3.5.

    To go into incremental distance mode, program G91. In incremental distance mode, axis numbers
    (X, Y, Z, A, B, C) usually represent increments from the current values of the numbers.

    I and J numbers always represent increments, regardless of the distance mode setting. K numbers
    represent increments in all but one usage (see Section 3.5.16.8), where the meaning changes with
    distance mode.

    """

####################################################################################################

class G92_G92_1_G92_2_G92_3:

    """**3.5.18 Coordinate System Offsets — G92, G92.1, G92.2, G92.3**

    See Section 3.2.2 for an overview of coordinate systems.

    To make the current point have the coordinates you want (without motion), program G92 X…  Y… Z…
    A…  B… C… , where the axis words contain the axis numbers you want.  All axis words are
    optional, except that at least one must be used. If an axis word is not used for a given axis,
    the coordinate on that axis of the current point is not changed.

    **It is an error if:**

    * all axis words are omitted.

    When G92 is executed, the origin of the currently active coordinate system moves. To do this,
    origin offsets are calculated so that the coordinates of the current point with respect to the
    moved origin are as specified on the line containing the G92. In addition, parameters 5211 to
    5216 are set to the X, Y, Z, A, B, and C-axis offsets. The offset for an axis is the amount the
    origin must be moved so that the coordinate of the controlled point on the axis has the
    specified value.

    Here is an example. Suppose the current point is at X=4 in the currently specified coordinate
    system and the current X-axis offset is zero, then G92 x7 sets the X-axis offset to -3, sets
    parameter 5211 to -3, and causes the X-coordinate of the current point to be 7.

    The axis offsets are always used when motion is specified in absolute distance mode using any of
    the nine coordinate systems (those designated by G54 - G59.3). Thus all nine coordinate systems
    are affected by G92.

    Being in incremental distance mode has no effect on the action of G92.

    Non-zero offsets may be already be in effect when the G92 is called. If this is the case, the
    new value of each offset is A+B, where A is what the offset would be if the old offset were
    zero, and B is the old offset. For example, after the previous example, the X-value of the
    current point is 7. If G92 x9 is then programmed, the new X-axis offset is -5, which is
    calculated by [[7-9] + -3].

    To reset axis offsets to zero, program G92.1 or G92.2. G92.1 sets parameters 5211 to 5216 to
    zero, whereas G92.2 leaves their current values alone.

    To set the axis offset values to the values given in parameters 5211 to 5216, program G92.3.

    You can set axis offsets in one program and use the same offsets in another program. Program G92
    in the first program. This will set parameters 5211 to 5216. Do not use G92.1 in the remainder
    of the first program. The parameter values will be saved when the first program exits and
    restored when the second one starts up. Use G92.3 near the beginning of the second program.

    That will restore the offsets saved in the first program. If other programs are to run between
    the the program that sets the offsets and the one that restores them, make a copy of the
    parameter file written by the first program and use it as the parameter file for the second
    program.

    """

####################################################################################################

class G93_G94:

    """**Set Feed Rate Mode — G93 and G94**

    Two feed rate modes are recognized: units per minute and inverse time.  Program G94 to start the
    units per minute mode. Program G93 to start the inverse time mode.

    In units per minute feed rate mode, an F word (no, not *that* F word; we mean * feedrate*) is
    interpreted to mean the controlled point should move at a certain number of inches per minute,
    millimeters per minute, or degrees per minute, depending upon what length units are being used
    and which axis or axes are moving.

    In inverse time feed rate mode, an F word means the move should be completed in [one divided by
    the F number] minutes. For example, if the F number is 2.0, the move should be completed in half
    a minute.

    When the inverse time feed rate mode is active, an F word must appear on every line which has a
    G1, G2, or G3 motion, and an F word on a line that does not have G1, G2, or G3 is ignored. Being
    in inverse time feed rate mode does not affect G0 (rapid traverse) motions.

    **It is an error if:**

    * inverse time feed rate mode is active and a line with G1, G2, or G3 (explicitly or implicitly)
      does not have an F word.

    """

####################################################################################################

class G98_G99:

    """**Set Canned Cycle Return Level — G98 and G99**

    When the spindle retracts during canned cycles, there is a choice of how far it retracts: (1)
    retract perpendicular to the selected plane to the position indicated by the R word, or (2)
    retract perpendicular to the selected plane to the position that axis was in just before the
    canned cycle started (unless that position is lower than the position indicated by the R word,
    in which case use the R word position).

    To use option (1), program G99. To use option (2), program G98. Remember that the R word has
    different meanings in absolute distance mode and incremental distance mode.

    """

####################################################################################################

# **Input M Codes**
#
# M codes of the RS274/NGC language are shown in Table 7.

####################################################################################################

class M0_M1_M2_M30_M60:

    """**Program Stopping and Ending — M0, M1, M2, M30, M60**

    To stop a running program temporarily (regardless of the setting of the optional stop switch),
    program M0.

    To stop a running program temporarily (but only if the optional stop switch is on), program M1.

    It is OK to program M0 and M1 in MDI mode, but the effect will probably not be noticeable,
    because normal behavior in MDI mode is to stop after each line of input, anyway.

    To exchange pallet shuttles and then stop a running program temporarily (regardless of the
    setting of the optional stop switch), program M60.

    If a program is stopped by an M0, M1, or M60, pressing the cycle start button will restart the
    program at the following line.

    To end a program, program M2. To exchange pallet shuttles and then end a program, program
    M30. Both of these commands have the following effects.

    1. Axis offsets are set to zero (like G92.2) and origin offsets are set to the default (like G54).
    2. Selected plane is set to CANON_PLANE_XY (like G17).
    3. Distance mode is set to MODE_ABSOLUTE (like G90).
    4. Feed rate mode is set to UNITS_PER_MINUTE (like G94).
    5. Feed and speed overrides are set to ON (like M48).
    6. Cutter compensation is turned off (like G40).
    7. The spindle is stopped (like M5).
    8. The current motion mode is set to G_1 (like G1).
    9. Coolant is turned off (like M9).

    No more lines of code in an RS274/NGC file will be executed after the M2 or M30 command is
    executed. Pressing cycle start will start the program back at the beginning of the file.

    """

####################################################################################################

class M3_M4_M5:

    """**Spindle Control — M3, M4, M5**

    To start the spindle turning clockwise at the currently programmed speed, program M3.

    To start the spindle turning counterclockwise at the currently programmed speed, program M4.

    To stop the spindle from turning, program M5.

    It is OK to use M3 or M4 if the spindle speed is set to zero. If this is done (or if the speed
    override switch is enabled and set to zero), the spindle will not start turning.  If, later, the
    spindle speed is set above zero (or the override switch is turned up), the spindle will start
    turning. It is OK to use

    M3 or M4 when the spindle is already turning or to use M5 when the spindle is already stopped.

    """

####################################################################################################

class M6:

    """**Tool Change — M6**

    To change a tool in the spindle from the tool currently in the spindle to the tool most recently
    selected (using a T word — see Section 3.7.3), program M6. When the tool change is complete:

    * The spindle will be stopped.

    * The tool that was selected (by a T word on the same line or on any line after the previous
      tool change) will be in the spindle. The T number is an integer giving the changer slot of the
      tool (not its id).

    * If the selected tool was not in the spindle before the tool change, the tool that was in the
      spindle (if there was one) will be in its changer slot.

    * The coordinate axes will be stopped in the same absolute position they were in before the tool
      change (but the spindle may be re-oriented).

    * No other changes will be made. For example, coolant will continue to flow during the tool
      change unless it has been turned off by an M9.

    The tool change may include axis motion while it is in progress. It is OK (but not useful) to
    program a change to the tool already in the spindle. It is OK if there is no tool in the
    selected slot; in that case, the spindle will be empty after the tool change. If slot zero was
    last selected, there will definitely be no tool in the spindle after a tool change.

    """

####################################################################################################

class M7_M8_M9:

    """**Coolant Control — M7, M8, M9**

    * To turn mist coolant on, program M7.
    * To turn flood coolant on, program M8.
    * To turn all coolant off, program M9.

    It is always OK to use any of these commands, regardless of what coolant is on or off.

    """

####################################################################################################

class M48_M48:

    """**Override Control — M48 and M49**

    To enable the speed and feed override switches, program M48. To disable both switches, program
    M49. See Section 2.2.1 for more details. It is OK to enable or disable the switches when they
    are already enabled or disabled.

    """

####################################################################################################

# **Other Input Codes**

####################################################################################################

class F:

    """**Set Feed Rate — F**

    To set the feed rate, program F… . The application of the feed rate is as described in Section
    2.1.2.5, unless inverse time feed rate mode is in effect, in which case the feed rate is as
    described in Section 3.5.19.

    """

####################################################################################################

class S:

    """**Set Spindle Speed — S**

    To set the speed in revolutions per minute (rpm) of the spindle, program S… . The spindle will
    turn at that speed when it has been programmed to start turning. It is OK to program an S word
    whether the spindle is turning or not. If the speed override switch is enabled and not set at
    100%, the speed will be different from what is programmed. It is OK to program S0; the spindle
    will not turn if that is done.

    **It is an error if:**

    * the S number is negative.

    As described in Section 3.5.16.5, if a G84 (tapping) canned cycle is active and the feed and
    speed override switches are enabled, the one set at the lower setting will take effect. The
    speed and feed rates will still be synchronized. In this case, the speed may differ from what is
    programmed, even if the speed override switch is set at 100%.

    """

####################################################################################################

class T:

    """**Select Tool — T**

    To select a tool, program T…, where the T number is the carousel slot for the tool. The tool is
    not changed until an M6 is programmed (see Section 3.6.3). The T word may appear on the same
    line as the M6 or on a previous line. It is OK, but not normally useful, if T words appear on
    two or more lines with no tool change. The carousel may move a lot, but only the most recent T
    word will take effect at the next tool change. It is OK to program T0; no tool will be
    selected. This is useful if you want the spindle to be empty after a tool change.

    **It is an error if:**

    * a negative T number is used,
    * a T number larger than the number of slots in the carousel is used.

    On some machines, the carousel will move when a T word is programmed, at the same time machining
    is occurring. On such machines, programming the T word several lines before a tool change will
    save time. A common programming practice for such machines is to put the T word for the next
    tool to be used on the line after a tool change. This maximizes the time available for the
    carousel to move.

    """
