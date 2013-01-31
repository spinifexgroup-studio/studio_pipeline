# spckCreateTechChannels.py
# Version 0.1
# By Daniel Harkness

import maya.cmds as cmds
import maya.mel as mel

def createTechPasses():
	'''
	Setup render elements
	TODO:
	fix world normals
	'''	
	
	# first we make the sampler node as we will use this twice
	samplerNodeName = 'samplerInfo_for_render_elements'
	if not cmds.objExists(samplerNodeName) :
		samplerNode = cmds.shadingNode('samplerInfo', asUtility=True)
		samplerNode = cmds.rename(samplerNode, samplerNodeName)
	# Surface Normals channel
	layerToMake = 'surfaceNormals'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval ('vrayAddRenderElement normalsChannel;')
		cmds.rename (renderElement,layerToMake)
		cmds.setAttr (layerToMake + '.vray_name_normals', layerToMake, type = 'string')
		cmds.setAttr (layerToMake + '.vray_filtering_normals', True)	
	# Camera Normals channel
	layerToMake = 'cameraNormals'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval ('vrayAddRenderElement ExtraTexElement;')
		cmds.rename (renderElement,layerToMake)
		cmds.setAttr (layerToMake + '.vray_explicit_name_extratex', layerToMake, type = 'string')
		cmds.connectAttr (samplerNodeName + '.normalCamera', layerToMake + '.vray_texture_extratex')	
		cmds.setAttr (layerToMake + '.vray_filtering_extratex', True)
	# World Normals channel
	layerToMake = 'worldNormals'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval ('vrayAddRenderElement ExtraTexElement;')
		cmds.rename (renderElement,layerToMake)
		cmds.setAttr (layerToMake + '.vray_explicit_name_extratex', layerToMake, type = 'string')
		cmds.connectAttr (samplerNodeName + '.normalCamera', layerToMake + '.vray_texture_extratex')	
		cmds.setAttr (layerToMake + '.vray_filtering_extratex', True)
	# zDepth channel
	layerToMake = 'zDepth'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval('vrayAddRenderElement zdepthChannel;')
		renderElement = cmds.rename (renderElement, layerToMake)
		cmds.setAttr(renderElement + '.vray_depthFromCamera_zdepth', True)
		cmds.setAttr(renderElement + '.vray_depthClamp', False)
		cmds.setAttr(renderElement + '.vray_filtering_zdepth', False)
	# zDepth with AA
	layerToMake = 'zDepthAA'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval('vrayAddRenderElement zdepthChannel;')
		renderElement = cmds.rename (renderElement, layerToMake)
		cmds.setAttr(renderElement + '.vray_depthFromCamera_zdepth', True)
		cmds.setAttr(renderElement + '.vray_depthClamp', False)
		cmds.setAttr(renderElement + '.vray_filtering_zdepth', True)	
	# UVs
	layerToMake = 'UV'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval ('vrayAddRenderElement ExtraTexElement;')
		cmds.rename (renderElement,layerToMake)
		cmds.setAttr (layerToMake + '.vray_explicit_name_extratex', 'uv', type = 'string')
		cmds.connectAttr (samplerNodeName + '.uvCoord.uCoord', layerToMake + '.vray_texture_extratex.vray_texture_extratexR')	
		cmds.connectAttr (samplerNodeName + '.uvCoord.vCoord', layerToMake + '.vray_texture_extratex.vray_texture_extratexG')
		cmds.setAttr(layerToMake + '.vray_filtering_extratex', False)
	# worldXYZ
	layerToMake = 'worldXYZ'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval ('vrayAddRenderElement ExtraTexElement;')
		cmds.rename (renderElement,layerToMake)
		cmds.setAttr (layerToMake + '.vray_explicit_name_extratex', 'worldXYZ', type = 'string')
		cmds.setAttr (layerToMake + '.vray_considerforaa_extratex', False)
		cmds.connectAttr (samplerNodeName + '.pointWorld', layerToMake+'.vray_texture_extratex')
	# Ambient Occlusion
	layerToMake = 'AO'
	if not cmds.objExists (layerToMake) :
		renderElement = mel.eval ('vrayAddRenderElement ExtraTexElement;')
		renderElement = cmds.rename (renderElement,layerToMake)
		cmds.setAttr (renderElement + '.vray_explicit_name_extratex', layerToMake, type = 'string')
		newNode = cmds.shadingNode('VRayDirt', name = 'ao_tex', asTexture=True)
		cmds.connectAttr (newNode + '.outColor', renderElement + '.vray_texture_extratex')
		cmds.setAttr (newNode + '.invertNormal', 1)
		cmds.setAttr (newNode + '.ignoreForGi', 0)
		cmds.setAttr (newNode + '.blackColor', -0.5 ,-0.5 ,-0.5, type='double3')
		cmds.setAttr (newNode + '.falloff', 5)
	# TopDown falloff pass
	layerToMake = 'topDown'
	nodeToMake = 'topdown_tex'
	if not cmds.objExists (layerToMake) :
		if not cmds.objExists (nodeToMake) :
			# now create the vray plugin with no placement on UV (0 = none, 1 = 2d, 2 = 3d)
			newNode = mel.eval( 'catchQuiet (vrayCreateNodeFromDll (nodeToMake, "texture", "TexFalloff", 2));')
			newNode = cmds.rename( nodeToMake , nodeToMake )
			cmds.setAttr (newNode + '.direction_type', 2)
			cmds.setAttr (newNode + '.color1', 1, 0, 0, type='double3')
			cmds.setAttr (newNode + '.color2', 0, 1, 0, type='double3')
		renderElement = mel.eval ('vrayAddRenderElement ExtraTexElement;')
		renderElement = cmds.rename (renderElement,layerToMake)
		cmds.setAttr (renderElement + '.vray_explicit_name_extratex', layerToMake, type = 'string')
		cmds.connectAttr (nodeToMake + '.outColor', renderElement + '.vray_texture_extratex')  
	# Give some feedback for next steps
	cmds.select ( clear=True )
	dialogMessage = 'Tech Channels Created'
	result = cmds.confirmDialog(title='spckSetupScene', message=dialogMessage, button=['OK'], defaultButton='OK')
	print ('Complete.\n')