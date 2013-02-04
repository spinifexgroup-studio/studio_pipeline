# spckCreateCarMultimattes.py
# Version 0.1
# By Daniel Harkness

import maya.cmds as cmds
import maya.mel as mel

def createCarMattes():
	'''
	Setup render elements
	TODO:
	enter correct IDs for bulbs lens
	'''	
	
	# Main multimatte for main parts
	layerToMake = 'multimatte_main'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval ('vrayAddRenderElement MultiMatteElement;')
		cmds.rename (renderElement,layerToMake)
		cmds.setAttr (layerToMake + '.vray_name_multimatte', layerToMake, type = 'string')
        cmds.setAttr (layerToMake + '.vray_considerforaa_multimatte', True)
        cmds.setAttr (layerToMake + '.vray_redid_multimatte',   1)		# Paint
        cmds.setAttr (layerToMake + '.vray_greenid_multimatte', 2)		# TBA
        cmds.setAttr (layerToMake + '.vray_blueid_multimatte',  3)		# Windows
        cmds.setAttr (layerToMake + '.vray_usematid_multimatte', True)	
	# Main multimatte for the light elements like headlights and tailights
	layerToMake = 'multimatte_lights'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval ('vrayAddRenderElement MultiMatteElement;')
		cmds.rename (renderElement,layerToMake)
		cmds.setAttr (layerToMake + '.vray_name_multimatte', layerToMake, type = 'string')
        cmds.setAttr (layerToMake + '.vray_considerforaa_multimatte', True)
        cmds.setAttr (layerToMake + '.vray_redid_multimatte',   4)		# Read
        cmds.setAttr (layerToMake + '.vray_greenid_multimatte', 5)		# Fog and side lamps
        cmds.setAttr (layerToMake + '.vray_blueid_multimatte',  6)		# Headlights
        cmds.setAttr (layerToMake + '.vray_usematid_multimatte', True)
	# Main multimatte for smaller parts
	layerToMake = 'multimatte_parts'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval ('vrayAddRenderElement MultiMatteElement;')
		cmds.rename (renderElement,layerToMake)
 		cmds.setAttr (layerToMake + '.vray_name_multimatte', layerToMake, type = 'string')
 		cmds.setAttr (layerToMake + '.vray_considerforaa_multimatte', True)
        cmds.setAttr (layerToMake + '.vray_redid_multimatte',   7)		# Plastic
        cmds.setAttr (layerToMake + '.vray_greenid_multimatte', 8)		# Metal
        cmds.setAttr (layerToMake + '.vray_blueid_multimatte',  9)		# Chrome
        cmds.setAttr (layerToMake + '.vray_usematid_multimatte', True)
	# Main multimatte for wheels
	layerToMake = 'multimatte_wheels'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval ('vrayAddRenderElement MultiMatteElement;')
		cmds.rename (renderElement,layerToMake)
 		cmds.setAttr (layerToMake + '.vray_name_multimatte', layerToMake, type = 'string')
		cmds.setAttr (layerToMake + '.vray_considerforaa_multimatte', True)
        cmds.setAttr (layerToMake + '.vray_redid_multimatte',   10)		# Brake
        cmds.setAttr (layerToMake + '.vray_greenid_multimatte', 11)		# Tyre
        cmds.setAttr (layerToMake + '.vray_blueid_multimatte',  12)		# Alloys
        cmds.setAttr (layerToMake + '.vray_usematid_multimatte', True)
	# Main multimatte for bulbs, lenses and light chome
	layerToMake = 'multimatte_bulbsAndLenses'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval ('vrayAddRenderElement MultiMatteElement;')
		cmds.rename (renderElement,layerToMake)
  		cmds.setAttr (layerToMake + '.vray_name_multimatte', layerToMake, type = 'string')
  		cmds.setAttr (layerToMake + '.vray_considerforaa_multimatte', True)
        cmds.setAttr (layerToMake + '.vray_redid_multimatte',   13)		# Bulbs
        cmds.setAttr (layerToMake + '.vray_greenid_multimatte', 14)		# Lenses
        cmds.setAttr (layerToMake + '.vray_blueid_multimatte',  15)		# Light Chrome
        cmds.setAttr (layerToMake + '.vray_usematid_multimatte', True)
	# Give some feedback for next steps
	cmds.select ( clear=True )
	dialogMessage = 'Car Mattes Created'
	result = cmds.confirmDialog(title='spck', message=dialogMessage, button=['OK'], defaultButton='OK')
	print ('Car Mattes Success.\n')