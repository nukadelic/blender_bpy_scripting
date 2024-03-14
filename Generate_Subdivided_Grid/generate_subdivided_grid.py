import bpy 

def vec_dist( a , b ) : return ( (a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2 ) ** 0.5

def select( dist ) :
    count = 0
    zero = ( 0, 0, 0 )
    selected_indexes = []
    
    # selecting and displaying verticies 
    # https://blender.stackexchange.com/a/43138
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj = bpy.context.active_object
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    for i in range( len( bpy.context.active_object.data.vertices ) ) :
        
        v = bpy.context.active_object.data.vertices[ i ].co
        
        if vec_dist( v , zero ) < dist :    
            count = count + 1         
            selected_indexes.append( i )            
        
    for i in range( len( selected_indexes ) ) :
        ii = selected_indexes[ i ]
        obj.data.vertices[ ii ].select = True
    bpy.ops.object.mode_set(mode = 'EDIT')
                
    bpy.context.active_object.data.vertices.update()
    bpy.context.active_object.data.update()
    
    return count 

def make_grid( cuts , steps ):
    
    if bpy.context.active_object is not None : 
    
        bpy.ops.object.mode_set(mode = 'OBJECT') 
    
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    
    bpy.ops.object.mode_set(mode = 'EDIT') 
    
    bpy.ops.mesh.subdivide( number_cuts=cuts )
    
    # update mesh data 
    bpy.ops.object.mode_set(mode = 'OBJECT') 
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_all(action = 'DESELECT')

    # delete verticies outside selection     
    select( 1.01 )
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.mesh.delete(type='VERT')
        
    # subdivide each step 
    for step_i in range( steps - 1 ):
        
        step_inv = steps - step_i - 1 
        
        r = step_inv / steps
        
        select( r ) 
        
        bpy.ops.mesh.subdivide( number_cuts=1 )
        
        # update mesh data 
        bpy.ops.object.mode_set(mode = 'OBJECT') 
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_all(action = 'DESELECT')
        
    # triangulate 
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris(quad_method='FIXED', ngon_method='BEAUTY')
    bpy.ops.object.mode_set(mode = 'OBJECT') 
    
# ------------------------------------------------------------------------------
        
make_grid( 41 , 3 )  
