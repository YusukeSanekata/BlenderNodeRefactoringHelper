import bpy
from . import node_view, transfer_group_input_value
from mathutils import *; from math import *

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "NodeRefactoringHelper",
    "author": "Yusuke Sanekata",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic",
}


class NodeRefactoringHelperUIPanel(bpy.types.Panel):
    bl_label = "NodeRefactoringHelper"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.transfergroupinputvalue")
        layout.operator("object.extractnodevalues")

classes = [
    NodeRefactoringHelperUIPanel,
]


def register():
    node_view.register()
    transfer_group_input_value.register()
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    node_view.unregister()
    transfer_group_input_value.unregister()
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
