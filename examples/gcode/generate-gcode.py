#?##################################################################################################
#?#
#?# PythonicGcodeMachine - @licence_header_description@
#?# Copyright (C) 2018 Fabrice Salvaire
#?#
#?# This program is free software: you can redistribute it and/or modify
#?# it under the terms of the GNU General Public License as published by
#?# the Free Software Foundation, either version 3 of the License, or
#?# (at your option) any later version.
#?#
#?# This program is distributed in the hope that it will be useful,
#?# but WITHOUT ANY WARRANTY; without even the implied warranty of
#?# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#?# GNU General Public License for more details.
#?#
#?# You should have received a copy of the GNU General Public License
#?# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#?#
#?##################################################################################################

####################################################################################################

#r# ===========================
#r#  Generate a G-code program
#r# ===========================
#r#
#r# For API see
#r#
#r# * :mod:`PythonicGcodeMachine.Gcode.Rs274`
#r# * :mod:`PythonicGcodeMachine.Gcode.Rs274.Ast`
#r# * :mod:`PythonicGcodeMachine.Gcode.Rs274.Parser`

####################################################################################################

from PythonicGcodeMachine.Gcode.Rs274 import *
from PythonicGcodeMachine.Gcode.Rs274.Ast import *

####################################################################################################

#r# Create a G-code line (block) using AST API

line = Line(deleted=False, line_number=1, comment='a G-code block')

# Push some items
# Note: order doesn't matter, see RS-274 for details
line += Word('G', 0)
line += Comment('fast move')
line += Word('X', 10)
line += Word('Y', 20)

print(line)
#o#

#r# More simpler way to pass G/M-code

a_line = Line()
a_line += 'G0'
a_line += Word('X', 10)
print(a_line)
#o#

#r# Using the G-code parser

parser = GcodeParser()

a_line = parser.parse('G0 X0 Y0')
a_line += Word('Z', 0)
print(a_line)
#o#

a_line = Line()
a_line += 'G0'

parsed_line = parser.parse('X1 Y2')
print(list(parsed_line))
first_item = parsed_line[0]
print(first_item)
a_line += parsed_line

print(a_line)
#o#

#r# Expression : the AST way

line2 = line.clone()
line2 += Word('Z', Addition(30, Multiply(Parameter(100), Cosine(30))))
print(line2)
#o#

#r# Expression : the literal way

line3 = line.clone()
line3 += Word('Z', '[30 + [#100 * cos[30]]]')
print(line3)
#o#

#r# Invalid expression

try:
    line4 = line.clone()
    line4 += Word('Z', '1 + 2]')
    print(line4)
except ValueError:
    pass

#r# Create a G-code program

program = Program()

program += line

line2.line_number = 2
line2.comment = 'using expression'
program += line2

line3.deleted = True
line3.line_number = 3
line3.comment = None
program += line3

print(program)
#o#

#r# Line cleanup tools

line = Line(deleted=False, line_number=1, comment='a G-code block')
line += 'G0'
line += Comment('fast move')
line += Word('X', 10)
line += Word('Y', 20)

print(line)
#o#

line.toggle()
print(line)
#o#

line.toggle()
line.remove_line_number()
print(line)
#o#

line.remove_comment()
print(line)
#o#
