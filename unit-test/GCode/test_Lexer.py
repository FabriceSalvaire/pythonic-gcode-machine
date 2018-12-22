####################################################################################################
#
# PythonicGCodeMachine - @licence_header_description@
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

from PythonicGCodeMachine.GCode.Lexer import GCodeLexer

####################################################################################################

class TestGCodeLexer(unittest.TestCase):

    ##############################################

    def test_gcode_lexer(self):

        lexer = GCodeLexer()

        for gcode in (
                'G0 X0 Y0 Z0',
                'g0 x0 y0 z0',
                'G0X0Y0Z0',

                'N1 G0 X0 Y0 Z0',
                'N2 G0 X1.0 Y0 Z0',
                'N3.1 G0 X1.0 Y0 Z0',

                'N3.1 G0 X1.0 Y0 Z0 ; a eof comment',
                'N3.1 (comment 1) G0 (comment 2) X1.0 (comment 3) Y0 (comment 4) Z0 ; a eof comment',
        ):
            tokens = lexer.tokenize(gcode)
            print(gcode, list(tokens))

        for gcode in (
                'G0 (comment (wrong) 2) X0',
        ):
            tokens = lexer.tokenize(gcode)
            print(gcode, list(tokens))

####################################################################################################

if __name__ == '__main__':

    unittest.main()
