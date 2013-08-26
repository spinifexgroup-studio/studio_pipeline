channelSearchStrings = ["lighting", "lightselect", "GI", "diffuse","reflect", "refract", "specular", "selfIllum","sss"]
nodeXOffset = 200
nodeYOffset = 180
noOpTileColor = 0x9b00ff
allSelectedNodes = nuke.selectedNodes()

#iterate through all selected nodes
for selectedNode in allSelectedNodes:
    xPosMin = selectedNode['xpos'].value()
    yPosMin = selectedNode['ypos'].value()

    channelsDict = {}
    allChannels = selectedNode.channels()

    # Make a dictionary with all the channels and push into allChannels Array
    for channel in allChannels:
        thisData = str(channel.split('.')[0])
        channelsDict.update({thisData:''})
        allChannels = channelsDict.keys()

    # Run Through the dictionary and find only the channels we're after
    # We iterate like this to find multiple light selects or specs
    channelsToComp = []
    for searchString in channelSearchStrings:
        searchString = searchString.lower()
        for channel in allChannels:
            if channel.lower().find(searchString) > -1:
                print channel
                channelsToComp.append(channel)

    nodeNumber = -1
    mergeNumber = 2
    noOpNodes = []
    for channel in channelsToComp:
        nodeNumber += 1

        # Shuffle the channel into RGB but keep the alpha from RGBA
        shuffleNode = nuke.nodes.Shuffle(name = ("%s_shuffle" % channel), postage_stamp = True, out="rgb")
        shuffleNode.setXYpos ( xPosMin+nodeNumber*nodeXOffset,yPosMin+nodeYOffset)
        shuffleNode.setInput(0, selectedNode)
        shuffleNode['in'].setValue(channel)

        #make a noOp node for the header
        noOpNode = nuke.nodes.NoOp(name=channel, tile_color=noOpTileColor)
        noOpNode.setXYpos ( xPosMin+nodeNumber*nodeXOffset,yPosMin+1.5*nodeYOffset)
        noOpNode.setInput(0, shuffleNode)
        noOpNode.setXYpos ( xPosMin+nodeNumber*nodeXOffset,yPosMin+1.5*nodeYOffset)

        dotNode
        if nodeNumber > 0 and channel != "diffuse":
            #make a dot node for end of pipes
            dotNode = nuke.nodes.Dot(note_font_size=20)
            dotNode['label'].setValue(channel)
            dotNode.setXYpos ( xPosMin+nodeNumber*nodeXOffset+35,yPosMin+(mergeNumber+1)*nodeYOffset)
            dotNode.setInput(0,noOpNode)

            mergeNumber += 1
            mergeNode = nuke.nodes.Merge( name  = ("%s_merge" % channel), operation='plus',A='rgb');
            mergeNode.setXYpos ( xPosMin,yPosMin+(mergeNumber)*nodeYOffset)
            mergeNode.setInput(1,dotNode);
            if nodeNumber > 1:
                mergeNode.setInput(0,previousMergeNode);
            else:
                mergeNode.setInput(0,previousNoOpNode);

        if channel != "diffuse" and channel.lower().find("lightselect") < 0:
            noOpNodes.append(noOpNode)
               
        previousMergeNode = mergeNode;
        previousNoOpNode = noOpNode;

    allPassesMergeNode = nuke.nodes.Merge2( name  = "colourChannels_merge", operation='plus', hide_input = True, A='rgb');
    allPassesMergeNode.setXYpos ( xPosMin+(nodeNumber+1)*nodeXOffset,yPosMin)
    inputCount = 0
    for noOpNode in noOpNodes:
        allPassesMergeNode.setInput(inputCount,noOpNode)
        inputCount += 1
        if inputCount == 2: inputCount += 1 #skip the mask input

    extraInfoMerge = nuke.nodes.Merge( name  = ("%s_merge" % channel), operation='minus', postage_stamp = True, A='rgb');
    extraInfoMerge.setXYpos ( xPosMin+(nodeNumber+1)*nodeXOffset,yPosMin+nodeYOffset)
    extraInfoMerge.setInput(0,selectedNode)            
    extraInfoMerge.setInput(1,allPassesMergeNode)            
         
        