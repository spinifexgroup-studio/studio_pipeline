# spckSetupScene.py
# Version 0.9
# By Daniel Harkness

import maya.cmds as cmds
import maya.utils as utils
import maya.mel as mel
from createBaseRenderSettings import *

def setupScene():
	'''
	Setup some scene attributes we want to be common to all Spinifex car scenes
	TODO:
	make width over height as float
	'''
		
	# Check if we haven't done this before
	if cmds.objExists('vraySettings.setupSceneHasBeenRun'):
		# Check that everything is setup correctly before continuing.
		dialogMessage = 'setupScene has already been run. Do you wish to continue? Some of your render settings will be reset.'
		result = cmds.confirmDialog( title='spckSetupScene', message=dialogMessage, button=['YES','NO'], defaultButton='NO', cancelButton='NO', dismissString='NO' )
		if result == 'NO' :
			print("Aborted. We\'ve done this before...\n")
			return
	else:
		# Check that everything is setup correctly before continuing.
		dialogMessage = 'Have you set up your workspace.mel?'
		result = cmds.confirmDialog( title='spckSetupScene', message=dialogMessage, button=['YES','NO'], defaultButton='YES', cancelButton='NO', dismissString='NO' )
		if result == 'NO' :
			print('Go setup your workspace and run again.\n')
			return
		
	# Units for working in metric and 30fps
	cmds.currentUnit (linear='cm')
	cmds.currentUnit (angle='deg')
	cmds.currentUnit (time='ntsc')

	# Load VRAY if not active
	cmds.loadPlugin ('vrayformaya', quiet=True)
	cmds.pluginInfo ('vrayformaya', edit=True, autoload=True)
	cmds.setAttr  ('defaultRenderGlobals.ren', 'vray', type='string')

	cmds.evalDeferred ( 'createBaseRenderSettings()' , lowestPriority=True )	
	print('Success.\n')