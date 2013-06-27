import nuke, nukescripts, os


# Sets the proxy path of a read node according to spinifex standards
def SetReadProxies():
	# Check to se if nodes are selected
	nodes = nuke.selectedNodes()
	if nodes:
		# Build Interface
		panel = nuke.Panel('Proxy Type')
		panel.addEnumerationPulldown( 'Proxy Type', '"Sub Directory: filedir/proxy/filename" "Same Directory: filedir/filename_proxy" "Parent Directory: filedir_proxy/filename"' )
		panel.show()

		# Get Proxy type
		proxyType = 'same'
		if panel.value('Proxy Type') == "Sub Directory: filedir/proxy/filename":
			proxyType = 'sub'
		if panel.value('Proxy Type') == "Same Directory: filedir/filename_proxy":
			proxyType = 'same'
		if panel.value('Proxy Type') == "Parent Directory: filedir_proxy/filename":
			proxyType = 'parent'

		# Iterate through read nodes and set proxy path
		for node in nodes:
			if node.Class() == 'Read':
				filePath = node.knob('file').value().replace('\\','/')
				proxyPath = ''
				fileDir = os.path.dirname(filePath)
				fileBase = os.path.basename(filePath)
				# Proxies in sub directory
				if proxyType == 'sub':
					proxyPath = os.path.join ( fileDir, 'proxy', fileBase )
				# Proxies in same directory
				if proxyType == 'same':
					fileBase = fileBase.split('.%',1)[0] + '_proxy' + '.%' + fileBase.split('.%',1)[1]
					proxyPath = os.path.join ( fileDir, fileBase )
				# Proxies in parent directory
				if proxyType == 'parent':
					proxyPath = os.path.join ( os.path.dirname( fileDir ), os.path.basename( fileDir )+'_proxy', fileBase )
				# Set the proxy
				node.knob('proxy').setValue( proxyPath)
	else:
		nuke.message('Nothing Selected!')