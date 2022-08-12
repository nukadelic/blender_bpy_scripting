import bpy

'''
Before: CH_MS_Cap , Mesh.026
After: CharM_Cap , CharM_m_Cap
'''

str_original = "CH_MS"
str_new = "CharM"

mesh_owners = {}
for ob in bpy.data.objects:
    if ob.type == 'MESH':
        mesh_owners.setdefault(ob.data, []).append(ob)

for mesh in bpy.data.meshes :
    if not mesh in mesh_owners.keys() : continue 
    parent = mesh_owners[ mesh ][ 0 ]
    name = parent.name
    
    if mesh.name.find( str_new + "_m" ) > -1 and parent.name.find( str_new ) > -1 : continue
    
    print( "Before: " + parent.name + " > " + mesh.name )

    parent.name = name.replace( str_original , str_new )
    
    mesh.name = parent.name.replace( str_new, str_new + "_m" )
    
    print( "After: " + parent.name + " , " + mesh.name + "\n" )
