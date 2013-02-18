# Car.py
# Version 0.1
# By Daniel Harkness

import maya.cmds as cmds
import maya.utils as utils
import maya.mel as mel

class Car(object):
	def __init__ (self, name='spckCar '):
		self.name = self.promptName()
		self.createGroups ()
		
		
	def promptName (self):
		# Ask for a name for the car.
		dialogMessage = 'Enter name of car:'
		result = cmds.promptDialog( title='spck', message=dialogMessage, button=['OK','Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel' )
		if result == 'OK':
			carName = cmds.promptDialog (query=True, text=True)
			if len (carName) > 0:
				return str(carName)

	def createGroups (self):
		# Setup object names
		body			= self.name + '_body'
		exterior		= self.name + '_exterior'
		interior		= self.name + '_interior'
		headLights		= self.name + '_headLights'
		tailLights		= self.name + '_tailLights'
		fogLights		= self.name + '_fogLights'
		sideLights		= self.name + '_sideLights'
		
		wheels			= self.name + '_wheels'
		wheelFL			= self.name + '_wheelFL'
		wheelFR			= self.name + '_wheelFR'
		wheelBL			= self.name + '_wheelBL'
		wheelBR			= self.name + '_wheelBR'
		brakeFL			= self.name + '_brakeFL'
		brakeFR			= self.name + '_brakeFR'
		brakeBL			= self.name + '_brakeBL'
		brakeBR			= self.name + '_brakeBR'
		
		headLightL		= 'null_' + self.name + '_headLightL1'
		headLightR		= 'null_' + self.name + '_headLightR1'
		fogLightL		= 'null_' + self.name + '_fogLightL1'
		fogLightR		= 'null_' + self.name + '_fogLightR1'
		tailLightL		= 'null_' + self.name + '_tailLightL1'
		tailLightR		= 'null_' + self.name + '_tailLightR1'
		contactFL		= 'null_' + self.name + '_contactFL'
		contactFR		= 'null_' + self.name + '_contactFR'
		contactBL		= 'null_' + self.name + '_contactBL'
		contactBR		= 'null_' + self.name + '_contactBR'
		
		# Setup Nulls
		locatorArray = []
		
		locatorArray.append (cmds.spaceLocator ( name = headLightL 	, position = ( 50 , 45 , 150 )))
		locatorArray.append (cmds.spaceLocator ( name = headLightR 	, position = ( -50 , 45 , 150 )))
		locatorArray.append (cmds.spaceLocator ( name = fogLightL 	, position = ( 50 , 30 , 150 )))
		locatorArray.append (cmds.spaceLocator ( name = fogLightR 	, position = ( -50 , 30 , 150 )))
		locatorArray.append (cmds.spaceLocator ( name = tailLightL 	, position = ( 50 , 65 , -170 )))
		locatorArray.append (cmds.spaceLocator ( name = tailLightR 	, position = ( -50 , 65 , -170 )))
		locatorArray.append (cmds.spaceLocator ( name = contactFL 	, position = ( 70 , 0 , 100 )))
		locatorArray.append (cmds.spaceLocator ( name = contactFR 	, position = ( -70 , 0 , 100 )))
		locatorArray.append (cmds.spaceLocator ( name = contactBL 	, position = ( 70 , 0 , -120 )))
		locatorArray.append (cmds.spaceLocator ( name = contactBR 	, position = ( -70 , 0 , -120 )))
		
		# Scale Nulls and set axis correctly		
		for locator in locatorArray:
			cmds.select ( locator[0] )
			locatorShape = cmds.pickWalk ( direction = 'down' )
			cmds.setAttr ( locator[0]+'.translateX' , cmds.getAttr ( locatorShape[0]+'.localPositionX' ))
			cmds.setAttr ( locator[0]+'.translateZ' , cmds.getAttr ( locatorShape[0]+'.localPositionZ' ))
			cmds.setAttr ( locatorShape[0]+'.localPositionX' , 0 )
			cmds.setAttr ( locatorShape[0]+'.localPositionZ' , 0 )
			cmds.xform ( locator[0] , centerPivots = True )
			cmds.setAttr ( locator[0]+'.localScaleX' , 10 )
			cmds.setAttr ( locator[0]+'.localScaleY' , 10 )
			cmds.setAttr ( locator[0]+'.localScaleZ' , 10 )

		# Annotate Wheel positions
		annotation = cmds.annotate( contactFL , point= (150,0,150) , text='FL' )
		cmds.select (annotation)
		cmds.pickWalk ( direction = 'up')
		cmds.rename ( self.name+'annotationFL' )
		cmds.parent ( self.name+'annotationFL' , contactFL )
		
		annotation = cmds.annotate( contactFR , point= (-150,0,150) , text='FR' )
		cmds.select (annotation)
		cmds.pickWalk ( direction = 'up')
		cmds.rename ( self.name+'annotationFR' )
		cmds.parent ( self.name+'annotationFR' , contactFR )


		annotation = cmds.annotate( contactBL , point= (150,0,-150) , text='BL' )
		cmds.select (annotation)
		cmds.pickWalk ( direction = 'up')
		cmds.rename ( self.name+'annotationBL' )
		cmds.parent ( self.name+'annotationBL' , contactBL )


		annotation = cmds.annotate( contactBR , point= (-150,0,-150) , text='BR' )
		cmds.select (annotation)
		cmds.pickWalk ( direction = 'up')
		cmds.rename ( self.name+'annotationBR' )
		cmds.parent ( self.name+'annotationBR' , contactBR )


		
		# Group Structure
		alloy = '_alloy'
		tyre = '_tyre'
		
		
		cmds.group ( em=True, name = wheelFL+alloy )
		cmds.group ( em=True, name = wheelFL+tyre )
		cmds.group ( em=True, name = wheelFR+alloy )
		cmds.group ( em=True, name = wheelFR+tyre )
		cmds.group ( em=True, name = wheelBL+alloy )
		cmds.group ( em=True, name = wheelBL+tyre )
		cmds.group ( em=True, name = wheelBR+alloy )
		cmds.group ( em=True, name = wheelBR+tyre )
		cmds.group ( wheelFL+alloy , wheelFL+tyre , name = wheelFL )
		cmds.group ( wheelFR+alloy , wheelFR+tyre , name = wheelFR )
		cmds.group ( wheelBL+alloy , wheelBL+tyre , name = wheelBL )
		cmds.group ( wheelBR+alloy , wheelBR+tyre , name = wheelBR )
		cmds.group ( contactFL , name = brakeFL )
		cmds.group ( contactFR , name = brakeFR )
		cmds.group ( contactBL , name = brakeBL )
		cmds.group ( contactBR , name = brakeBR )
		cmds.group ( em=True, name = exterior )
		cmds.group ( em=True, name = interior )
		cmds.group ( headLightL , headLightR , name = headLights )
		cmds.group ( tailLightL , tailLightR , name = tailLights )
		cmds.group ( fogLightL , fogLightR , name = fogLights )
		cmds.group ( em=True, name = sideLights )
		
		cmds.group ( wheelFL , wheelFR , wheelBL , wheelBR , brakeFL , brakeFR , brakeBL , brakeBR , name = wheels )
		cmds.group ( headLights , tailLights , fogLights , sideLights , exterior , interior , name = body )
		cmds.group ( wheels , body , name = self.name )
		
		# Set object IDs on wheels and Lights
		
		mel.eval('vrayAddAttr ' + tailLights + ' vrayObjectID')
		mel.eval('vrayAddAttr ' + fogLights + ' vrayObjectID')
		mel.eval('vrayAddAttr ' + sideLights + ' vrayObjectID')
		mel.eval('vrayAddAttr ' + headLights + ' vrayObjectID')

		mel.eval('vrayAddAttr ' + wheelFL+alloy + ' vrayObjectID')
		mel.eval('vrayAddAttr ' + wheelFL+tyre + ' vrayObjectID')
		mel.eval('vrayAddAttr ' + wheelFR+alloy + ' vrayObjectID')
		mel.eval('vrayAddAttr ' + wheelFR+tyre + ' vrayObjectID')
		mel.eval('vrayAddAttr ' + wheelBL+alloy + ' vrayObjectID')
		mel.eval('vrayAddAttr ' + wheelBL+tyre + ' vrayObjectID')
		mel.eval('vrayAddAttr ' + wheelBR+alloy + ' vrayObjectID')
		mel.eval('vrayAddAttr ' + wheelBR+tyre + ' vrayObjectID')
		mel.eval('vrayAddAttr ' + brakeFL + ' vrayObjectID')
		mel.eval('vrayAddAttr ' + brakeFR + ' vrayObjectID')
		mel.eval('vrayAddAttr ' + brakeBL + ' vrayObjectID')
		mel.eval('vrayAddAttr ' + brakeBR + ' vrayObjectID')
		
		cmds.setAttr ( tailLights+'.vrayObjectID' , 4 )
		cmds.setAttr ( fogLights+'.vrayObjectID' , 5 )
		cmds.setAttr ( sideLights+'.vrayObjectID' , 5 )
		cmds.setAttr ( headLights+'.vrayObjectID' , 6 )

		cmds.setAttr ( brakeFL+'.vrayObjectID' , 10 )
		cmds.setAttr ( brakeFR+'.vrayObjectID' , 10 )
		cmds.setAttr ( brakeBL+'.vrayObjectID' , 10 )
		cmds.setAttr ( brakeBR+'.vrayObjectID' , 10 )
		cmds.setAttr ( wheelFL+tyre+'.vrayObjectID' , 11 )
		cmds.setAttr ( wheelFL+alloy+'.vrayObjectID' , 12 )
		cmds.setAttr ( wheelFR+tyre+'.vrayObjectID' , 11 )
		cmds.setAttr ( wheelFR+alloy+'.vrayObjectID' , 12 )
		cmds.setAttr ( wheelBL+tyre+'.vrayObjectID' , 11 )
		cmds.setAttr ( wheelBL+alloy+'.vrayObjectID' , 12 )
		cmds.setAttr ( wheelBR+tyre+'.vrayObjectID' , 11 )
		cmds.setAttr ( wheelBR+alloy+'.vrayObjectID' , 12 )
		
		cmds.select ( self.name , replace = True )
		cmds.addAttr ( longName='isCar', attributeType='message' )			

	