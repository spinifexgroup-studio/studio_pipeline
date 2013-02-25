# recursiveRename.py
# Version 0.1
# By Daniel Harkness

import maya.cmds as cmds
import maya.utils as utils
import maya.mel as mel

def renameChildren( findStr = "" , replaceStr = "" , selection = [] ):
	# Pass in selection list or selected items or everything if nothing selected
	if not selection:
		selection = cmds.ls( selection = True )
		if not selection:
			# Check that the user wants to rename everything.
			dialogMessage = 'Nothing is selected. Do you want to search everything?'
			result = cmds.confirmDialog( title='spin', message=dialogMessage, button=['YES','NO'], defaultButton='NO', cancelButton='NO', dismissString='NO' )
			if result == 'NO' :
				print("Aborted.\n")
				return
			selection = cmds.ls( long=True )

	if len(findStr) == 0:
		# Source and replace text.
		dialogMessage = 'Find text:'
		result = cmds.promptDialog( title='spin', message=dialogMessage, button=['OK','Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel' )
		if result == 'OK':
			findStr = cmds.promptDialog (query=True, text=True)
		dialogMessage = 'Replace text:'
		result = cmds.promptDialog( title='spin', message=dialogMessage, button=['OK','Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel' )
		if result == 'OK':
			replaceStr = cmds.promptDialog (query=True, text=True)
			
	replaceList = []
	replaceList = cmds.listRelatives (selection , allDescendents=True, noIntermediate=True, fullPath=True )
	if not replaceList:
		replaceList = []
	replaceList = replaceList + selection
	
	for item in replaceList:
		if findStr in item:
			cmds.select ( item , replace = True)
			itemName = cmds.ls( long=False , selection=True)
			cmds.rename ( itemName[0].replace ( findStr , replaceStr ) )
			#print itemName + '\nrenamed to\n' + itemName[0].replace ( findStr , replaceStr ) + '\n'