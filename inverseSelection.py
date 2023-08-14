"""
Christopher Lew
Jul 10,2023
Inverses a selection
TO INVERSE: press update groups button on start up and whenever groups change then press inverse selection
"""

def button_wrapper(func, *args, **kwargs):
    def wrapped(_):
        func(*args, **kwargs)
    return wrapped
    
def updateGroups():
	if groups:
		groups.clear()
	meshes = cmds.ls(visible=True, dag=True, long=True, type='transform')
	#if the transform has no geometric children, then it is a group and add to groups list
	for obj in meshes:
		if not cmds.listRelatives(obj, shapes=True):
			groups.append(obj)

def inverse():
    #get current selection (to deselect later)
    originalSelection = cmds.ls(selection=True, long=True, type='transform')
    for obj in groups:
    	originalSelection.append(obj)
    #select everything visible (NO CAMERAS!)
    newSelection = cmds.ls(visible=True, dag=True, long=True, type='transform')
    
    cmds.select(newSelection)
    cmds.select(originalSelection, deselect=True)
    
def inverseUI():
    window = cmds.window( title="Inverse Selection", iconName="Inverse", widthHeight=(350, 60) )
    masterLayout = cmds.columnLayout( adjustableColumn=True)
    cmds.textField( editable=False, text='Press "Update Groups" upon start up and when groups change')
    
    cmds.rowLayout( numberOfColumns=2, columnWidth2=[175,175], columnAttach2=['both', 'both'], columnOffset2=[10, 20] )
    
    cmds.button( label='Update Groups', command=button_wrapper(updateGroups) )
    cmds.button( label='Inverse Selection', command=button_wrapper(inverse) )
    cmds.showWindow( window )

groups = []
inverseUI()