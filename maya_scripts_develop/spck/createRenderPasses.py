# spckCreateRenderElements.py
# Version 0.2
# By Daniel Harkness

import maya.cmds as cmds
import maya.mel as mel

def createRenderPasses():
	'''
	Setup render elements
	TODO:
	'''	
	
	# Create diffuse channel
	layerToMake = 'diffuse'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval ('vrayAddRenderElement diffuseChannel;')
		cmds.rename (renderElement,layerToMake)
	# Create reflect channel
	layerToMake = 'reflect'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval ('vrayAddRenderElement reflectChannel;')
		cmds.rename (renderElement,layerToMake)
	# Create refract channel
	layerToMake = 'refract'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval ('vrayAddRenderElement refractChannel;')
		cmds.rename (renderElement,layerToMake)
	# Create specular channel
	layerToMake = 'specular'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval ('vrayAddRenderElement specularChannel;')
		cmds.rename (renderElement,layerToMake)
	# Create lighting channel
	layerToMake = 'lighting'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval ('vrayAddRenderElement lightingChannel;')
		cmds.rename (renderElement,layerToMake)
	# Create GI channel
	layerToMake = 'GI'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval ('vrayAddRenderElement giChannel;')
		cmds.rename (renderElement,layerToMake)
	# Create rawGI channel
	layerToMake = 'rawGI'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval ('vrayAddRenderElement rawGiChannel;')
		cmds.rename (renderElement,layerToMake)
	# Create selfIllum channel
	layerToMake = 'selfIllum'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval ('vrayAddRenderElement selfIllumChannel;')
		cmds.rename (renderElement,layerToMake)
	print ('Success!')
