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

#r# ===============
#r#  Query G-codes
#r# ===============
#r#
#r# For API see
#r#
#r# * :mod:`PythonicGcodeMachine.Gcode.Rs274`
#r# * :mod:`PythonicGcodeMachine.Gcode.Rs274.Config`
#r# * :mod:`PythonicGcodeMachine.Gcode.Rs274.Machine`

####################################################################################################

from pathlib import Path

from PythonicGcodeMachine.Gcode.Rs274.Machine import GcodeMachine

####################################################################################################

#r# We build a RS-274 G-code Machine

machine = GcodeMachine()

####################################################################################################

#r# We get G-code information

gcode = machine.config.gcodes['G0']

print('Modal group:', gcode.modal_group)
print('Execution order:', gcode.execution_order)
#o#

print('\nreStructuredText doc:\n')
print(gcode.doc)
#o#

#r# Convert the reStructuredText doc using `pypandoc <https://github.com/bebraw/pypandoc>`_ and
#r# `Pandoc <https://pandoc.org>`_

try:
    print('\nMarkdown doc:')
    print(gcode.convert_doc('md'))
except (ImportError, RuntimeError):
    pass
#o#

try:
    print('\nHTML doc:')
    print(gcode.convert_doc('html5'))
except (ImportError, RuntimeError):
    pass
#o#
