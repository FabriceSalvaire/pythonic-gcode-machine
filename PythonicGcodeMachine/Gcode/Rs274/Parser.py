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

__all__ = ['GcodeParserError', 'GcodeParser']

####################################################################################################

# https://rply.readthedocs.io/en/latest/
from ply import yacc

from .Lexer import GcodeLexer

####################################################################################################

class GcodeParserError(ValueError):
    pass

####################################################################################################

class GcodeParser:

    """Class to implement a RS-274 G-code parser.

    For references, see

    * The NIST RS274NGC Interpreter — Version 3 — Appendix E. Production Rules for the RS274/NGC Language
    * http://linuxcnc.org/docs/2.7/html/gcode/overview.html

    Production Language

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

    __lexer_cls__ = GcodeLexer

    ##############################################

    # Start symbol
    def p_line(self, p):
        '''line : DIVIDED_BY line_right
                | line_right
        '''

    def p_line_right(self, p):
        '''line_right : line_content
                      | line_content EOF_COMMENT
        '''

    def p_line_content(self, p):
        'line_content : segments'
        # p[0] = 

    def p_numbered_line(self, p):
        'line_content : line_number segments'

    def p_line_number(self, p):
        '''line_number : N POSITIVE_INTEGER
                       | N POSITIVE_REAL
        '''

    def p_segments(self, p):
        '''segments : segment
                    | segments segment
        '''

    def p_segment(self, p):
        '''segment : mid_line_word
                   | comment
                   | parameter_setting
        '''

    ##############################################

    def p_comment(self, p):
        'comment : ordinary_comment'
          # 'comment : message | ordinary_comment':

    def p_ordinary_comment(self, p):
        'ordinary_comment : INLINE_COMMENT'

    # def p_message(self, p):
      # 'message : left_parenthesis + {white_space} + letter_m + {white_space} + letter_s +
      #   {white_space} + letter_g + {white_space} + comma + {comment_character} +
      #   right_parenthesis .

    ##############################################

    def p_mid_line_word(self, p):
        'mid_line_word : mid_line_letter real_value'

    def p_mid_line_letter(self, p):
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

    def p_parameter_setting(self, p):
        'parameter_setting : PARAMETER_SIGN parameter_index EQUAL_SIGN real_value'

    def p_parameter_value(self, p):
        'parameter_value : PARAMETER_SIGN parameter_index'

    def p_parameter_index(self, p):
        'parameter_index : real_value'

    def p_real_value(self, p):
        '''real_value : POSITIVE_INTEGER
                      | POSITIVE_REAL
                      | REAL
                      | expression
                      | parameter_value
                      | unary_combo
        '''

    ##############################################

    def p_unary_combo(self, p):
        '''unary_combo : ordinary_unary_combo
                       | arc_tangent_combo
        '''

    def p_ordinary_unary_combo(self, p):
        'ordinary_unary_combo : ordinary_unary_operation expression'

    def p_expression(self, p):
        'expression : LEFT_BRACKET inner_expression RIGHT_BRACKET'

    def p_inner_expression(self, p):
        '''inner_expression : real_value
                            | inner_expression binary_operation real_value
        '''

    def p_arc_tangent_combo(self, p):
        # atan[1.5]/[1.0]
        'arc_tangent_combo : ARC_TANGENT expression DIVIDED_BY expression'

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

    def p_binary_operation(self, p):
        '''binary_operation : binary_operation1
                            | binary_operation2
                            | binary_operation3
        '''

    def p_binary_operation1(self, p):
        'binary_operation1 : POWER'

    def p_binary_operation2(self, p):
        '''binary_operation2 : DIVIDED_BY
                             | MODULO
                             | TIMES
        '''

    def p_binary_operation3(self, p):
        '''binary_operation3 : AND
                             | EXCLUSIVE_OR
                             | MINUS
                             | NON_EXCLUSIVE_OR
                             | PLUS
        '''

    ##############################################

    # def p_empty(self, p):
    #     'empty :'
    #     pass

    ##############################################

    def p_error(self, p):
        raise GcodeParserError(p.lexpos)

    ##############################################

    def __init__(self):
        self._build()

    ##############################################

    def _build(self, **kwargs):
        """Build the parser"""
        self._lexer = self.__lexer_cls__()
        self.tokens = self._lexer.tokens
        self._parser = yacc.yacc(
            module=self,
            # debug=True,
            optimize=0,
        )

    ##############################################

    def parse(self, line):
        line = line.strip()
        ast = self._parser.parse(
            line,
            lexer=self._lexer._lexer,
            # debug=True,
        )
