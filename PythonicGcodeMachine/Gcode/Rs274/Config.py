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
    'Parameter',
    'Parameters',
    'Letters',
    'Gcode',
    'Gcodes',
    'ModalGroups',
    'ExecutionOrder',
]

####################################################################################################

import yaml

####################################################################################################

class YamlMixin:
    def _load_yaml(self, yaml_path):
        with open(yaml_path, 'r') as fh:
            data = yaml.load(fh.read())
        return data

####################################################################################################

class MeaningMixin:

    ##############################################

    def __init__(self, meaning):
        self._meaning = str(meaning)

    ##############################################

    @property
    def meaning(self):
        return self._meaning

####################################################################################################

class Parameter(MeaningMixin):

    ##############################################

    def __init__(self, index, meaning, value):

        MeaningMixin.__init__(self, meaning)
        self._index = int(index)
        self._value = float(value)

    ##############################################

    @property
    def index(self):
        return self._index

    @property
    def default_value(self):
        return self._value

####################################################################################################

class Parameters(YamlMixin):

    ##############################################

    def __init__(self, yaml_path):

        data = self._load_yaml(yaml_path)
        self._parameters = {}
        for index, d in data.items():
            parameter = Parameter(index, d['meaning'], d['value'])
            self._parameters[index] = parameter

    ##############################################

    def __len__(self):
        return len(self._parameters)

    def __iter__(self):
        return iter(self._parameters.values())

    def __getitem__(self, index):
        return self._parameters[index]

####################################################################################################

class Letter(MeaningMixin):

    ##############################################

    def __init__(self, letter, meaning):

        MeaningMixin.__init__(self, meaning)
        self._letter = str(letter)

    ##############################################

    @property
    def letter(self):
        return self._letter

####################################################################################################

class Letters(YamlMixin):

    ##############################################

    def __init__(self, yaml_path):

        data = self._load_yaml(yaml_path)
        self._letters = {}
        for letter, d in data.items():
            self._letters[letter] = Letter(letter, d['meaning'])

    ##############################################

    def __len__(self):
        return len(self._letters)

    def __iter__(self):
        return iter(self._letters.values())

    def __getitem__(self, letter):
        return self._letters[letter]

####################################################################################################

class Gcode(MeaningMixin):

    ##############################################

    def __init__(self, code, meaning):

        MeaningMixin.__init__(self, meaning)
        self._code = str(code)

    ##############################################

    @property
    def code(self):
        return self._code

####################################################################################################

class Gcodes(YamlMixin):

    ##############################################

    def __init__(self, yaml_path):

        data = self._load_yaml(yaml_path)
        self._gcodes = {}
        for code, d in data.items():
            gcode = Gcode(code, d['meaning'])
            self._gcodes[code] = gcode

    ##############################################

    def __len__(self):
        return len(self._gcodes)

    def __iter__(self):
        return iter(self._gcodes.values())

    def __getitem__(self, code):
        return self._gcodes[code]

####################################################################################################

class ExecutionOrder(YamlMixin):

    ##############################################

    def __init__(self, yaml_path):

        data = self._load_yaml(yaml_path)
        self._order = []
        count = 1
        for index, gcodes in data.items():
            if index != count:
                raise ValueError('Unexpected index {} versus {}'.format(index, count))
            count += 1
            if not isinstance(gcodes, list):
                gcodes = list(gcodes)
            self._order.append(gcodes)

    ##############################################

    def __len__(self):
        return len(self._order)

    def __iter__(self):
        return iter(self._order.values())

    def __getitem__(self, slice_):
        return self._order[slice_]

####################################################################################################

class ModalGroups(YamlMixin):

    ##############################################

    def __init__(self, yaml_path):

        data = self._load_yaml(yaml_path)
        self._groups = {}
        for index, gcodes in data.items():
            self._groups[index] = list(gcodes)

    ##############################################

    def __len__(self):
        return len(self._groups)

    def __iter__(self):
        return iter(self._groups.values())

    def __getitem__(self, index):
        return self._groups[index_]

