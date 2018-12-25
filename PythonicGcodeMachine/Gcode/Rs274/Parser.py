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

"""Module to implement a RS-274 G-code parser.

Usage::

   parser = GcodeParser()
   ast_line = parser.parse(gcode_line)
   ast_program = parser.parse_lines(gcode_lines)

**Implementation**

The parser is generated automatically from the grammar defined in this class using the generator
`PLY <https://www.dabeaz.com/ply/ply.html>`_ which implement a LALR(1) parser similar to the
tools **lex** and **yacc**.

The parser construct an `abstract syntax tree (AST)
<https://en.wikipedia.org/wiki/Abstract_syntax_tree>`_ during the parsing.

User can subclass this parser to support a derived G-code flavour.

**For references, see**

* `The NIST RS274NGC Interpreter — Version 3 — Appendix E. Production Rules for the RS274/NGC Language
  <https://www.nist.gov/publications/nist-rs274ngc-interpreter-version-3>`_
* http://linuxcnc.org/docs/2.7/html/gcode/overview.html

"""

__all__ = [
    'GcodeParserError',
    'GcodeParser',
    'GcodeParserMixin',
    'GcodeGrammarMixin',
]

####################################################################################################

from pathlib import Path

# https://rply.readthedocs.io/en/latest/
from ply import yacc

from . import Ast
from .Lexer import GcodeLexer

####################################################################################################

class GcodeParserError(ValueError):
    pass

####################################################################################################

class GcodeGrammarMixin:

    """Mixin to implement the grammar.

    **Production Language for RS-274**

    The symbols in the productions are mostly standard syntax notation. Meanings of the symbols
    are:

      * ``=`` The symbol on the left of the equal sign is equivalent to the expression on the right
      * ``+`` followed by
      * ``|`` or
      * ``.`` end of production (a production may have several lines)
      * ``[]`` zero or one of the expression inside square brackets may occur
      * ``{}`` zero to many of the expression inside curly braces may occur
      * ``()`` exactly one of the expression inside parentheses must occur

    The productions are:

      * arc_tangent_combo = arc_tangent + expression + divided_by + expression .
      * binary_operation = binary_operation1 | binary_operation2 | binary_operation3 .
      * binary_operation1 = power .
      * binary_operation2 = divided_by | modulo | times .
      * binary_operation3 = and | exclusive_or | minus | non_exclusive_or | plus .
      * comment = message | ordinary_comment .
      * expression = left_bracket + real_value + { binary_operation + real_value } + right_bracket .
      * line = [block_delete] + [line_number] + {segment} + end_of_line .
      * line_number = letter_n + digit + [digit] + [digit] + [digit] + [digit] .
      * message = left_parenthesis + {white_space} + letter_m + {white_space} + letter_s +
        {white_space} + letter_g + {white_space} + comma + {comment_character} +
        right_parenthesis .
      * mid_line_letter = letter_a | letter_b | letter_c| letter_d | letter_f | letter_g | letter_h | letter_i
        | letter_j | letter_k | letter_l | letter_m | letter_p | letter_q | letter_r | letter_s | letter_t
        | letter_x | letter_y | letter_z .
      * mid_line_word = mid_line_letter + real_value .
      * ordinary_comment = left_parenthesis + {comment_character} + right_parenthesis .
      * ordinary_unary_combo = ordinary_unary_operation + expression .
      * ordinary_unary_operation =
        absolute_value | arc_cosine | arc_sine | cosine | e_raised_to |
        fix_down | fix_up | natural_log_of | round | sine | square_root | tangent .
      * parameter_index = real_value .
      * parameter_setting = parameter_sign + parameter_index + equal_sign + real_value .
      * parameter_value = parameter_sign + parameter_index .
      * real_number =
        [ plus | minus ] +
        (( digit + { digit } + [decimal_point] + {digit}) | ( decimal_point + digit + {digit})) .
      * real_value = real_number | expression | parameter_value | unary_combo .
      * segment = mid_line_word | comment | parameter_setting .
      * unary_combo = ordinary_unary_combo | arc_tangent_combo .

    """

    # Build the operation map
    # Note: sphinx show locals if not _foo
    __operation_map__ = {}
    for _cls_name in Ast.__all__:
        _cls = getattr(Ast, _cls_name)
        if hasattr(_cls, '__gcode__'):
            __operation_map__[_cls.__gcode__] = _cls

    ##############################################

    # Start symbol
    def p_line(self, p):
        '''line : DIVIDED_BY line_right
                | line_right
        '''
        if len(p) == 3:
            self._line.deleted = True
        # p[0] = self._line

    def p_line_right(self, p):
        '''line_right : line_content
                      | line_content EOF_COMMENT
        '''
        if len(p) == 3:
            self._line.comment = p[2]
        # p[0] = self._line

    def p_line_content(self, p):
        'line_content : segments'
        # p[0] = self._line

    def p_numbered_line(self, p):
        'line_content : line_number segments'
        self._line.line_number = p[1]
        # p[0] = self._line

    def p_line_number(self, p):
        '''line_number : N POSITIVE_INTEGER
                       | N POSITIVE_REAL
        '''
        p[0] = p[2]

    def p_segments(self, p):
        '''segments : segment
                    | segments segment
        '''
        if len(p) == 2:
            self._line += p[1]
        else:
            self._line += p[2]

    def p_segment(self, p):
        '''segment : mid_line_word
                   | comment
                   | parameter_setting
        '''
        p[0] = p[1]

    ##############################################

    def p_comment(self, p):
        'comment : ordinary_comment'
        # 'comment : message | ordinary_comment':
        p[0] = p[1]

    def p_ordinary_comment(self, p):
        'ordinary_comment : INLINE_COMMENT'
        p[0] = Ast.Comment(p[1], self._machine)

    # def p_message(self, p):
      # 'message : left_parenthesis + {white_space} + letter_m + {white_space} + letter_s +
      #   {white_space} + letter_g + {white_space} + comma + {comment_character} +
      #   right_parenthesis .

    ##############################################

    def p_mid_line_word(self, p):
        'mid_line_word : mid_line_letter real_value'
        p[0] = Ast.Word(p[1], p[2], self._machine)

    def p_mid_line_letter(self, p):
        # LETTER
        '''mid_line_letter : A
                           | B
                           | C
                           | D
                           | F
                           | G
                           | H
                           | I
                           | J
                           | K
                           | L
                           | M
                           | P
                           | Q
                           | R
                           | S
                           | T
                           | X
                           | Y
                           | Z
        '''
        p[0] = str(p[1])

    def p_parameter_setting(self, p):
        'parameter_setting : PARAMETER_SIGN parameter_index EQUAL_SIGN real_value'
        p[0] = Ast.ParameterSetting(p[2], p[4], self._machine)

    def p_parameter_value(self, p):
        'parameter_value : PARAMETER_SIGN parameter_index'
        p[0] = Ast.Parameter(p[2], self._machine)

    def p_parameter_index(self, p):
        'parameter_index : real_value'
        p[0] = p[1]

    def p_real_value(self, p):
        '''real_value : POSITIVE_INTEGER
                      | POSITIVE_REAL
                      | REAL
                      | expression
                      | parameter_value
                      | unary_combo
        '''
        p[0] = p[1]

    ##############################################

    def p_unary_combo(self, p):
        '''unary_combo : ordinary_unary_combo
                       | arc_tangent_combo
        '''
        p[0] = p[1]

    def p_ordinary_unary_combo(self, p):
        'ordinary_unary_combo : ordinary_unary_operation expression'
        p[0] = self.__operation_map__[p[1]](p[2])

    def p_expression(self, p):
        'expression : LEFT_BRACKET inner_expression RIGHT_BRACKET'
        p[0] = p[2]

    def p_inner_expression(self, p):
        '''inner_expression : real_value
                            | inner_expression binary_operation real_value
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = self.__operation_map__[p[2]](p[1], p[3])

    def p_arc_tangent_combo(self, p):
        # atan[1.5]/[1.0]
        'arc_tangent_combo : ARC_TANGENT expression DIVIDED_BY expression'
        p[0] = DividedBy(ArcTangent(p[2]), p[4])

    def p_ordinary_unary_operation(self, p):
        '''ordinary_unary_operation : ABSOLUTE_VALUE
                                    | ARC_COSINE
                                    | ARC_SINE
                                    | COSINE
                                    | E_RAISED_TO
                                    | FIX_DOWN
                                    | FIX_UP
                                    | NATURAL_LOG_OF
                                    | ROUND
                                    | SINE
                                    | SQUARE_ROOT
                                    | TANGENT
        '''
        p[0] = p[1]

    def p_binary_operation(self, p):
        '''binary_operation : binary_operation1
                            | binary_operation2
                            | binary_operation3
        '''
        p[0] = p[1]

    def p_binary_operation1(self, p):
        'binary_operation1 : POWER'
        p[0] = p[1]

    def p_binary_operation2(self, p):
        '''binary_operation2 : DIVIDED_BY
                             | MODULO
                             | TIMES
        '''
        p[0] = p[1]

    def p_binary_operation3(self, p):
        '''binary_operation3 : AND
                             | EXCLUSIVE_OR
                             | MINUS
                             | NON_EXCLUSIVE_OR
                             | PLUS
        '''
        p[0] = p[1]

    ##############################################

    # def p_empty(self, p):
    #     'empty :'
    #     pass

    ##############################################

    def p_error(self, p):
        raise GcodeParserError(p.lexpos)

####################################################################################################

class GcodeParserMixin:

    """Mixin to implement a RS-274 G-code parser"""

    __lexer_cls__ = GcodeLexer

    ##############################################

    def __init__(self, machine=None):

        self._machine = machine
        self._build()
        self._reset()

    ##############################################

    @property
    def machine(self):
        return self._machine

    ##############################################

    def _reset(self):
        self._line = None

    ##############################################

    def _build(self, **kwargs):

        """Build the parser"""

        self._lexer = self.__lexer_cls__()
        self.tokens = self._lexer.tokens
        self._parser = yacc.yacc(
            module=self,
            debug=False,
            optimize=1,
            tabmodule='_parsetab',
            # outputdir=Path(__file__).parent.joinpath('ply'),
        )

    ##############################################

    def parse(self, line):

        """Parse a G-code line.

        Return a :class:`PythonicGcodeMachine.Gcode.Rs274.Ast.Line` instance.
        """

        line = line.strip()

        self._line = Ast.Line(machine=self._machine)
        ast = self._parser.parse(
            line,
            lexer=self._lexer._lexer,
            # debug=True,
        )

        line = self._line
        self._reset()

        return line

    ##############################################

    def parse_lines(self, lines):

        """Parse a G-code lines

        Return a :class:`PythonicGcodeMachine.Gcode.Rs274.Ast.Program` instance.
        """

        if not isinstance(lines, (list, tuple)):
            lines = lines.split('\n')

        program = Ast.Program(machine=self._machine)
        for line in lines:
            try:
                program += self.parse(line)
            except GcodeParserError as exception:
                print('Parse Error:', line)
                raise exception

        return program

####################################################################################################

class GcodeParser(GcodeParserMixin, GcodeGrammarMixin):
    pass
