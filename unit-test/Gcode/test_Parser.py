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

####################################################################################################

import unittest

####################################################################################################

from PythonicGcodeMachine.Gcode.Rs274.Lexer import GcodeLexer, GcodeLexerError
from PythonicGcodeMachine.Gcode.Rs274.Parser import GcodeParser, GcodeParserError

####################################################################################################

def print_rule():
    print()
    print('#'*100)
    print()


####################################################################################################

class TestGcodeLexer(unittest.TestCase):

    ##############################################

    def test_gcode_lexer(self):

        print_rule()

        lexer = GcodeLexer()

        for gcode in (
                'G0 X0 Y0 Z0',
                'g0 x0 y0 z0',
                'G0X0Y0Z0',

                r'/ G0 X0 Y0 Z0',

                'N1 G0 X0 Y0 Z0',
                'N2 G0 X1.0 Y0 Z0',
                'N3.1 G0 X1.0 Y0 Z0',

                'N3.1 G0 X1.0 Y0 Z0 ; a eof comment',
                'N3.1 (comment 1) G0 (comment 2) X1.0 (comment 3) Y0 (comment 4) Z0 ; a eof comment',

                '#3=1. G0 X [ 1 + acos[0] - [#3 ** [4.0/2]]]'
        ):
            print()
            print(gcode)
            try:
                tokens = lexer.tokenize(gcode)
                print(list(tokens))
            except GcodeLexerError as exception:
                position, = exception.args
                print(' ' * position + '^')
                print('Lexer Error')
                raise exception

        for gcode in (
                'G0 (comment (wrong) 2) X0',
        ):
            with self.assertRaises(GcodeLexerError):
                list(lexer.tokenize(gcode))

####################################################################################################

class TestGcodeParser(unittest.TestCase):

    ##############################################

    def test_gcode_parser(self):

        print_rule()

        parser = GcodeParser()

        for gcode in (
                'G0 X0 Y0 Z0',
                'g0 x0 y0 z0',
                'G0X0Y0Z0',

                r'/ G0 X0 Y0 Z0',

                'N1 G0 X0 Y0 Z0',
                'N2 G0 X1.0 Y0 Z0',
                'N3.1 G0 X1.0 Y0 Z0',

                'N3.1 G0 X1.0 Y0 Z0 ; a eof comment',
                'N3.1 (comment 1) G0 (comment 2) X1.0 (comment 3) Y0 (comment 4) Z0 ; a eof comment',

                '#3=1. G0 X#3 Y0'
                'G0 #3=1. X#3 Y0'

                '#3=1. G0 X [ 1 + acos[0] - [#3 ** [4.0/2]]]'
        ):
            print()
            print(gcode)
            try:
                parser.parse(gcode)
            except GcodeParserError as exception:
                position, = exception.args
                print(' ' * position + '^')
                print('Parser Error')
                raise exception

        # for gcode in (
        #         'G0 (comment (wrong) 2) X0',
        # ):
        #     with self.assertRaises(GcodeLexerError):
        #         list(lexer.tokenize(gcode))

####################################################################################################

if __name__ == '__main__':

    unittest.main()
