import bpy

#all_objects = list( bpy.data.objects )
#mesh_A = bpy.data.objects[ "A" ]
#selection = list( bpy.context.selected_objects )
# bpy.ops.object.transform_apply() 
#bpy.ops.transform.translate( value=( -1 , 0, 0 ) )
#bpy.context.object.location.z = 0

# ----------------------------------------------------------------------------------

def text_extrude( z ):
    
    if( bpy.context.active_object.type != "FONT" ):
        return False
    
    bpy.ops.object    .mode_set(mode =      'OBJECT')
    bpy.ops.object    .convert(target=      'MESH')
    bpy.ops.object    .mode_set(mode =      'EDIT') 
    bpy.ops.mesh      .select_all(action=   'SELECT')

    bpy.ops.mesh.extrude_region_move( TRANSFORM_OT_translate={"value":(0, 0, z )} )

    bpy.ops.mesh      .select_all(action=   'SELECT')

    bpy.ops.transform.translate(value=( -0, -0 , - ( z / 2 ) ) )

    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    return True

        
# ----------------------------------------------------------------------------------

def separate_selected():
    
    lo_b = [ob for ob in bpy.data.objects if ob.type == 'MESH']
    
    bpy.ops.mesh.separate(type='SELECTED')
    
    lo_a = [ob for ob in bpy.data.objects if ob.type == 'MESH']

    for i in lo_b:
        lo_a.remove(i)
    separate_object = lo_a[0]
    
    return separate_object

# ----------------------------------------------------------------------------------
 
def selectVert0( _target ):
    # https://blender.stackexchange.com/a/43138
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    if len( _target.data.vertices ) <= 0 :
        return False
    _target.data.vertices[0].select = True
    # me.vertices.foreach_set("select",[not i for i in range(len(me.vertices))])
    bpy.ops.object.mode_set(mode = 'EDIT')
    return True 


def recenter( _item ):
    _item.select_set(True)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.origin_set( type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN' )
    bpy.context.scene.cursor.location = (0,0,0)
    _item.location.x = 0
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    bpy.ops.object.mode_set(mode='EDIT')
    _item.select_set(False)




extrude_amount = 0.2

M = bpy.context.active_object

success = text_extrude( extrude_amount )

# print( M.name , M.type , success )

result = list()

M.select_set( True )

while selectVert0( M ):    
    
    bpy.ops.mesh.select_linked( delimit=set() )
    
    new_mesh = separate_selected()
    
    result.append( new_mesh )
    

M.select_set( False )
    
for i in range(len(result)):
    _item = result[ i ]
    
    recenter( _item )
    
    _item.name = "M" + str( i )
    
    
M.select_set( True )

bpy.ops.object.mode_set(mode='OBJECT')

bpy.data.objects.remove( M , do_unlink=True )





# bpy.ops.object.select_all(action='DESELECT')

# bpy.ops.object.mode_set(mode = 'OBJECT') 
# bpy.ops.object.mode_set(mode = 'EDIT') 
# bpy.ops.object.editmode_toggle()

# me.vertices[ 0 ].select = True

# -- -- another way to select only vert 0
# me.vertices.foreach_set("select",[not i for i in range(len(me.vertices))])

# bpy.ops.mesh.select_linked( delimit=set() )

#for o in list( bpy.context.selected_objects ):
#    o.location.x = 0
