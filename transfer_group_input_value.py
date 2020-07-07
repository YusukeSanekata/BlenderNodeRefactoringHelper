import bpy
from mathutils import *; from math import *
"""
ノードグループのインプット設定値を
グループ内ノードに転送する。
"""

def find_node_input(nodes):
    for node in nodes:
        if node.bl_idname == "NodeGroupInput":
            return node
    raise ValueError("No NodeGroupInput.")

# to_socket.nodeがrerouteだったら、reroute先を取得したい
def get_terminal_to_sockets(to_socket) -> []:
    if to_socket.node.bl_idname != "NodeReroute":
        return [to_socket]
    to_sockets = []
    for link in to_socket.node.outputs[0].links:
        to_sockets.extend(get_terminal_to_sockets(link.to_socket))
    return to_sockets

def transfer_output_value(output, value):
    to_sockets = []
    for link in output.links:
        from_socket = link.from_socket
        to_socket = link.to_socket
        to_sockets.extend(get_terminal_to_sockets(to_socket))
    for to_socket in to_sockets:
        to_socket.default_value = value

def main():
    node_group_instance = bpy.context.object.active_material.node_tree.nodes.active
    if node_group_instance.bl_idname != "ShaderNodeGroup":
        raise ValueError("select ShaderNodeGroup.")
    node_group_input = find_node_input(node_group_instance.node_tree.nodes)
    for socket_index, output in enumerate(node_group_input.outputs):
        if output.bl_idname == "NodeSocketVirtual":
            continue
        transfer_output_value(output, node_group_instance.inputs[socket_index].default_value)


class TransferGroupInputValueOperator(bpy.types.Operator):
    bl_idname = "object.transfergroupinputvalue"
    bl_label = "TransferGroupInputValue"

    def execute(self, context):
        main()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(TransferGroupInputValueOperator)

def unregister():
    bpy.utils.unregister_class(TransferGroupInputValueOperator)

if __name__ == "__main__":
    register()
