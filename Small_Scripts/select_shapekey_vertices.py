import bmesh
import bpy 


def vec_dist( a , b ) : return ( (a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2 ) ** 0.5


def select( obj , idx = -1 , err_pow = 3 ):
    
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_mode(type="VERT")
    
    if idx == -1 : idx = obj.active_shape_key_index
    
    if idx == 0 : return # prevent selecting for default shape key 
    
    k0 = obj.data.shape_keys.key_blocks[ 0 ]
    k1 = obj.data.shape_keys.key_blocks[ idx ]
    
    me = obj.data
    bm = bmesh.from_edit_mesh( me )
    
    count = 0
    
    min_dist = pow( 10, -err_pow ) 
    
    for i in range( len( k0.data ) ) : 
        
        v1 = k0.data[ i ].co
        v2 = k1.data[ i ].co
        
        changed = vec_dist( v1 , v2 ) > min_dist
        
        # select only edited verticies
        bm.verts[ i ].select = changed
        
        if changed : count = count + 1
    
    #print( "Count: " + str( count ) )
    
    me.update() # make selection visible in 3d viewport 
    
    
# bpy.context.scene.objects[ 0 ]

select( bpy.context.selected_objects[ 0 ] )
