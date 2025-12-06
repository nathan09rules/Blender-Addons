bl_info = {
    "name": "autocomplete",
    "author": "Nathan Dsouza",
    "version": (1,0,0),
    "blender": (5,0,0),
    "category": "Object"
}

import bpy

class ObjectX(bpy.types.Operator):
    bl_idname = "object.move_x"
    bl_label = "Move X by One"
    bl_options = {'REGISTER' , 'UNDO'}
    
    def execute(self ,context):
        scene = context.scene
        for obj in scene.objects:
            obj.location.x += 1.0
        
        return {'FINISHED'}

def menu_func(self , context):
    self.layout.operator(ObjectX.bl_idname)

def register():
    bpy.utils.register_class(ObjectX)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(ObjectX)

if __name__ == "__main__":
    register()