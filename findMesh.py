"""
Christopher Lew
Jul 4,2023
Selects meshes based on user input (text must be exact match)
TO SEARCH: hit seach button or right enter key to search for characters in text field
           will seach within a selection if it exists or through all meshes
"""
from maya import cmds

#we wrap the functions to avoid confusing command statements
def button_wrapper(func, *args, **kwargs):
    def wrapped(_):
        func(*args, **kwargs)
    return wrapped

def search(text_field, result_field):
    selection = cmds.ls(selection=True, long=True)
    changedState = False
    
    #if something is already selected add the children
    if selection:
        meshes = selection
        for obj in selection:
            children = cmds.listRelatives(obj, allDescendents=True, fullPath=True, type='transform')
            if children:
                for child in children: 
                    meshes.append(child)
    else:
        meshes = cmds.ls(type='transform', dag=True, long=True)

    #get text from textfield
    key = cmds.textField(text_field, query=True, text=True)
    
    for obj in meshes:
        shortName = obj.split('|')[-1]
        result = shortName.find(key)
        
        if result != -1:
            changedState = True;
            cmds.select(obj, add=True)
    #update result text field
    if changedState:
        cmds.textField(result_field, edit=True, text='Success!')
    else:
        cmds.textField(result_field, edit=True, text='Mesh does not exist')

def findMeshUI():
    window = cmds.window( title="Find Mesh", widthHeight=(450, 120) )
    masterLayout = cmds.columnLayout( adjustableColumn=True )
    cmds.textField(editable=False, text="Select a parent to search through its children, otherwise searches through outliner")
    result = cmds.textField(editable=False)
    
    cmds.rowLayout( adjustableColumn=1, numberOfColumns=3 )
    input = cmds.textField()
    #pass function and text field into button_wrapper
    selection = cmds.ls(selection=True)
    cmds.textField(input, edit=True, enterCommand=button_wrapper(search, input, result))
    cmds.button( label='Search', command=button_wrapper(search, input, result) )
    
    #buttons and other stuff go with nearest layout, set parent .. to go back to original layout
    cmds.setParent( masterLayout )
    cmds.button(label='Deselect', command=('cmds.select(clear=True)'))
    cmds.button(label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)'))
    
    cmds.showWindow( window )

findMeshUI()
    