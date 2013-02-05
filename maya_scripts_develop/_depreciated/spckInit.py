# Load SPCK commands

import maya.cmds as cmds
import os, sys

def setupSpckPipeline():
	import spck
	
cmds.evalDeferred ( 'setupSpckPipeline()' , lowestPriority = True )	