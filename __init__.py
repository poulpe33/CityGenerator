bl_info = {
    "name": "City Generator",
    "author": "Guillaume Dauphin & Antoine Dujardin",
    "category": "Add Mesh"
}

# To support reload properly, try to access a package var, 
# if it's there, reload everything
if "bpy" in locals():
    import imp
    imp.reload(city)
    imp.reload(const)
    imp.reload(resources)
else:
    from city_generator import city, const, resources


import bpy

# shared
city_instance = None

class CityGeneratorPanel(bpy.types.Panel):
    bl_label = "City Generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Generators'
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="City Parameters:")
        
        scene = context.scene
        row = layout.row()
        row.prop(scene, 'city_x_size')
        row = layout.row()
        row.prop(scene, 'city_y_size')
        row = layout.row()
        row.prop(scene, 'min_block_size')
        row = layout.row()
        row.prop(scene, 'max_block_size')
        row = layout.row()
        row.prop(scene, 'road_size')
        row = layout.row()
        row.operator('city.generate')
        row.operator('city.delete')


class OBJECT_OT_GenerateCity(bpy.types.Operator):
    bl_idname = "city.generate"
    bl_label = "Generate"
    bl_description = "Generates the city based on the given parameters"
 
    def execute(self, context):
        global city_instance
        scene = context.scene
        
        if (scene.city_x_size < scene.min_block_size or
            scene.city_y_size < scene.min_block_size or
            scene.max_block_size < (2*scene.min_block_size +
                                    const.min_road_size)):
            return {'CANCELLED'}
        
        # Remove previous city (if any)
        bpy.ops.city.delete()
        
        # Load the resources
        resources.load_all(scene)
        
        # set the environment
        bpy.data.worlds["World"].light_settings.use_environment_light \
            = True
        
        # Create the city
        city_instance = city.City(scene.city_x_size,
                                  scene.city_y_size,
                                  scene.min_block_size,
                                  scene.max_block_size,
                                  scene.road_size, scene)
        
        return {'FINISHED'}


class OBJECT_OT_DeleteCity(bpy.types.Operator):
    bl_idname = "city.delete"
    bl_label = "Delete"
    bl_description = "Delete the city"
 
    def execute(self, context):
        global city_instance
        scene = context.scene
        
        # delete city and python objects
        if city_instance != None:
            del city_instance
            city_instance = None
        
        # delect all
        if bpy.context.object:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT') 
        
        # unlink objects
        for key, object in scene.objects.items():
            if key.startswith("C_"):
                scene.objects.unlink(object)
        
        # erase the objects
        for key, object in bpy.data.objects.items():
            if key.startswith("C_"):
                bpy.data.objects.remove(object)
                del object
        
        # erase the meshes
        for key, mesh in bpy.data.meshes.items():
            if key.startswith("C_"):
                bpy.data.meshes.remove(mesh)
                del mesh
    
        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)
    
    bpy.types.Scene.city_x_size = \
        bpy.props.FloatProperty(name="X size", default=30.0, min=1.0,
                                max=200.0)
    bpy.types.Scene.city_y_size = \
        bpy.props.FloatProperty(name="Y size", default=30.0, min=1.0,
                                max=200.0)
    bpy.types.Scene.min_block_size = \
        bpy.props.FloatProperty(name="Min block size", default=3.0,
                                min=2.0, max=10.0)
    bpy.types.Scene.max_block_size = \
        bpy.props.FloatProperty(name="Max block size", default=10.0,
                                min=3.0, max=30.0)
    bpy.types.Scene.road_size = \
        bpy.props.FloatProperty(name="Road size", default=2.0,
                                min=const.min_road_size,
                                max=5.0)


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.city_x_size
    del bpy.types.Scene.city_y_size
    del bpy.types.Scene.min_block_size
    del bpy.types.Scene.max_block_size
    del bpy.types.Scene.road_size


if __name__ == "__main__":
    register()
