# bakeFor2d.py
# Version 0.1
# By Daniel Harkness

import maya.cmds as cmds
import maya.utils as utils
import maya.mel as mel

selection = cmds.ls( selection = True )
if not selection:
	selection = cmds.ls()

cameraList = []
nullList = []
for item in selection:
	if cmds.objectType ( item , isType='camera' ):
		cameraList.append ( item )
	if cmds.objectType ( item , isType='locator' ):
		if 'null' in item:
			nullList.append ( item )
			
for nullItem in nullList:
	cmds.select (nullItem, replace=True)
	nullTransform = cmds.pickWalk ( direction='up' )

	newNullName = nullItem[:-5]+'_baked'
	newNullTransform = cmds.spaceLocator ( name=newNullName , position = (0,0,0))
	
	newNullShape = cmds.listRelatives ( children=True, shapes=True, allDescendents=False)
	cmds.setAttr ( newNullShape[0]+'.localScaleX' , cmds.getAttr ( nullItem+'.localScaleX' ))
	cmds.setAttr ( newNullShape[0]+'.localScaleY' , cmds.getAttr ( nullItem+'.localScaleY' ))
	cmds.setAttr ( newNullShape[0]+'.localScaleZ' , cmds.getAttr ( nullItem+'.localScaleZ' ))
	
	
	worldMatrix = cmds.xform(nullTransform, q=True, ws=True, m=True)
	cmds.xform(newNullTransform, ws=True, m=worldMatrix )

	cmds.parentConstraint ( nullTransform , newNullTransform , maintainOffset=True , weight=1 )
