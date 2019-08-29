import os
import fileops

class SPIMIQuery:
	
	def __init__(self):
	 	self.index = fileops.readIndexIntoMemory()

	def runQuery(self, keyword):
		# Parse keyword
		terms = self.parseQuery(keyword)

		if ' or ' in keyword.lower():
			operation = 'OR'
		elif ' and ' in keyword.lower():
			operation = 'AND'
		elif terms:
			operation = 'None, it\'s a single word query'
		else:
			operation = 'Nothing input'
		
		print '\nYour Operation Is: ' + operation

		print '\nYour Terms Are:'
		for i, term in enumerate(terms):
			print str((i + 1)) + ": " + term
		print "" # blank line to skip to next line

		# Collect Postings Lists
		listOfPostingsList = [[]]
		for term in terms:
			term_with_dot = term + '.'
			if term in self.index:
				listOfPostingsList.append(self.index[term])
			if term_with_dot in self.index:
				if len(listOfPostingsList) != 1:
					for item in self.index[term_with_dot]:
						listOfPostingsList[len(listOfPostingsList)-1].append(item)
				else:
					listOfPostingsList.append(self.index[term_with_dot])
		del listOfPostingsList[0] # delete the blank array initializer so as not to mess up intersection calculation

		# find intersections
		if listOfPostingsList: # not empty
			if operation == 'OR':
				results = list(set.union(*map(set, listOfPostingsList)))
			elif len(listOfPostingsList) == len(terms):
				results = list(set.intersection(*map(set, listOfPostingsList)))
			else:
				results = []
		else: 
			results = []
		
		print "----------------------------------------------------"
		if len(results) == 0: # not empty
			print "Your search - \" " + keyword + " \" - did not match any documents"
		else:
			print "Document Results: ", sorted(results)
		print "----------------------------------------------------\n"
		
		#print [i for i in self.index[term] for term in terms]
		
	# Currently, words must be separated by single AND to be parse correctly
	def parseQuery(self, keyword):
		lower = keyword.lower()
		if ' or ' in lower:
			return lower.split(' or ')
		else:
			return lower.split(' and ')