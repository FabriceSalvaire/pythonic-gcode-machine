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

__all__ = ['GcodeLexerError', 'GcodeLexer']

####################################################################################################

import re

try:
    import ply.lex as lexer
except ModuleNotFoundError:
    import PythonicGcodeMachine.PythonLexYacc.lex as lexer

####################################################################################################

class GcodeLexerError(ValueError):
    pass

####################################################################################################

class GcodeLexer:

    """Class to implement a RS-274 G-code lexer.

    For references, see

    * The NIST RS274NGC Interpreter — Version 3 — Appendix E. Production Rules for the RS274/NGC Language
    * http://linuxcnc.org/docs/2.7/html/gcode/overview.html

    """

    # List of token names.
    tokens = (
        'ABSOLUTE_VALUE',
        'AND',
        'ARC_COSINE',
        'ARC_SINE',
        'ARC_TANGENT',
        'COSINE',
        'DIVIDED_BY',
        'EQUAL_SIGN',
        'EXCLUSIVE_OR',
        'E_RAISED_TO',
        'FIX_DOWN',
        'FIX_UP',
        'LEFT_BRACKET',
        # 'LEFT_PARENTHESIS',
        'MINUS',
        'MODULO',
        'NATURAL_LOG_OF',
        'NON_EXCLUSIVE_OR',
        'PARAMETER_SIGN',
        'PLUS',
        'POWER',
        'RIGHT_BRACKET',
        # 'RIGHT_PARENTHESIS',
        'ROUND',
        'SINE',
        'SQUARE_ROOT',
        'TANGENT',
        'TIMES',

        'A', 'B', 'C', 'D',
        'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'P', 'Q', 'R', 'S', 'T',
        'X', 'Y', 'Z',

        'POSITIVE_INTEGER',
        'POSITIVE_REAL',
        'REAL',
        'INLINE_COMMENT',
        'EOF_COMMENT',
    )

    # Regular expression rules for simple tokens
    t_ABSOLUTE_VALUE = r'abs'
    t_AND = r'and'
    t_ARC_COSINE = r'acos'
    t_ARC_SINE = r'asin'
    t_ARC_TANGENT = r'atan'
    # t_BLOCK_DELETE = r'\/' # slash
    t_COSINE = r'cos'
    t_DIVIDED_BY = r'\/' # slash
    t_EQUAL_SIGN = r'='
    t_EXCLUSIVE_OR = r'xor'
    t_E_RAISED_TO = r'exp'
    t_FIX_DOWN = r'fix'
    t_FIX_UP = r'fup'
    t_LEFT_BRACKET = r'\['
    # t_LEFT_PARENTHESIS = r'\('
    t_MINUS = r'-'
    t_MODULO = r'mod'
    t_NATURAL_LOG_OF = r'ln'
    t_NON_EXCLUSIVE_OR = r'or'
    t_PARAMETER_SIGN = r'\#'
    t_PLUS = r'\+'
    t_POWER = r'\*\*'
    t_RIGHT_BRACKET = r'\]'
    # t_RIGHT_PARENTHESIS = r'\)'
    t_ROUND = r'round'
    t_SINE = r'sin'
    t_SQUARE_ROOT = r'sqrt'
    t_TANGENT = r'tan'
    t_TIMES = r'\*'

    t_A = r'a'
    T_B = r'b'
    t_C = r'c'
    t_D = r'd'

    t_F = r'f'
    t_G = r'g'
    t_H = r'h'
    t_I = r'i'
    t_J = r'j'
    t_K = r'k'
    t_L = r'l'
    t_M = r'm'
    t_N = r'n'

    t_P = r'p'
    t_Q = r'q'
    t_R = r'r'
    t_S = r's'
    t_T = r't'

    t_X = r'x'
    t_Y = r'y'
    t_Z = r'z'

    # def t_POSITIVE_INTEGER(self, t):
    #     r'\d+'
    #     t.value = int(t.value)
    #     return t

    # def t_POSITIVE_REAL(self, t):
    #     r'\d*\.\d+'
    #     t.value = float(t.value)
    #     return t

    def t_REAL(self, t):
        # r'((-)?((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+)))'
        r'((\+|-)?(\d+\.\d*|(\.)?\d+))'
        value = t.value
        if '.' in value:
            value = float(value)
            if value > 0:
                t.type = 'POSITIVE_REAL'
            else:
                t.type = 'REAL'
        else:
            value = int(value)
            t.type = 'POSITIVE_INTEGER'
        t.value = value
        return t

    def t_INLINE_COMMENT(self, t):
        r'\([^\)]*\)'
        value = t.value[1:-1]
        position = value.find('(')
        if position != -1:
            raise GcodeLexerError(t.lexpos + position +1)
        t.value = value
        return t

    def t_EOF_COMMENT(self, t):
        r';.*'
        t.value = t.value[1:].strip()
        return t

    # Ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    def t_error(self, t):
        'Error handling rule'
        # t.lexer.skip(1)
        # raise GcodeLexerError("Illegal character @{} '{}'".format(t.lexpos, t.value))
        raise GcodeLexerError(t.lexpos)

    ##############################################

    def __init__(self):
        self._build()

    ##############################################

    def _build(self, **kwargs):
        """Build the lexer"""
        self._lexer = lexer.lex(
            module=self,
            reflags=int(re.VERBOSE + re.IGNORECASE),
            optimize=1,
            **kwargs,
        )

    ##############################################

    def input(self, data):
        return self._lexer.input(data)

    ##############################################

    def tokenize(self, data):
        self.input(data)
        while True:
            token = self._lexer.token()
            if not token:
                break
            yield token
