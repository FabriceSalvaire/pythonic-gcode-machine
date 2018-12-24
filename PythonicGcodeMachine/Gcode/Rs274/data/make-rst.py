#! /usr/bin/env python3

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

"""Script to generate rST files.

"""

####################################################################################################

import pathlib

from PythonicGcodeMachine.Gcode.Rs274 import config

####################################################################################################

source_path = pathlib.Path(__file__).absolute().parents[4]
print('Source:', source_path)
rst_path = source_path.joinpath('doc', 'sphinx', 'source', 'gcode-reference', 'rs-274')
print('rST:', rst_path)

config.execution_order.to_rst(rst_path.joinpath('execution_order.rst'))
config.gcodes.to_rst(rst_path.joinpath('gcodes.rst'))
config.letters.to_rst(rst_path.joinpath('letters.rst'))
config.modal_groups.to_rst(rst_path.joinpath('modal_groups.rst'))
config.parameters.to_rst(rst_path.joinpath('parameters.rst'))
