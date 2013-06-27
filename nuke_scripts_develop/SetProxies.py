import nuke, nukescripts, os

def SetReadProxies():

	nodes = nuke.selectedNodes()
	if nodes:
		panel = nuke.Panel('Proxy Type')
		panel.addEnumerationPulldown( 'Proxy Type', '"Sub Directory: filedir/proxy/filename" "Same Directory: filedir/filename_proxy" "Parent Directory: filedir_proxy/filename"' )
		panel.show()

		proxyType = 'same'

		if panel.value('Proxy Type') == "Sub Directory: filedir/proxy/filename":
			proxyType = 'sub'
		if panel.value('Proxy Type') == "Same Directory: filedir/filename_proxy":
			proxyType = 'same'
		if panel.value('Proxy Type') == "Parent Directory: filedir_proxy/filename":
			proxyType = 'parent'

		for node in nodes:
			if node.Class() == 'Read':
				filePath = node.knob('file').value().replace('\\','/')
				proxyPath = ''
				fileDir = os.path.dirname(filePath)
				fileBase = os.path.basename(filePath)
				if proxyType == 'sub':
					proxyPath = os.path.join ( fileDir, 'proxy', fileBase )
			
				if proxyType == 'same':
					fileBase = fileBase.split('.%',1)[0] + '_proxy' + '.%' + fileBase.split('.%',1)[1]
					proxyPath = os.path.join ( fileDir, fileBase )
			
				if proxyType == 'parent':
					proxyPath = os.path.join ( os.path.dirname( fileDir ), os.path.basename( fileDir )+'_proxy', fileBase )
		
				node.knob('proxy').setValue( proxyPath)
	else:
		nuke.message('Nothing Selected!')