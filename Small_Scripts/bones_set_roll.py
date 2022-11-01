import bpy 
from math import degrees , radians

'''
Set bone roll value to the selected bones 
make sure you are in armature edit mode 
'''

value = radians( 0 ) 

selected_bones = bpy.context.selected_bones

for i in range(len(selected_bones)):
    
    bone = selected_bones[ i ] 
    
    bone.roll = value
