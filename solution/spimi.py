from os import listdir
from collections import OrderedDict
import ast
import re

def spimi():
	#Open all the block files
	blockFiles = [open('DISK/' + i) for i in listdir('DISK/') if i.find('DS_Store') == -1]
	#Open the final index file
	indexFile = open('result/index.txt', 'a+') #python3 - (, encoding = "ISO-8859-1")

	firstLines = OrderedDict() # blockId:{term:[postings]}

	for blockFile in blockFiles:
		if 'BLOCK' in blockFile.name:
			blockFileID = getBlockFileID(blockFile)
			term = {}
			line = blockFile.readline()

			if not line == '':
				lineSplit = line.split(':')
				term = lineSplit[0]
				postings = ast.literal_eval(lineSplit[1])
				firstLines[blockFileID] = {term : postings}

	blocksEmpty = False #set to true when nothing is left in blocks

	while not blocksEmpty:
		lowestWordBlockIdTuple = min([[firstLines[i], i] for i in firstLines]) # get lowest term alphabetically, format [{term: [postings list]}, blockId]
		currentTerm = list(lowestWordBlockIdTuple[0].keys())[0]
		blocksWithThisTerm = [blockId for blockId in firstLines if currentTerm in [termKey for termKey in firstLines[blockId]]] # returns the blockIds of the blocks that have the same term at the top of their file
		combinedPostings = sorted(sum([pl[currentTerm] for pl in (firstLines[i] for i in blocksWithThisTerm)], []))
		indexFile.write(str(currentTerm) + ":" + str(combinedPostings) + "\n")

		for blockFileId in blocksWithThisTerm:
			blockFile = getBlockFileById(blockFileId, blockFiles)
			if blockFile: # if blockFile was found
				term = {}
				line = blockFile.readline()
				if not line == '':
					lineSplit = line.split(':')
					term = lineSplit[0]
					postings = ast.literal_eval(lineSplit[1])
					firstLines[blockFileId] = {term : postings}
				#else, remove blockFile from blockFiles list
				else:
					del firstLines[blockFileId]
					blockFiles.remove(getBlockFileById(blockFileId, blockFiles))
			else:
				print("remove")
				blockFiles.remove(getBlockFileById(blockFileId, blockFiles))
		if not blockFiles: #if blockFiles is completely empty
			blocksEmpty = True
	
	return 0


def getBlockFileID(blockFile):
	fileName = blockFile.name
	fileIDMatched = re.search('BLOCK(\d*).txt', fileName)
	if fileIDMatched:
		return int(fileIDMatched.group(1))

def getBlockFileById(usedBlockId, blockFiles):
	matchingFiles = [file for file in blockFiles if re.search('BLOCK' + str(usedBlockId), file.name)] # should be only one that matches
	if matchingFiles: # if not empty
		return matchingFiles[0]
	else:
		return False