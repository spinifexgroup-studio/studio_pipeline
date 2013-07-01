import nuke, nukescripts, os

# ASk user for proxy type
def BuildInterface():
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
	return proxyType
	
	
# Get Proxy path based on type of proxy
def GetProxyPath (node, proxyType):
	filePath = node.knob('file').value().replace('\\','/')
	proxyPath = ''
	fileDir = os.path.dirname(filePath)
	fileBase = os.path.basename(filePath)
	# Proxies in sub directory
	if proxyType == 'sub':
		proxyPath = os.path.join ( fileDir, 'proxy', fileBase )
	# Proxies in same directory
	if proxyType == 'same':
		if '.%' in fileBase:
			fileBase = fileBase.split('.%',1)[0] + '_proxy' + '.%' + fileBase.split('.%',1)[1]
		else:
			fileBase, fileExt = os.path.splitext (fileBase)
			fileBase = fileBase + '_proxy' + fileExt
		proxyPath = os.path.join ( fileDir, fileBase )
	# Proxies in parent directory
	if proxyType == 'parent':
		proxyPath = os.path.join ( os.path.dirname( fileDir ), os.path.basename( fileDir )+'_proxy', fileBase )
	return proxyPath
	
# Sets the proxy path of a read node according to spinifex standards
def SetReadProxies():
	# Check to see if nodes are selected
	nodes = nuke.selectedNodes()
	if nodes:
		validNodeSelected = False
		for node in nodes:
			if node.Class() == 'Read':
				validNodeSelected = True
		if validNodeSelected:
			proxyType = BuildInterface()
			for node in nodes:
				if node.Class() == 'Read':
					# Set the proxy
					proxyPath = GetProxyPath ( node, proxyType )
					node.knob('proxy').setValue(proxyPath)
		else:
			nuke.message('No Read Nodes Selected!')
	else:
		nuke.message('Nothing Selected!')

		
# Sets the proxy path of a write node according to spinifex standards
def SetWriteProxies():
	# Check to see if nodes are selected
	nodes = nuke.selectedNodes()
	if nodes:
		validNodeSelected = False
		for node in nodes:
			if node.Class() == 'Write':
				validNodeSelected = True
		if validNodeSelected:
			proxyType = BuildInterface()
			for node in nodes:
				if node.Class() == 'Write':
					# Set the proxy
					proxyPath = GetProxyPath ( node, proxyType )
					if not os.path.exists ( os.path.dirname(proxyPath)):
						os.makedirs (os.path.dirname(proxyPath))
					node.knob('proxy').setValue(proxyPath)
		else:
			nuke.message('No Read Nodes Selected!')
	else:
		nuke.message('Nothing Selected!')


