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

"""Module to implement an AST for RS-274 G-code.
"""

####################################################################################################

__all__ = [
    'Program',
    'LineItem',
    'Line',
    'Comment',
    'Word',
    'RealValue',
    'ParameterMixin',
    'ParameterSetting',
    'Parameter',
    'UnaryOperation',
    'AbsoluteValue',
    'ArcCosine',
    'ArcSine',
    'ArcTangent',
    'Cosine',
    'ERaisedTo',
    'FixDown',
    'FixUp',
    'NaturalLogOf',
    'Round',
    'Sine',
    'SquareRoot',
    'Tangent',
    'BinaryOperation',
    'Power',
    'DividedBy',
    'Modulo',
    'Times',
    'And',
    'ExclusiveOr',
    'Minus',
    'NonExclusiveOr',
    'Plus',
]

####################################################################################################

import math

####################################################################################################

class Program:

    """Class to implement a G-code program

    Usage::

        program = Program()
        program += line
        str(program)

    """

    ##############################################

    def __init__(self):
        self._lines = []

    ##############################################

    def push(self, line):
        self._lines.append(line)

    def __iadd__(self, item):
        self.push(item)
        return self

    ##############################################

    def __len__(self):
        return len(self._lines)

    def __iter__(self):
        return iter(self._lines)

    def __getitem__(self, _slice):
        return self._lines[_slice]

    def iter_on_not_deleted(self):
        for line in self._lines:
            if line:
                yield line

    ##############################################

    def __repr__(self):

        text = 'Program(\n'
        for line in self:
            text += repr(line) + '\n'
        text += ')\n'

        return text

    ##############################################

    def __str__(self):
        return '\n'.join(map(str, self))

####################################################################################################

class LineItem:
    pass

####################################################################################################

class Line:

    """Class to implement a G-code line

    Usage::

        line = Line(def=False, line_number=1, comment='a comment')
        line += Word('G', 0)
        line += Comment('move')
        line += Word('X', 10)
        line += Comment('Y value')
        line += Word('Y', 20)
        line += ParameterSetting('1', 1.2)
        str(line)

    """

    ##############################################

    def __init__(self, deleted=False, line_number=None, comment=None):

        self.deleted = deleted
        self.line_number = line_number
        self.comment = comment

        self._items = []

    ##############################################

    @property
    def deleted(self):
        return self._deleted

    @deleted.setter
    def deleted(self, value):
        self._deleted = bool(value)

    @property
    def line_number(self):
        return self._line_number

    @line_number.setter
    def line_number(self, value):
        if value is not None:
            value = float(value)
            if value.is_integer():
                value = int(value)
        self._line_number = value

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        if value is not None:
            self._comment = str(value)
        else:
            self._comment = None

    ##############################################

    def push(self, item):
        if isinstance(item, LineItem):
            self._items.append(item)
        else:
            raise ValueError

    def __iadd__(self, item):
        self.push(item)
        return self

    ##############################################

    def __bool__(self):
        return not self._deleted

    ##############################################

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, _slice):
        return self._items[_slice]

    ##############################################

    def __repr__(self):

        items = []
        if not self:
            items.append('Deleted')
        items += list(map(repr, self))
        if self._comment:
            items.append(self._comment)

        return 'Line{}'.format(self, items)

    ##############################################

    def __str__(self):

        line = ''
        if not self:
            line += r'\ '
        if self._line_number:
            line += 'N{} '.format(self._line_number)
        line += ' '.join(map(str, self))
        if self._comment:
            line += ' ; ' + self._comment

        return line

####################################################################################################

class Comment(LineItem):

    ##############################################

    def __init__(self, text):
        self.set(text)

    ##############################################

    def set(self, text):
        if '(' in text:
            raise ValueError('Comment cannot contains a "("')
        self._text = str(text)

    ##############################################

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self.set(value)

    ##############################################

    def __repr__(self):
        return 'Comment({0._text})'.format(self)

    def __str__(self):
        return '({0._text})'.format(self)

####################################################################################################

class Word(LineItem):

    LETTERS = (
        'A', 'B', 'C', 'D',
        'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', # 'N',
        'P', 'Q', 'R', 'S', 'T',
        'X', 'Y', 'Z',
    )

    ##############################################

    def __init__(self, letter, value):
        self.letter = letter
        self.value = value

    ##############################################

    @property
    def letter(self):
        return self._letter

    @letter.setter
    def letter(self, value):
        value = str(value).upper()
        if value not in self.LETTERS:
            raise ValueError
        self._letter = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        # float expression ...
        self._value = value

    ##############################################

    def __repr__(self):
        return 'Word({0._letter} {0._value})'.format(self)

    def __str__(self):
        return '{0._letter}{0._value}'.format(self)

####################################################################################################

class RealValue:
    pass

####################################################################################################

class ParameterMixin:

    ##############################################

    def __init__(self, parameter):
        self.parameter = parameter

    ##############################################

    @property
    def parameter(self):
        return self._parameter

    @parameter.setter
    def parameter(self, value):
        try:
            value = int(value)
        except ValueError:
            value = str(value)
        self._parameter = value

####################################################################################################

class ParameterSetting(LineItem, ParameterMixin):

    ##############################################

    def __init__(self, parameter, value):
        ParameterMixin.__init__(self, parameter)
        self.value = value

    ##############################################
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        # float expression ...
        self._value = value

    ##############################################

    def __repr__(self):
        return 'ParameterSetting({0._parameter} = {0._value})'.format(self)

    def __str__(self):
        return '#{0._parameter}={0._value}'.format(self)

####################################################################################################

class Parameter(RealValue, ParameterMixin):

    ##############################################

    def __init__(self, parameter):
        ParameterMixin.__init__(self, parameter)

    ##############################################

    def __repr__(self):
        return 'Parameter({0._parameter})'.format(self)

    def __str__(self):
        return '#{0._parameter}'.format(self)

####################################################################################################

class UnaryOperation(RealValue):

    __function__ = None
    __gcode__ = None

    ##############################################

    def __init__(self, arg):
        self.arg = arg

    ##############################################

    @property
    def arg(self):
        return self._arg

    @arg.setter
    def arg(self, value):
        self._arg = value

    ##############################################

    def float(self):
        return self.__function__(float(self._arg))

    ##############################################

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, repr(self._arg))

    ##############################################

    def __str__(self):
        return '{0.__gcode__}[{0._arg}]'.format(self)

####################################################################################################

class AbsoluteValue(UnaryOperation):
    __function__ = abs
    __gcode__ = 'abs'

class ArcCosine(UnaryOperation):
    __function__ = lambda x: math.acos(math.radians(x))
    __gcode__ = 'acos'

class ArcSine(UnaryOperation):
    __function__ = lambda x: math.degrees(math.asin(x))
    __gcode__ = 'asin'

class ArcTangent(UnaryOperation):
    __function__ = lambda x: math.degrees(math.atan(x))
    __gcode__ = 'atan'

class Cosine(UnaryOperation):
    __function__ = lambda x: math.degrees(math.cos(x))
    __gcode__ =  'cos'

class ERaisedTo(UnaryOperation):
    __function__ = math.exp
    __gcode__ = 'exp'

class FixDown(UnaryOperation):
    __function__ = math.ceil
    __gcode__ = 'fix'

class FixUp(UnaryOperation):
    __function__ = math.floor
    __gcode__ = 'fup'

class NaturalLogOf(UnaryOperation):
    __function__ = math.log
    __gcode__ = 'ln'

class Round(UnaryOperation):
    __function__ = round
    __gcode__ =  'round'

class Sine(UnaryOperation):
    __function__ = lambda x: math.sin(math.radians(x))
    __gcode__ = 'sin'

class SquareRoot(UnaryOperation):
    __function__ = math.sqrt
    __gcode__ = 'sqrt'

class Tangent(UnaryOperation):
    __function__ = lambda x: ath.tan(math.radians(x))
    __gcode__ = 'tan'

####################################################################################################

class BinaryOperation(RealValue):

    __function__ = None
    __gcode__ = None

    ##############################################

    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    ##############################################

    @property
    def arg1(self):
        return self._arg1

    @arg1.setter
    def arg1(self, value):
        self._arg1 = value

    @property
    def arg2(self):
        return self._arg2

    @arg2.setter
    def arg2(self, value):
        self._arg2 = value

    ##############################################

    def float(self):
        return self.__function__(float(self._arg1), float(self._arg2))

    ##############################################

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, repr(self._arg))

    ##############################################

    def __str__(self):
        return '[{0._arg1} {0.__gcode__} {0._arg2}]'.format(self)

####################################################################################################

class Power(BinaryOperation):
    __function__ = lambda a, b: a**b
    __gcode__ = '**'

class DividedBy(BinaryOperation):
    __function__ = lambda a, b: a / b
    __gcode__ = '/'

class Modulo(BinaryOperation):
    __function__ = lambda a, b: a % b
    __gcode__ = 'mod'

class Times(BinaryOperation):
    __function__ = lambda a, b: a * b
    __gcode__ =  '*'

class And(BinaryOperation):
    __function__ = lambda a, b: a & b
    __gcode__ = 'and'

class ExclusiveOr(BinaryOperation):
    __function__ = lambda a, b: a ^ b
    __gcode__ = 'xor'

class Minus(BinaryOperation):
    __function__ = lambda a, b: a - b
    __gcode__ = '-'

class NonExclusiveOr(BinaryOperation):
    __function__ = lambda a, b: a | b
    __gcode__ = 'or'

class Plus(BinaryOperation):
    __function__ = lambda a, b: a + b
    __gcode__ = '+'
