
def vec_dist( a , b ) : return ( (a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2 ) ** 0.5

def select( obj , idx = -1 ):
    
    if idx == -1 : idx = obj.active_shape_key_index
        
    if idx == 0 : return # prevent selecting for default shape key 
    
    k0 = obj.data.shape_keys.key_blocks[ 0 ]
    k1 = obj.data.shape_keys.key_blocks[ idx ]
    
    me = o.data
    bm = bmesh.from_edit_mesh( me )
    
    for i in range( len( k0.data ) ) : 
        v1 = k0.data[ i ].co
        v2 = k1.data[ i ].co
        
        # select only edited verticies
        bm.verts[ i ].select = vec_dist( v1 , v2 ) > 1e-7
    
    me.update() # make selection visible in 3d viewport 
    
    
'''

select( bpy.context.scene.selected_objects[ 0 ] )

'''
