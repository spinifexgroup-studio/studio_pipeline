#!/usr/bin/python
#spck_aepx_maker.py
#
#Takes template spck .aepx file and changes all expressions and composition names to new shot name

import binascii
import re
import os
import pymel.core as pm
import maya.cmds as mc
import sys

#def spckMakeAepx (replacementShotName):
	
templateShotName	= 'shXXXX'
replacementShotName = str(input('New Shot Name (characters and numbers and underscore only - no spaces - enlose in single quotes): '))
replacementShotPath = "~/Desktop/spck_v0.3_"+replacementShotName+"_new_shot_v001.aepx"
replacementShotPath = os.path.expanduser(replacementShotPath)

fileIn  = open("/Volumes/RESOURCES/05_Motion_Studio_Tools/spck/aepx/spck_v0.3_shXXXX.aepx")
fileOut = open(replacementShotPath, "wt")

for line in fileIn:
	# for each line in file, search for the shot name and replace with new shot name
	# some of the shot names are hidden in binary data in bdata = "hex data" lines
	# if no shot name found in line, write out original line
	
	if templateShotName in line:
		fileOut.write( line.replace(templateShotName, replacementShotName))
		#print line
	elif 'bdata' in line:
		#for each bdata line, find the binary data between the quotes, and unhex it
		#strip the quotes "" from the extracted data
		#search for the shot name and replace if found
		#write out new line if data was replaced otherwise write out old line
		
		bData = re.search (r'"(.*?)"' , line)
		bDataNoQuotes = bData.group(0).replace('"', '').strip()
		asciiData = binascii.unhexlify(bDataNoQuotes)
		if templateShotName in asciiData:
			asciiData = asciiData.replace (templateShotName, replacementShotName)
			replacementData = binascii.hexlify(asciiData)
			line = line.replace(bDataNoQuotes, replacementData)
			#print asciiData
		fileOut.write(line)
	else:
		fileOut.write(line)
		
#Be nice and close the files

fileIn.close()
fileOut.close()