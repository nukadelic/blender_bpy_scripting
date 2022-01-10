![IMG](https://github.com/nukadelic/blender_bpy_scripting/blob/main/Text_To_Separate_Meshes/img.png?raw=true)

### Execution

* store selected text in `M`
* _Extrude Text_ (#1)
* Focus `M`
* while first vertex selection (#2) is possible - select "char"
* Separate selected "char" (#3)
* Unfocus `M`
* Loop "chars" and _recenter_ them (#4)
* Set mesh name based on index (charcode upper case A = 65)
* Focus `M` and delete it 

```py
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
    
    _item.name = str( chr(i + 65 ) )
    
    
M.select_set( True )

bpy.ops.object.mode_set(mode='OBJECT')

bpy.data.objects.remove( M , do_unlink=True )
```

### 1. Extrude Text 

* check if selection is a font 
* convert to mesh 
* extrude on Z axis by amount `z` 
* recenter 

```py
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
```

### 2. Select First vertex
* exit / enter object mode to refresh selection
* check if data length is valid & select 1st vertex 

```py
def selectVert0( _target ):
    # https://blender.stackexchange.com/a/43138
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    if len( _target.data.vertices ) <= 0 :
        return False
    
    # me.vertices.foreach_set("select",[not i for i in range(len(me.vertices))])
    _target.data.vertices[0].select = True
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    return True 
```



### 3. Seperate selection and return new mesh 

* create two lists ( before separation and after ) 
* compare the lists and return the unique one ( the new created mesh ) 

```py
def separate_selected():
    # https://blenderartists.org/t/access-a-separated-object-with-python/540716/5
    
    lo_b = [ob for ob in bpy.data.objects if ob.type == 'MESH']
    bpy.ops.mesh.separate(type='SELECTED')
    lo_a = [ob for ob in bpy.data.objects if ob.type == 'MESH']
    
    for i in lo_b:
        lo_a.remove(i)
    
    separate_object = lo_a[0]
    
    return separate_object
```

### 4. Recenter object and align origin 

```py
def recenter( _item ):

    _item.select_set(True)
    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.origin_set( type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN' )
    
    _item.location.x = 0
    
    bpy.context.scene.cursor.location = (0,0,0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    bpy.ops.object.mode_set(mode='EDIT')
    
    _item.select_set(False)
```

Font : https://www.dafont.com/targa.font , Licence : Public domain / GPL / OFL
