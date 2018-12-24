####################################################################################################

"""Example to show how to annote a G-code program.
"""

####################################################################################################

from pathlib import Path

from PythonicGcodeMachine.Gcode.Rs274 import GcodeParser, gcodes, letters

####################################################################################################

program_filename = 'mill-example-1.ngc'

programs_directory = Path(__file__).parent.joinpath('programs')
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
    print(line.ansi_str())
    for word in line.iter_on_word():
        if word.letter in 'GM':
            meaning = gcodes[str(word)].meaning
            print(meaning_format.format(str(word), meaning))
        else:
            letter = word.letter
            meaning = letters[letter].meaning
            print(meaning_format.format(letter, meaning))
