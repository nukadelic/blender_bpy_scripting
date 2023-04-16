import bpy

move_to = ( 0, 0, 0 )

move_only_selected = False 

# -----------------------------------

move_objects = bpy.data.objects

if move_only_selected : move_objects = bpy.context.selected_objects

for ob in move_objects :
    
    if ob.type == 'MESH':
        
        ob.location = move_to
