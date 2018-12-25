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

"""Module to implement a basic tool set.
"""

####################################################################################################

__all__ = [
    'Tool',
    'LatheTool',
    'ToolSet',
]

####################################################################################################

import yaml

####################################################################################################

class Tool:

    """Class to define a tool"""

    ##############################################

    def __init__(self, tool_id, offset, diameter=None, comment=None):

        self._id = tool_id
        self._tool_offset = offset
        self._tool_diameter = diameter
        self._comment = comment

        self._tool_set = None
        self._pocket = None

        self._loaded = False

    ##############################################

    @property
    def id(self):
        return self._id

    @tool_id.setter
    def id(self, value):
        self._id = str(value)

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value

    @property
    def diameter(self):
        return self._diameter

    @diameter.setter
    def diameter(self, value):
        self._diameter = float(value)

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        self._comment = str(value)

    ##############################################

    @property
    def tool_set(self):
        return self._tool_set

    @tool_set.setter
    def tool_set(self, value):
        self._tool_set = value

    @property
    def pocket(self):
        return self._pocket

    @pocket.setter
    def pocket(self, value):
        self._pocket = int(value)

    ##############################################

    @property
    def loaded(self):
        return self._loaded

    @loaded.setter
    def loaded(self, value):
        self._loaded = bool(value)

    def toggle_loaded(self):
        self._loaded = not self._loaded
        return self

    ##############################################

    def _to_dict(self, d, keys):
        for key in keys:
            d[key] = geattr(self, key)

    ##############################################

    def to_dict(self):

        keys = (
            'id',
            'tool_offset',
            'tool_diameter',
            'comment',
            'pocket',
        )

        return self._to_dict({}, keys)

####################################################################################################

class LatheTool(Tool):

    """Class to define a lathe tool"""

    ##############################################

    def __init__(self, tool_id, offset, front_angle, back_angle, orientation,
                 diameter=None, comment=None):

        super(). __init__(tool_id, offset, diameter, comment)

        self._front_angle = front_angle
        self._back_angle = back_angle
        self._orientation = orientation

    ##############################################

    @property
    def front_angle(self):
        return self._front_angle

    @front_angle.setter
    def front_angle(self, value):
        self._front_angle = float(value)

    @property
    def back_angle(self):
        return self._back_angle

    @back_angle.setter
    def back_angle(self, value):
        self._back_angle = float(value)

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = int(value)

    ##############################################

    def to_dict(self):

        d = super().to_dict()
        keys = (
            'front_angle',
            'back_angle',
            'orientation',
        )
        self._to_dict(d, keys)

        return d

####################################################################################################

class ToolSet:

    """Class to define a tool set"""

    ##############################################

    def __init__(self):

        self._tools = {} # Free pocket implementation

    ##############################################

    def __len__(self):
        return len(self._tools)

    def __iter__(self):
        return iter(self._tools.values())

    def __getitem__(self, pocket):
        return self._tools[pocket]

    ##############################################

    def remove_tool(self, pocket):
        if isinstance(pocket, Tool):
            pocket = pocket.pocket
        tool = self._tools.pop(pocket)
        tool.tool_set = None
        tool.pocket = None
        return tool

    ##############################################

    def add_tool(self, tool, pocket):
        old_tool = self.remove_tool(pocket)
        self._tools[pocket] = tool
        tool.tool_set = self
        tool.pocket = pocket
        return old_tool

    ##############################################

    def load_yaml(self, path):

        with (open(path, 'r')) as fh:
            yaml_data = yaml.load(fh.read())

        for pocket, d in yaml_data.items():
            if 'front_angle' in d:
                cls = LatheTool
            else:
                cls = Tool
            tool = cls(*d)
            self.add_tool(tool, pocket)

    ##############################################

    def write_yaml(self, path):

        data = {}
        for tool in self:
            d = tool.to_dict()
            del d['pocket']
            data[tool.pocket] = d

        yaml_data = yaml.dump(data, default_flow_style=False)
        with (open(path, 'w')) as fh:
            fh.write(yaml_data)
