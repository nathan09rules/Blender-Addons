bl_info = {
    "name": "autocomplete",
    "author": "Nathan Dsouza",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "category": "Object"
}

import re
import bpy


def build_map(script_text):
    roots = {}

    # Matches imports
    imports = re.compile(r"(?<=import\s)([\w, ]+)", re.MULTILINE).findall(script_text)
    for i in imports:
        roots[i] = i

    # Matches "var = something.something"
    pattern = re.compile(r"^\s*([a-zA-Z_]\w*)\s*=\s*([\w\.]+)", re.MULTILINE)

    for var, value in pattern.findall(script_text):
        path = value.strip().split(".")
        if len(path) > 1:
            if path[0] in roots.keys():
                roots[var] = roots[path[0]] + "." + ".".join(path[1:])

    return roots


def resolve(var, roots):
    path = var.split(".")
    if len(path) > 1:
        if path[0] in roots.keys():
            return roots[path[0]] + "." + ".".join(path[1:])
        else:
            return var
    else:
        if path[0] in roots.keys():
            return roots[path[0]]


class Autocomplete(bpy.types.Operator):
    bl_idname = "wm.auto"
    bl_label = "Autocomplete"

    running: bpy.props.BoolProperty(default=True)

    def modal(self, context, event):
        if event.type == 'ESC' and event.value == 'PRESS':
            return {'CANCELLED'}

        if event.type == 'PERIOD' and event.value == 'PRESS':
            print("PERIOD")
            script_text = bpy.context.space_data.text.as_string()
            var_map = build_map(script_text)

            space = bpy.context.space_data.text
            line = space.current_line.body
            char_index = space.current_character

            last = ""
            for i in line[char_index - 1 :: -1]:
                if i != " ":
                    last += i
                else:
                    break

            last = last[::-1]
            full_path = resolve(last, var_map)
            
            print("-" * 50)
            print("ROOT PATH:" , full_path)
            
            try:
                full = eval(full_path)
                print(dir(full))
                print("SIMLIPIED" + "-"*50)
                print([p.identifier for p in full.bl_rna.properties if not p.is_hidden])
            except AttributeError as e:
                print(e)
            except Exception as e:
                print(e)
        return {'PASS_THROUGH'}
    
    #IDK how to execute tho 
    
    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def menu_func(self, context):
    self.layout.operator("wm.auto", text="Autocomplete")

def register():
    bpy.utils.register_class(Autocomplete)
    bpy.types.TEXT_MT_text.append(menu_func)
    #auto start
    bpy.ops.wm.auto('INVOKE_DEFAULT')

def unregister():
    bpy.types.TEXT_MT_text.remove(menu_func)
    bpy.utils.unregister_class(Autocomplete)

register()