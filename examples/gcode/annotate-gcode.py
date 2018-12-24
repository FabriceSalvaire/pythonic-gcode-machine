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

from PythonicGcodeMachine.Gcode.Rs274 import GcodeParser, config

####################################################################################################

program_filename = 'mill-example-1.ngc'

programs_directory = Path(__file__).parents[1].joinpath('programs')
program_path = programs_directory.joinpath(program_filename)
with open(program_path, 'r') as fh:
    lines = fh.readlines()
    if lines[0].startswith(';'):
        lines = lines[1:]

parser = GcodeParser()
program = parser.parse_lines(lines)

meaning_format = '  {:5}: {}'
for line in program:
    print()
    # print(line.ansi_str()) # Fixme: pyterate
    print(str(line))
    for word in line.iter_on_word():
        if word.letter in 'GM':
            meaning = config.gcodes[str(word)].meaning
            print(meaning_format.format(str(word), meaning))
        else:
            letter = word.letter
            meaning = config.letters[letter].meaning
            print(meaning_format.format(letter, meaning))
#o#
