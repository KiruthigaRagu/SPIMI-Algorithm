from collections import OrderedDict
import ast
import os
			
def readIndexIntoMemory():
	index = OrderedDict()
	# Open Index File
	indexFile = open("result/index.txt")
	for line in indexFile:
		if not line == '':
			split = line.split(':')
			term = split[0]
			postings = ast.literal_eval(split[1]) # convert a string list to a list
			index.update({term: postings})
			
	# Generate some stats about imported index
	postingsCount = 0
	# print 'Size of index: ' + str(len(index)) + '\n'
	for i in index:
		postingsCount += len(index[i])
	# print 'Number of total postings: ' + str(postingsCount) + '\n'
	
	return index