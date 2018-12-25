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

"""Module to implement a basic G-code machine.
"""

####################################################################################################

__all__ = [
    'MachineState',
]

####################################################################################################

from enum import Enum, auto

from .Coordinate import Coordinate
from .ToolSet import ToolSet

####################################################################################################

class PlaneSelection:
    XY = auto()
    XZ = auto()
    YZ = auto()

class FeedRateMode:
    UNITS_PER_MINUTE = auto()
    INVERSE_TIME = auto()

####################################################################################################

class MachineState:

    NUMBER_OF_COORDINATE_SYSTEMS = 9

    ##############################################

    def __init__(self,
                 number_of_axes,
                 is_metric=True,
    ):

        self._number_of_axes = int(number_of_axes)
        self._coordinate = Coordinate(dimension=self._number_of_axes)

        self._tool_set = ToolSet()
        self._tool = None # T

        self._is_metric = bool(is_metric)
        self._use_metric = self._is_metric # G20 inch / G21 mm
        self._use_absolut = True # G90 absolut / G91 incremental

        # G17 XY-plane selection
        # G18 XZ-plane selection
        # G19 YZ-plane selection
        self._plane = None

        # G54 G55 G56 G57 G58 G59 G59.1 G59.2 G59.3
 	self._coordinate_system = None

        self._feed_rate = 0 # F
        # G93 units per minute
        # G94 inverse time
        self._feed_rate_mode = FeedRateMode.UNITS_PER_MINUTE

        self._spindle_rate = 0 # S

        ### 4 	M0 M1 M2 M30 M60 	stopping
        ### 6 	M6 	tool change
        ### 7 	M3 M4 M5 	spindle turning
        ### 8 	M7 M8 M9 	coolant (special case: M7 and M8 may be active at the same time)
        ### 9 	M48 M49 	enable/disable feed and speed override switches
        ### 10 	G98 G99 	return mode in canned cycles
        ### 13 	G61 G61.1 G64 	path control mode

    ##############################################

    @property
    def number_of_axes(self):
        return self._number_of_axes

    @property
    def coordinate(self):
        return self._coordinate

    ##############################################

    @property
    def is_metric(self):
        return self._is_metric

    @property
    def use_metric(self):
        return self._use_metric

    @use_metric.setter
    def use_metric(self, value):
        self._use_metric = bool(value)

    ##############################################

    @property
    def use_absolut(self):
        return self._use_absolut

    @use_absolut.setter
    def use_absolut(self, value):
        self._use_absolut = bool(value)

    ##############################################

    @property
    def plane(self):
        return self._plane

    @plane.setter
    def plane(self, value):
        self._plane = PlaneSelection(value)

    ##############################################

    @property
    def coordinate_system(self):
        return self._coordinate_system

    @coordinate_system.setter
    def coordinate_system(self, value):
        _value = int(value)
        if not(1 <= _value <= self.NUMBER_OF_COORDINATE_SYSTEMS):
            raise ValueError('Invalid coordinate system {}'.format(value))
        self._coordinate_system = _value

    ##############################################

    @property
    def tool_set(self):
        return self._tool_set

    def load_tool(self, pocket):
        """Load the tool at the given carousel pocket.

        Raise ValueError if KeyError.
        """
        self._tool.toggle_loaded()
        try:
            self._tool = self._tool_set[pocket].toggle_loaded()
        except KeyError:
            raise ValueError('Invalid carousel pocket {}'.format(pocket))

    ##############################################

    @property
    def feed_rate(self):
        return self._feed_rate

    @feed_rate.setter
    def feed_rate(self, value):
        # negative feedback ?
        self._feed_rate = float(value)

    @property
    def feed_rate_mode(self):
        return self._feed_rate_mode

    @feed_rate_mode.setter
    def feed_rate_mode(self, value):
        self._feed_rate_mode = FeedRateMode(value)

    ##############################################

    @property
    def spindle_rate(self):
        return self._spindle_rate

    @spindle_rate.setter
    def spindle_rate(self, value):
        _value = float(value)
        if _value < 0:
            raise ValueError('Negative spindle rate {}'.format(value))
        self._spindle_rate = _value

