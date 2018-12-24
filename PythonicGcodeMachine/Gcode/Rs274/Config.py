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
    'ModalGroup',
    'ModalGroups',
    'ExecutionGroup',
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

class RstMixin:

    ##############################################

    def _make_rst(self, headers, columns, **kwargs):

        number_of_columns = len(headers)
        if len(columns) != number_of_columns:
            raise ValueError('Number of columns mismatch')
        number_of_lines = len(self)

        table = []
        rule = ''
        line_format = ''
        for c, title in enumerate(headers):
            if rule:
                rule += ' '
                line_format += ' '
            length = len(title)
            column = columns[c]
            str_columns = []
            if hasattr(self, 'sorted_iter'):
                it = self.sorted_iter()
            else:
                it = self
            for line_number, item in enumerate(it):
                formater = kwargs.get('str_' + column, str)
                field = getattr(item, column)
                text = formater(field)
                length = max(len(text), length)
                str_columns.append(text)
            rule += '='*length
            line_format += '{:' + str(length) + '}'
            table.append(str_columns)

        rst = ''
        rst += rule + '\n'
        rst += line_format.format(*headers) + '\n'
        rst += rule + '\n'
        for line_number in range(number_of_lines):
            fields = [table[c][line_number] for c in range(number_of_columns)]
            rst += line_format.format(*fields) + '\n'
        rst += rule + '\n'

        return rst

    ##############################################

    def _write_rst(self, path, *args, **kwargs):
        print('Write {}'.format(path))
        with open(path, 'w') as fh:
            fh.write(self._make_rst(*args, **kwargs))

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

class Parameters(YamlMixin, RstMixin):

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

    ##############################################

    def to_rst(self, path):
        self._write_rst(
            path,
            headers=('Parameter Number', 'Parameter Value', 'Comment'),
            columns=('index', 'default_value', 'meaning'),
        )

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

class Letters(YamlMixin, RstMixin):

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

    ##############################################

    def to_rst(self, path):
        self._write_rst(
            path,
            headers=('Letter', 'Meaning'),
            columns=('letter', 'meaning'),
        )

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

class Gcodes(YamlMixin, RstMixin):

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

    ##############################################

    def sorted_iter(self):

        items = list(self)
        items.sort(key=lambda item: str(ord(item.code[0])*1000) + item.code[1:])
        return items

    ##############################################

    def to_rst(self, path):
        self._write_rst(
            path,
            headers=('G-code', 'Meaning'),
            columns=('code', 'meaning'),
        )
####################################################################################################

class ExecutionGroup(MeaningMixin):

    ##############################################

    def __init__(self, index, gcodes, meaning):

        MeaningMixin.__init__(self, meaning)
        self._index = int(index)
        self._gcodes = list(gcodes)

    ##############################################

    @property
    def index(self):
        return self._index

    @property
    def gcodes(self):
        return self._gcodes

####################################################################################################

class ExecutionOrder(YamlMixin, RstMixin):

    ##############################################

    def __init__(self, yaml_path):

        data = self._load_yaml(yaml_path)
        self._order = []
        count = 1
        for index, d in data.items():
            if index != count:
                raise ValueError('Unexpected index {} versus {}'.format(index, count))
            count += 1
            gcodes = d['gcodes']
            if not isinstance(gcodes, list):
                gcodes = [gcodes]
            group = ExecutionGroup(index, gcodes, d['meaning'])
            self._order.append(group)

    ##############################################

    def __len__(self):
        return len(self._order)

    def __iter__(self):
        return iter(self._order)

    def __getitem__(self, slice_):
        return self._order[slice_]

    ##############################################

    def to_rst(self, path):
        self._write_rst(
            path,
            headers=('Order', 'G-codes', 'Comment'),
            columns=('index', 'gcodes', 'meaning'),
            str_gcodes=lambda item: ', '.join(item),
        )

####################################################################################################

class ModalGroup(MeaningMixin):

    ##############################################

    def __init__(self, index, gcodes, meaning):

        MeaningMixin.__init__(self, meaning)
        self._index = int(index)
        self._gcodes = list(gcodes)

    ##############################################

    @property
    def index(self):
        return self._index

    @property
    def gcodes(self):
        return self._gcodes

####################################################################################################

class ModalGroups(YamlMixin, RstMixin):

    ##############################################

    def __init__(self, yaml_path):

        data = self._load_yaml(yaml_path)
        self._groups = {}
        for index, d in data.items():
            gcodes = d['gcodes']
            if not isinstance(gcodes, list):
                gcodes = [gcodes]
            group = ExecutionGroup(index, gcodes, d['meaning'])
            self._groups[index] = group

    ##############################################

    def __len__(self):
        return len(self._groups)

    def __iter__(self):
        return iter(self._groups.values())

    def __getitem__(self, index):
        return self._groups[index]

    ##############################################

    def sorted_iter(self):

        items = list(self)
        items.sort(key=lambda item: item.index)
        return items

    ##############################################

    def to_rst(self, path):
        self._write_rst(
            path,
            headers=('Group', 'G-codes', 'Comment'),
            columns=('index', 'gcodes', 'meaning'),
            str_gcodes=lambda item: '(' + ', '.join(item) + ')',
        )

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
