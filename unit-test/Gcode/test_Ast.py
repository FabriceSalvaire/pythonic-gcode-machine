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

####################################################################################################

import math
import unittest

####################################################################################################

from PythonicGcodeMachine.Gcode.Rs274.Ast import *

####################################################################################################

class TestAst(unittest.TestCase):

    ##############################################

    def test_basic(self):

        # program = Program()

        word = Word('G', 0)
        self.assertEqual(str(word), 'G0')
        word = Word('g', 0)
        self.assertEqual(str(word), 'G0')
        word = Word('G', 1.0)
        self.assertEqual(str(word), 'G1.0')

        line = Line()
        line.push(Word('G', 1))
        self.assertEqual(str(line), 'G1')
        line.comment = 'a comment'
        self.assertEqual(str(line), 'G1 ; a comment')
        line.line_number = 1
        self.assertEqual(str(line), 'N1 G1 ; a comment')
        line.line_number = 1.1
        self.assertEqual(str(line), 'N1.1 G1 ; a comment')
        line.deleted = True
        self.assertEqual(str(line), r'\ N1.1 G1 ; a comment')

        line = Line()
        for value, letter in enumerate('GXYZ'):
            line.push(Word(letter, value))
        self.assertEqual(str(line), 'G0 X1 Y2 Z3')

        line = Line()
        for value, letter in enumerate('GXYZ'):
            line += Word(letter, value)
        self.assertEqual(str(line), 'G0 X1 Y2 Z3')

        line.push(ParameterSetting(1, 1.2))
        self.assertEqual(str(line), 'G0 X1 Y2 Z3 #1=1.2')

    ##############################################

    def test_expression(self):

        expr = Cosine(45)
        self.assertEqual(str(expr), 'cos[45]')
        self.assertEqual(float(expr), math.cos(math.radians(45)))

        self.assertEqual(str(Addition(1, 2)), '[1 + 2]')

        expr = Addition(1, Subtraction(3, 4))
        self.assertEqual(str(expr), '[1 + [3 - 4]]')
        self.assertEqual(float(expr), 1 + (3 - 4))

####################################################################################################

if __name__ == '__main__':

    unittest.main()
