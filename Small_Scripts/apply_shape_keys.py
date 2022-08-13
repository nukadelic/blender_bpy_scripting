# https://blender.stackexchange.com/a/200727

import bpy
scene = bpy.context.scene

for ob in scene.objects:
  
    if not hasattr(ob.data, "shape_keys"): continue
      
    ob.shape_key_add(name='CombinedKeys', from_mix=True)
    
    if ob.data.shape_keys:
        for shapeKey in ob.data.shape_keys.key_blocks:
            ob.shape_key_remove(shapeKey)
