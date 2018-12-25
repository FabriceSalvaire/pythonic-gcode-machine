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

"""Module to implement a basic G-code machine.
"""

####################################################################################################

__all__ = [
    'GcodeMachine',
]

####################################################################################################

from pathlib import Path as Path

from .Config import Config
from .Parser import GcodeParser, GcodeParserError

####################################################################################################

class GcodeMachine:

    PARSER_CLS = GcodeParser

    GM_LETTERS = 'GM'

    ##############################################

    def __init__(self):

        self._config = None
        self.load_config()

        self._parser = None
        self.setup_parser()

    ##############################################

    def load_config(self):

        data_path = Path(__file__).parent.joinpath('data')
        self._config = Config(
            execution_order=data_path.joinpath('rs274-execution-order.yaml'),
            gcodes=data_path.joinpath('rs274-gcodes.yaml'),
            letters=data_path.joinpath('rs274-word-starting-letter.yaml'),
            modal_groups=data_path.joinpath('rs274-modal-groups.yaml'),
            parameters=data_path.joinpath('rs274-default-parameter-file.yaml'),
        )

    ##############################################

    def setup_parser(self):

        self._parser = self.PARSER_CLS(machine=self)

    ##############################################

    @property
    def config(self):
        return self._config

    @property
    def parser(self):
        return self._parser

    ##############################################

    def reset():
        pass

    ##############################################

    def is_gm_letter(self, letter):
        return letter in self.GM_LETTERS

    ##############################################

    def is_gm_word(self, word):
        return self.is_gm_letter(word.letter)
