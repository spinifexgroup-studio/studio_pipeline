# connectCarToCraftRig.py
# Version 0.1
# By Daniel Harkness

import maya.cmds as cmds
import maya.utils as utils
import maya.mel as mel

def connectCarToCraftRig():
	selection = cmds.ls ( selection=True )
	if len ( selection ) == 2:
		if cmds.objExists ( selection[0]+'.isCar' ):
			if selection[1][-20:] == 'CarBodyMeshTransform':
				craftRigName = selection[1][:-20]
				cmds.group ( craftRigName+'TargetMeshTransform' , craftRigName+'GravityDirectionMeshTransform' ,craftRigName+'CarBodyMeshTransform' ,  name=craftRigName+'group')
				cmds.xform ( os=True , piv=( 0, 0, 0 ))
				cmds.setAttr ( craftRigName+'group.rotateY' , 180 )
				cmds.ungroup ( craftRigName+'group' )
			
				carName = selection[0]
				underCarriageY = cmds.getAttr (carName+'_exterior.boundingBoxMinY')
				carLength = cmds.getAttr (carName+'.boundingBoxSizeZ')
				rigLength = 352.0 #baked value - can't get bounding box information becaus of follow cam
			
				cmds.select ( craftRigName+'CarBodyMeshTransform' , replace=True )
				scaleValue = carLength/rigLength
				cmds.scale ( scaleValue, scaleValue, scaleValue, relative=True )
			
				rigFront = cmds.getAttr ( craftRigName+'CarBodyMeshTransform.boundingBoxMaxZ' )
				carFront = cmds.getAttr ( carName+'.boundingBoxMaxZ' )
				cmds.move ( 0 , 0 , carFront-rigFront , relative = True )

				cmds.parentConstraint ( craftRigName+'CarBodyMeshTransform' , carName+'_body' , maintainOffset=True , weight= 1 )
				
				carWheels			= [ carName+'_wheelFL' , carName+'_wheelFR' , carName+'_wheelBL' , carName+'_wheelBR' ]		 
				carBrakes			= [ carName+'_brakeFL' , carName+'_brakeFR' , carName+'_brakeBL' , carName+'_brakeBR' ]		 
				carContactLocators	= [ 'null_'+carName+'_contactFL' , 'null_'+carName+'_contactFR' , 'null_'+carName+'_contactBL' , 'null_'+carName+'_contactBR' ]
				rigWheels			= [ craftRigName+'WheelMesh_FLTransform' , craftRigName+'WheelMesh_FRTransform' , craftRigName+'WheelMesh_BLTransform' , craftRigName+'WheelMesh_BRTransform' ]
				rigWheelRelocators	= [ craftRigName+'WheelRelocatorMesh_FLTransform' , craftRigName+'WheelRelocatorMesh_FRTransform' , craftRigName+'WheelRelocatorMesh_BLTransform' , craftRigName+'WheelRelocatorMesh_BRTransform' ]
				rigWheelCenters		= [ craftRigName+'WheelCenterMesh_FLTransform' , craftRigName+'WheelCenterMesh_FRTransform' , craftRigName+'WheelCenterMesh_BLTransform' , craftRigName+'WheelCenterMesh_BRTransform' ]

				for i in range (0,4):
					cmds.xform ( carWheels[i] , centerPivots=True)	
					pos = cmds.xform ( carWheels[i] , query=True, rotatePivot=True , worldSpace=True )
					cmds.move ( pos[0],pos[1],pos[2], rigWheelRelocators[i] , worldSpace=True , absolute=True)
					cmds.move ( pos[0],cmds.getAttr ( carWheels[i]+'.boundingBoxMinY' ),pos[2], carContactLocators[i] , worldSpace=True , absolute=True)
	
					rigWheelDiametre = cmds.getAttr ( rigWheels[i]+'.boundingBoxSizeY' )
					carWheelDiametre = cmds.getAttr ( carWheels[i]+'.boundingBoxSizeY' ) 
	
					cmds.select ( rigWheelRelocators[i], replace=True )
					scaleValue = ( carWheelDiametre/rigWheelDiametre ) / cmds.getAttr (craftRigName+'CarBodyMeshTransform.scaleY') / cmds.getAttr ( rigWheelRelocators[i]+'.scaleY')
					cmds.scale ( scaleValue, scaleValue, scaleValue, relative=True )
	
					cmds.select ( rigWheels[i] , replace=True )
					cmds.select ( carWheels[i] , add=True )
	
					cmds.parentConstraint ( rigWheels[i] , carWheels[i] , maintainOffset=True , weight=1 )
					cmds.parentConstraint ( rigWheelCenters[i] , carBrakes[i] , maintainOffset=True , weight=1 )
					
				print 'Car Rigged. Success!'
			else:
				print 'Usage: Select valid car first then command click Craft rig.'
		else:
			print 'Usage: Select valid car first then command click Craft rig.'
	else:
		print 'Usage: Select valid car first then command click Craft rig.'
	
