# bakeFor2d.py
# Version 0.1
# By Daniel Harkness

import maya.cmds as cmds
import maya.utils as utils
import maya.mel as mel

def bakeFor2d( selection = [] ):
	bakeFirst = 0
	bakeLast = 0

	# Get First and last Frames.
	dialogMessage = 'Bake Start Frame:'
	result = cmds.promptDialog( title='spin', message=dialogMessage, button=['OK','Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel' )
	if result == 'OK':
		promptResult = cmds.promptDialog (query=True, text=True)
		if len (promptResult) > 0:
			try:
				int(promptResult)
			except:
				print 'Aborted. Please enter in valid frame numbers.'
				pass
			bakeFirst = int(promptResult)
	dialogMessage = 'Bake Last Frame:'
	result = cmds.promptDialog( title='spin', message=dialogMessage, button=['OK','Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel' )
	if result == 'OK':
		promptResult = cmds.promptDialog (query=True, text=True)
		if len (promptResult) > 0:
			try:
				int(promptResult)
			except:
				print 'Aborted. Please enter in valid frame numbers.'
				pass
			bakeLast = int(promptResult)
			
	
			


	bakeList = []			# List of items to bake
	constraintList = []		# List of constraints for cameras and nuls - deleted at end
	nullList = []			# List of locators
	cameraList = []			# List of cameras

	# Pass in selection list or selected items or everything if nothing selected
	if not selection:
		selection = cmds.ls( selection = True )
		if not selection:
			selection = cmds.ls()

	# Iterate through the selection for nulls or cameras
	if selection:
		cameraList = cmds.listRelatives(selection, allDescendents=True, noIntermediate=True, fullPath=False, type='camera')
		nullList = cmds.listRelatives(selection, allDescendents=True, noIntermediate=True, fullPath=False, type='locator')
		if not cameraList:
			cameraList = []
		if not nullList:
			nullList = []

	for nullShape in nullList:
		if 'null' in nullShape:
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
		# filter out stero cameras
		if cmds.objectType (cameraShape) == 'camera':
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
		'''
		bakedItemsGroup = 'bakedItems'
		if not cmds.objExists ( bakedItemsGroup ):
			cmds.group ( name=bakedItemsGroup, em=True )
		for item in bakeList:
			cmds.parent ( item, bakedItemsGroup)
		'''
		cmds.select (clear=True)
		for item in bakeList:
			cmds.select ( item, add=True )
		cmds.bakeResults ( time=(bakeFirst,bakeLast) , simulation=True )
		for item in constraintList:
			cmds.delete (item)
		# Remove name spacing
		for item in bakeList:
			if type(item) is list:
				item = item[0]
			if ':' in item:
				print item+' has namespacing'
				itemSplit = item.split (':')
				cmds.rename ( item , itemSplit[len(itemSplit)-1] )