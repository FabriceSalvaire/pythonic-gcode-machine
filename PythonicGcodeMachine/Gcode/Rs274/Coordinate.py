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

"""Module to implement a machine coordinate.
"""

####################################################################################################

__all__ = [
    'Coordinate',
]

####################################################################################################

import numpy as np

####################################################################################################

class Coordinate:

    ##############################################

    def __init__(self, *args, dimension=None):

        if args:
            self._v = numpy.array(args)
        else:
            self._v = numpy.zeros(dimension)

    ##############################################

    def clone(self):
        return self.__class__(self._v)

    ##############################################

    @property
    def dimension(self):
        return self._v.shape[0]

    ##############################################

    def __len__(self):
        return self.dimension

    def __iter__(self):
        return iter(self._v)

    def __getitem__(self, slice_):
        return self._v[slice_]

    ##############################################

    def set(self, v):
        if isintance(self, Coordinate):
            self._v = self._v
        else:
            self._v = v

    ##############################################

    def __eq__(self, v):
        return self._v == self._v

    ##############################################

    def __iadd__(self, v):
        self._v += self._v
        return self

    ##############################################

    def __isub__(self, v):
        self._v -= self._v
        return self
