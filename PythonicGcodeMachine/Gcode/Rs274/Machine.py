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

"""
"""

####################################################################################################

__all__ = [
    'Config',
    'Parameter',
    'Parameters',
    'Letters',
    'Gcode',
    'Gcodes',
    'ModalGroups',
    'ExecutionOrder',
]

####################################################################################################

####################################################################################################

class Config:

    ##############################################

    def __init__(self,
                 execution_order,
                 gcodes,
                 letters,
                 modal_groups,
                 parameters,
    ):

        self._execution_order = str(execution_order)
        self._gcodes = str(gcodes)
        self._letters = str(letters)
        self._modal_groups = str(modal_groups)
        self._parameters = str(parameters)

    ##############################################

    @property
    def execution_order(self):
        if isinstance(self._execution_order, str):
            self._execution_order = ExecutionOrder(self._execution_order)
        return self._execution_order

    @property
    def gcodes(self):
        if isinstance(self._gcodes, str):
            self._gcodes = Gcodes(self._gcodes)
        return self._gcodes

    @property
    def letters(self):
        if isinstance(self._letters, str):
            self._letters = Letters(self._letters)
        return self._letters

    @property
    def modal_groups(self):
        if isinstance(self._modal_groups, str):
            self._modal_groups = ModalGroups(self._modal_groups)
        return self._modal_groups

    @property
    def parameters(self):
        if isinstance(self._parameters, str):
            self._parameters = Parameters(self._parameters)
        return self._parameters
