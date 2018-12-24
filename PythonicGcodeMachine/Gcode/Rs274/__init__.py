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

"""Module to implement the G-code language.

See :ref:`rs-274-reference-page` for more details about the RS-274 specification.
"""

####################################################################################################

from pathlib import Path as _Path

from .Config import Config as _Config
from .Parser import GcodeParser, GcodeParserError

_data_path = _Path(__file__).parent.joinpath('data')

config = _Config(
    execution_order=_data_path.joinpath('rs274-execution-order.yaml'),
    gcodes=_data_path.joinpath('rs274-gcodes.yaml'),
    letters=_data_path.joinpath('rs274-word-starting-letter.yaml'),
    modal_groups=_data_path.joinpath('rs274-modal-groups.yaml'),
    parameters=_data_path.joinpath('rs274-default-parameter-file.yaml'),
)
