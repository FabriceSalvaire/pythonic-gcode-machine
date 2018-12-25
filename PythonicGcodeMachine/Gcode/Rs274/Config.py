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

"""Module to implement a G-code implementation configuration and an Oriented Object API for the YAML
configuration files.

See YAML files for examples and :ref:`rs-274-reference-page`.

API implements an array interface or a dictionary interface for a table.

"""

####################################################################################################

__all__ = [
    'Config',
    'MeaningMixin',
    'ExecutionGroup',
    'ExecutionOrder',
    'Gcode',
    'GcodeSet',
    'LetterSet',
    'ModalGroup',
    'ModalGroupSet',
    'Parameter',
    'ParameterSet',
]

####################################################################################################

import yaml

####################################################################################################

def ensure_list(obj):
    if not isinstance(obj, list):
        obj = [obj]
    return obj

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
        """A comment"""
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
        """Parameter's index (table key)"""
        return self._index

    @property
    def default_value(self):
        return self._value

    ##############################################

    def __repr__(self):
        return '#{0._index}: {0._meaning}'.format(self)

####################################################################################################

class ParameterSet(YamlMixin, RstMixin):

    """Class for the table of parameters."""

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
        """G-code letter (table key)"""
        return self._letter

    ##############################################

    def __repr__(self):
        return '#{0._letter}: {0._meaning}'.format(self)

####################################################################################################

class LetterSet(YamlMixin, RstMixin):

    """Class for the table of letters."""

    GM_LETTERS = 'GM'
    AXIS_LETTERS = 'XYZABC' # 6-axis

    ##############################################

    def is_gm_letter(self, letter):
        return letter in self.GM_LETTERS

    def is_axis_letter(self, letter):
        return letter in self.AXIS_LETTERS

    ##############################################

    def is_gm_word(self, word):
        return self.is_gm_letter(word.letter)

    def is_axis_word(self, word):
        return self.is_axis_letter(word.letter)

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

    def __init__(self, gcode, meaning,
                 modal_group=None,
                 execution_order=None,
                 doc=None,
    ):

        MeaningMixin.__init__(self, meaning)
        self._gcode = str(gcode)

        # Those are set later due to the initialisation process
        self._modal_group = modal_group
        self._execution_order = execution_order
        self._doc = doc

    ##############################################

    @property
    def gcode(self):
        """G-code (table key)"""
        return self._gcode

    @property
    def modal_group(self):
        return self._modal_group

    @property
    def execution_order(self):
        return self._execution_order

    @property
    def execution_order_index(self):
        return self._execution_order.index

    @property
    def doc(self):
        return self._doc

    ##############################################

    def __str__(self):
        return self._gcode

    ##############################################

    def convert_doc(self, format):
        import pypandoc
        return pypandoc.convert_text(self.doc, 'rst', format=format)

####################################################################################################

class GcodeSet(YamlMixin, RstMixin):

    """Class for the table of G-codes."""

    ##############################################

    def __init__(self, yaml_path):

        data = self._load_yaml(yaml_path)
        self._gcodes = {}
        for gcode_txt, d in data.items():
            gcode = Gcode(gcode_txt, d['meaning'])
            self._gcodes[gcode_txt] = gcode

        self._sorted_gcodes = None

    ##############################################

    def __len__(self):
        return len(self._gcodes)

    def __iter__(self):
        return iter(self._gcodes.values())

    def __getitem__(self, code):
        return self._gcodes[code]

    def __contains__(self, code):
        return code in self._gcodes

    ##############################################

    def _sort(self):

        if self._sorted_gcodes is None:
            items = list(self)
            items.sort(key=lambda item: str(ord(item.gcode[0])*1000) + item.gcode[1:])
            self._sorted_gcodes = items
        return self._sorted_gcodes

    ##############################################

    def sorted_iter(self):
        return iter(self._sort())

    ##############################################

    def iter_on_slice(self, start, stop):

        start_index = None
        stop_index = None
        for i, item in enumerate(self._sort()):
            if item.gcode == start:
                start_index = i
            elif item.gcode == stop:
                stop_index = i
        if start_index > stop_index:
            raise ValueError('{} > {}'.format(start, stop))

        return iter(self._sorted_gcodes[start_index:stop_index+1])

    ##############################################

    def to_rst(self, path):
        self._write_rst(
            path,
            headers=('G-code', 'Meaning'),
            columns=('gcode', 'meaning'),
        )

####################################################################################################

class ExecutionGroup(MeaningMixin):

    ##############################################

    def __init__(self, index, gcodes, raw_gcodes, meaning):

        MeaningMixin.__init__(self, meaning)
        self._index = int(index)
        self._gcodes = list(gcodes)
        self._raw_gcodes = list(raw_gcodes)

    ##############################################

    @property
    def index(self):
        """Order index (table key)"""
        return self._index

    @property
    def gcodes(self):
        """G-Codes list"""
        return self._gcodes

    @property
    def raw_gcodes(self):
        """Raw G-Codes list"""
        return self._raw_gcodes

    ##############################################

    def __str__(self):
        return '#{0._index} Meaning: {0._meaning}'.format(self)

####################################################################################################

class ExecutionOrder(YamlMixin, RstMixin):

    """Class for the execution order table."""

    ##############################################

    def __init__(self, yaml_path, gcode_set):

        data = self._load_yaml(yaml_path)

        self._order = []
        count = 1
        for index, d in data.items():
            if index != count:
                raise ValueError('Unexpected index {} versus {}'.format(index, count))
            count += 1

            raw_gcodes = ensure_list(d['gcodes'])

            gcodes = []
            for gcode in raw_gcodes:
                if '-' in gcode:
                    start, stop = [int(code[1:]) for code in gcode.split('-')]
                    letter = gcode[0]
                    for i in range(start, stop+1):
                        _gcode = '{}{}'.format(letter, i)
                        gcodes.append(gcode_set[_gcode])
                else:
                    try:
                        gcode = gcode_set[gcode]
                    except KeyError:
                        if gcode != 'COMMENT':
                            raise ValueError('Invalid G-code {}'.format(gcode))
                    gcodes.append(gcode)

            group = ExecutionGroup(index, gcodes, raw_gcodes, d['meaning'])
            self._order.append(group)

            for gcode in gcodes:
                if isinstance(gcode, Gcode):
                    gcode._execution_order = group

    ##############################################

    def __len__(self):
        return len(self._order)

    def __iter__(self):
        return iter(self._order)

    def __getitem__(self, index):
        return self._order[index]

    ##############################################

    def to_rst(self, path):
        self._write_rst(
            path,
            headers=('Order', 'G-codes', 'Comment'),
            columns=('index', 'raw_gcodes', 'meaning'),
            str_gcodes=lambda item: ' '.join(item),
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
        """Group id (table key)"""
        return self._index

    @property
    def gcodes(self):
        """G-Codes list"""
        return self._gcodes

    ##############################################

    def __repr__(self):
        return '#{0._index}: ({1}) Meaning: {0._meaning}'.format(self, ' '.join([str(gcode) for gcode in self._gcodes]))

####################################################################################################

class ModalGroupSet(YamlMixin, RstMixin):

    """Class for the table of modal groups."""

    ##############################################

    def __init__(self, yaml_path, gcode_set):

        data = self._load_yaml(yaml_path)

        self._groups = {}
        for index, d in data.items():
            gcodes = ensure_list(d['gcodes'])
            gcodes = [gcode_set[gcode] for gcode in gcodes]
            group = ModalGroup(index, gcodes, d['meaning'])
            self._groups[index] = group
            for gcode in gcodes:
                gcode._modal_group = group

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
            str_gcodes=lambda gcodes: ' '.join([str(gcode) for gcode in gcodes]),
        )

####################################################################################################

class Config:

    """Class to register a G-code implementation configuration.

    An instance is build from a set of YAML files.

    """

    ##############################################

    def __init__(self,
                 execution_order,
                 gcodes,
                 letters,
                 modal_groups,
                 parameters,
    ):

        """Each argument is a path to the corresponding YAML file.

        """

        self._gcodes = GcodeSet(gcodes)
        self._execution_order = ExecutionOrder(execution_order, self._gcodes)
        self._modal_groups = ModalGroupSet(modal_groups, self._gcodes)

        # self._letters = str(letters)
        # self._parameters = str(parameters)
        self._letters = LetterSet(letters)
        self._parameters = ParameterSet(parameters)

        self._load_doc()

    ##############################################

    def _load_doc(self):

        from . import GcodeDoc as gcode_doc
        for obj in gcode_doc.__dict__.values():
            if isinstance(obj, type):
                self._load_gcode_doc_cls(obj)

    ##############################################

    def _set_gcode_doc(self, gcode, cls):
        rst_doc = cls.__doc__
        rst_doc = rst_doc.replace('\n' + ' '*4, '\n')
        self._gcodes[gcode]._doc = rst_doc

    ##############################################

    def _load_gcode_doc_cls(self, cls):

        cls_name = cls.__name__
        for letter in self._letters.GM_LETTERS:
            cls_name = cls_name.replace('_' + letter, ' ' + letter)
        cls_name = cls_name.replace('_to', '-')
        cls_name = cls_name.replace('_', '.')
        gcodes = cls_name.split(' ')
        i = 0
        while i < len(gcodes):
            gcode = gcodes[i]
            if gcode.endswith('-'):
                start = gcode[:-1]
                i += 1
                stop = gcodes[i]
                for _gcode in self._gcodes.iter_on_slice(start, stop):
                    self._set_gcode_doc(str(_gcode), cls)
            else:
                self._set_gcode_doc(gcode, cls)
            i += 1

    ##############################################

    @property
    def execution_order(self):
        """:class:`ExecutionOrder` instance"""
        return self._execution_order

    @property
    def gcodes(self):
        """:class:`GcodeSet` instance"""
        return self._gcodes

    @property
    def letters(self):
        """:class:`LetterSet` instance"""
        # if isinstance(self._letters, str):
        #     self._letters = LetterSet(self._letters)
        return self._letters

    @property
    def modal_groups(self):
        """:class:`ModalGroupSet` instance"""
        return self._modal_groups

    @property
    def parameters(self):
        """:class:`ParameterSet` instance"""
        # if isinstance(self._parameters, str):
        #     self._parameters = ParameterSet(self._parameters)
        return self._parameters
