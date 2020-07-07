import bpy
from mathutils import *; from math import *
# https://discordapp.com/channels/337822736581918731/701017402908868659/721383594043506699

"""
ノードに設定されている値を、入出力ノードとして別出しする。
"""

def main():
    active_material = bpy.context.object.active_material
    node_tree = active_material.node_tree
    nodes = node_tree.nodes

    active_node = bpy.context.object.active_material.node_tree.nodes.active
    print("active_node.bl_rna:" + str(active_node.bl_rna))

    input_node_types = {
        "RGBA": "ShaderNodeRGB",
        "VALUE": "ShaderNodeValue",
        "VECTOR": "ShaderNodeNormal",
    }


    def create_input_node(node_type):
        if node_type not in input_node_types:
            return None
        node = nodes.new(input_node_types[node_type])
        return node


    output_node_types = {
        "RGBA": "ShaderNodeEmission",
    }


    def create_output_node(node_type):
        if node_type not in output_node_types:
            return None
        node = nodes.new(output_node_types[node_type])
        return node


    def set_default_output(node, value):
        node.outputs[0].default_value = value


    def connect(input, output):
        node_tree.links.new(input, output)


    def auto_connect_to_input(output, node):
        for input in node.inputs:
            if input.type == output.type:
                connect(input, output)
                return


    offset_x = 50
    offset_y = 50


    x, y = active_node.location

    # process inputs
    for i in range(len(active_node.inputs)):
        input = active_node.inputs[i]
        print("input.name:" + str(input.name))
        print("input.type:" + str(input.type))
        view_node = create_input_node(input.type)
        if view_node is None:
            continue
        set_default_output(view_node, input.default_value)
        _x = x - (view_node.width + offset_x)
        _y = y
        y -= view_node.height + offset_y
        view_node.location = Vector((_x, _y))
        output = view_node.outputs[0]
        connect(input, output)

    x, y = active_node.location
    x += active_node.width + offset_x

    # process outputs
    for i in range(len(active_node.outputs)):
        output = active_node.outputs[i]
        print("output.name:" + str(output.name))
        print("output.type:" + str(output.type))
        view_node = create_output_node(output.type)
        if view_node is None:
            continue
        _x = x
        _y = y
        y -= view_node.height + offset_y
        view_node.location = Vector((_x, _y))
        input = view_node.inputs[0]
        auto_connect_to_input(output, view_node)
        # connect(input, output)



class ExtractNodeValuesOperator(bpy.types.Operator):
    bl_idname = "object.extractnodevalues"
    bl_label = "ExtractNodeValues"

    def execute(self, context):
        main()
        return {'FINISHED'}



def register():
    bpy.utils.register_class(ExtractNodeValuesOperator)

def unregister():
    bpy.utils.unregister_class(ExtractNodeValuesOperator)

if __name__ == "__main__":
    register()
