bl_info = {
    "name": "UV Unpack Checker",
    "author": "BakedMystic3D",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > UV Unpack Checker",
    "description": "Notifies if any mesh lacks UV unwrap and allows selection of those meshes.",
    "warning": "",
    "category": "UV",
}

import bpy
from bpy.app.handlers import persistent

# ------------------------------------------------------
#    UV Check Function & Handler
# ------------------------------------------------------

def check_uv_unwrap():
    """
    Checks all mesh objects for UV layers and updates the status bar.
    """
    # Ensure context is available
    if not hasattr(bpy.context, 'window_manager'):
        return
    wm = bpy.context.window_manager
    no_uv = [obj.name for obj in bpy.data.objects if obj.type == 'MESH' and not obj.data.uv_layers]
    if no_uv:
        wm.status_text_set("Meshes without UVs: " + ", ".join(no_uv))
    else:
        wm.status_text_set("")

@persistent
def depsgraph_update_handler(dummy):
    """
    Handler called after depsgraph update.
    """
    check_uv_unwrap()

# ------------------------------------------------------
#    Operators
# ------------------------------------------------------

class UVUNCHECKER_OT_select_no_uv(bpy.types.Operator):
    """
    Selects all mesh objects without UV unwrap.
    """
    bl_idname = "uv_unpack_checker.select_no_uv"
    bl_label = "Select Meshes Without UV"
    bl_description = "Select all mesh objects that have no UV unwrap"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and not obj.data.uv_layers:
                obj.select_set(True)
        return {'FINISHED'}

# ------------------------------------------------------
#    Panels
# ------------------------------------------------------

class UVUNCHECKER_PT_panel(bpy.types.Panel):
    """
    Sidebar panel for UV Unpack Checker.
    """
    bl_label = "UV Unpack Checker"
    bl_idname = "UVUNCHECKER_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'UV Unpack Checker'

    def draw(self, context):
        layout = self.layout
        layout.operator("uv_unpack_checker.select_no_uv", icon='UV')

# ------------------------------------------------------
#    Registration
# ------------------------------------------------------

classes = [
    UVUNCHECKER_OT_select_no_uv,
    UVUNCHECKER_PT_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # Add handler for UV check
    bpy.app.handlers.depsgraph_update_post.append(depsgraph_update_handler)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    # Remove handler
    if depsgraph_update_handler in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(depsgraph_update_handler)
    # Clear status
    if hasattr(bpy.context, 'window_manager'):
        bpy.context.window_manager.status_text_set("")

# Allows script to be run directly from Blender's text editor
if __name__ == "__main__":
    register()
