# Car.py
# Version 0.1
# By Daniel Harkness

import maya.cmds as cmds
import maya.utils as utils
import maya.mel as mel

selection = cmds.ls( selection = True )
if selection:
	selectionChildren = cmds.listRelatives ( selection, children=True, allDescendents=True, shapes=True )
	selection = selection + selectionChildren	
else:
	selection = cmds.ls()

cameraList = []
nullList = []
bakeList = []
constraintList = []

for item in selection:
	if cmds.objectType ( item , isType='camera' ):
		cameraList.append ( item )
	if cmds.objectType ( item , isType='locator' ):
		if 'null' in item:
			nullList.append ( item )
			
for nullShape in nullList:
	cmds.select (nullShape, replace=True)
	nullTransform = cmds.pickWalk ( direction='up' )

	newNullName = nullShape[:-5]+'_baked'
	newNullTransform = cmds.spaceLocator ( name=newNullName , position = (0,0,0))
	
	newNullShape = cmds.listRelatives ( children=True, shapes=True, allDescendents=False)
	cmds.setAttr ( newNullShape[0]+'.localScaleX' , cmds.getAttr ( nullShape+'.localScaleX' ))
	cmds.setAttr ( newNullShape[0]+'.localScaleY' , cmds.getAttr ( nullShape+'.localScaleY' ))
	cmds.setAttr ( newNullShape[0]+'.localScaleZ' , cmds.getAttr ( nullShape+'.localScaleZ' ))
	
	
	worldMatrix = cmds.xform(nullTransform, q=True, ws=True, m=True)
	cmds.xform(newNullTransform, ws=True, m=worldMatrix )

	constraint = cmds.parentConstraint ( nullTransform , newNullTransform , maintainOffset=True , weight=1 )
	
	bakeList.append ( newNullTransform )
	constraintList.append ( constraint )

for cameraShape in cameraList:
	# check for default ortho cameras
	if not ( 'persp' in cameraShape or 'side' in cameraShape or 'top' in cameraShape or 'front' in cameraShape ):
		# check for craft cameras
		if not ( 'WheelerExt' in cameraShape ):
			cmds.select (cameraShape, replace=True)
			cameraTransform = cmds.pickWalk (direction='up')
	
			newCameraName = cameraShape[:-5]+'_baked'
			newCamera = cmds.camera()
			newCameraTransform = newCamera[0]
			newCameraShape = newCamera[1]
	
			worldMatrix = cmds.xform(cameraTransform, q=True, ws=True, m=True)
			cmds.xform(newCameraTransform, ws=True, m=worldMatrix )
	
			constraint = cmds.parentConstraint ( cameraTransform , newCameraTransform , maintainOffset=True , weight=1 )

			cmds.connectAttr ( cameraShape+'.focalLength' , newCameraShape+'.focalLength' , force=True )
			cmds.connectAttr ( cameraShape+'.cameraAperture' , newCameraShape+'.cameraAperture' , force=True )
			cmds.connectAttr ( cameraShape+'.filmOffset' , newCameraShape+'.filmOffset' , force=True )
			cmds.connectAttr ( cameraShape+'.lensSqueezeRatio' , newCameraShape+'.lensSqueezeRatio' , force=True )

			cmds.rename ( newCamera[0] , newCameraName )
			
			bakeList.append ( newCameraName )
			constraintList.append ( constraint )
			
if bakeList and constraintList:
	bakedItemsGroup = 'bakedItems'
	if not cmds.objExists ( bakedItemsGroup ):
		cmds.group ( name=bakedItemsGroup, em=True )
	cmds.select (clear=True)
	for item in bakeList:
		cmds.parent ( item, bakedItemsGroup)
	for item in bakeList:
		cmds.select ( item, add=True )
	cmds.bakeResults ( time=(320,340) , simulation=True )
	for item in constraintList:
		cmds.delete (item)


