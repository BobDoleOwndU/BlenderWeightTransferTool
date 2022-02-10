bl_info = {
    "name": "Weight Transfer",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy

from bpy.props import(
    StringProperty,
    BoolProperty,
    IntProperty,
    FloatProperty,
    FloatVectorProperty,
    EnumProperty,
    PointerProperty,
)

from bpy.types import(
    Panel,
    Menu,
    Operator,
    PropertyGroup,
)

################################################################
# Properties
################################################################
class WeightTransferProperties(PropertyGroup):
    obj: StringProperty(
        name = "Object",
        description = ":",
        default = "",
    )
    
    vertGroup0: StringProperty(
        name = "Target",
        description = ":",
        default = "",
    )
    
    vertGroup1: StringProperty(
        name = "Source(s)",
        description = ":",
        default = "",
    )

################################################################
# Operators
################################################################
class OBJECT_OT_WeightTransfer(Operator):
    bl_label = "Weight Transfer"
    bl_idname = "object.weight_transfer"

    def execute(self, context):
        scene = context.scene
        properties = scene.weight_transfer_properties

        obj = bpy.context.scene.objects[properties.obj]

        vertGroup0 = obj.vertex_groups[properties.vertGroup0]
        sourceGroups = properties.vertGroup1.split(',')

        for group in sourceGroups:
            if group in obj.vertex_groups:
                vertGroup1 = obj.vertex_groups[group]
            
                vg_idx = vertGroup1.index
                vs = [v for v in obj.data.vertices if vg_idx in [vg.group for vg in v.groups]]

                for v in vs:
                    vertGroup0.add([v.index], 1.0, 'REPLACE')
    
                obj.vertex_groups.remove(vertGroup1)

        print("Weights transferred to: " + vertGroup0.name)
        
        return {'FINISHED'}
    
class OBJECT_OT_ObjectSelect(Operator):
    bl_label = "Select Object"
    bl_idname = "object.object_select"
    
    def execute(self, context):
        scene = context.scene
        properties = scene.weight_transfer_properties
        
        properties.obj = bpy.context.active_object.name
        
        return{'FINISHED'}
    
class OBJECT_OT_VertGroupTargetSelect(Operator):
    bl_label = "Select Target"
    bl_idname = "object.vert_group_target_select"
    
    def execute(self, context):
        scene = context.scene
        properties = scene.weight_transfer_properties
        
        properties.vertGroup0 = bpy.context.active_bone.name
        
        return{'FINISHED'}
    
class OBJECT_OT_VertGroupSourceSelect(Operator):
    bl_label = "Select Source(s)"
    bl_idname = "object.vert_group_source_select"
    
    def execute(self, context):
        scene = context.scene
        properties = scene.weight_transfer_properties
        properties.vertGroup1 = ""
        
        selection = bpy.context.selected_bones
        
        for bone in selection:
            properties.vertGroup1 += bone.name + ','
            
        properties.vertGroup1 = properties.vertGroup1[0:len(properties.vertGroup1) - 1]
        
        return{'FINISHED'}
    
################################################################
# Panels
################################################################
class OBJECT_PT_WeightTransfer(Panel):
    bl_label = "Weight Transfer"
    bl_idname = "OBJECT_PT_weight_transfer"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Weight Transfer"
    #bl_context = "objectmode"
    
    @classmethod
    def poll(self,context):
        return context.object is not None
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        properties = scene.weight_transfer_properties
        
        layout.prop(properties, 'obj')
        layout.operator('object.object_select')
        layout.prop(properties, 'vertGroup0')
        layout.operator('object.vert_group_target_select')
        layout.prop(properties, 'vertGroup1')
        layout.operator('object.vert_group_source_select')
        layout.operator('object.weight_transfer')

################################################################
# Registration
################################################################
classes = (
    WeightTransferProperties,
    OBJECT_OT_WeightTransfer,
    OBJECT_OT_ObjectSelect,
    OBJECT_OT_VertGroupTargetSelect,
    OBJECT_OT_VertGroupSourceSelect,
    OBJECT_PT_WeightTransfer
)

def register():
    from bpy.utils import register_class
    
    for cls in classes:
        register_class(cls)
        
    bpy.types.Scene.weight_transfer_properties = PointerProperty(type=WeightTransferProperties)
    
def unregister():
    from bpy.utils import unregister_class
    
    for cls in reversed(classes):
        unregister_class(cls)
        
    del bpy.types.Scene.weight_transfer_properties
    
if __name__ == "__main__":
    register()
