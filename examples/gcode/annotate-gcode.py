#?##################################################################################################
#?#
#?# PythonicGcodeMachine - A Python G-code Toolkit
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
#r#  Annotate a G-code program
#r# ===========================
#r#
#r# For API see
#r#
#r# * :mod:`PythonicGcodeMachine.Gcode.Rs274`
#r# * :mod:`PythonicGcodeMachine.Gcode.Rs274.Ast`
#r# * :mod:`PythonicGcodeMachine.Gcode.Rs274.Parser`

####################################################################################################

from pathlib import Path

from PythonicGcodeMachine.Gcode.Rs274.Machine import GcodeMachine

####################################################################################################

#r# We build a RS-274 G-code Machine

machine = GcodeMachine()

####################################################################################################

#r# We load a G-code program

program_filename = 'mill-example-1.ngc'

programs_directory = Path(__file__).parents[1].joinpath('programs')
program_path = programs_directory.joinpath(program_filename)
with open(program_path, 'r') as fh:
    lines = fh.readlines()
    if lines[0].startswith(';'):
        lines = lines[1:]

####################################################################################################

#r# We parse the program

program = machine.parser.parse_lines(lines)

#r# We dump the annotated program

meaning_format = '  {:5}: {}'
for line in program:
    print()
    # print(line.ansi_str()) # Fixme: pyterate
    print(str(line))
    for word in line.iter_on_word():
        if word.is_valid_gcode:
            margin = ' '*9
            print(meaning_format.format(str(word), word.meaning))
            print(margin + 'Modal group: {}'.format(word.modal_group.meaning))
            print(margin + 'Execution order: {}'.format(word.execution_order.index))
        else:
            print(meaning_format.format(word.letter, word.meaning))
#o#
