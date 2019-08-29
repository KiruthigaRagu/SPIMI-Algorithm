import sys
import string
import nltk
from nltk.stem.porter import *
from collections import OrderedDict
import nltk_functions.word_tokenize
from nltk_functions.stemmer import PorterStemmer
import sys

def preprocess(documents, memorysize):

	tokenizer = nltk_functions.word_tokenize.Word_Tokenize()

	stopwords_30 = ['a', 'all', 'am', 'an', 'and', 'any', 'are', 'as', 'at', 'but',
					'by', 'do', 'each', 'for', 'from', 'in', 'into', 'is', 'no', 
					'nor', 'not', 'of', 'or', 'so', 'such', 'the', 'to', 'too', 'very', 'with']
	
	terms = []
	termPostingsList = {}
	filenameincrementer = 0
	terms_num_before_processing = 0
	terms_num_after_processing = 0
	
	for index, documentId in enumerate(documents):
		#if documentId > 300: break; # for testing on small sample
		
		# Step 1A: Tokenize
		tokens = tokenizer.word_tokenize(documents[documentId])
		# tokens = nltk.word_tokenize(documents[documentId])

		terms_num_before_processing += len(tokens)

		# Step 1B: Stem
		#tokens = [PorterStemmer().stem(i) for i in tokens]
		
		# stemmer = PorterStemmer()
		# tokens = [stemmer.stem(i) for i in tokens]
		
		#print("\nAfter stemming, the number of terms is: " + str(len(tokens)) + '\n')

		# Step 2: Normalize
		normalized = tokens

		normalized = [i for i in normalized if not i in string.digits] # remove numbers
		#print("Completed normalizing phase 1 - remove digits...")
		#print("\nAfter removing digits, the number of terms is: " + str(len(normalized)) + '\n')

		# normalized = [i for i in normalized if not i in stopwords.words('english')] #remove stopwords
		# normalized = [i for i in normalized if not i in stopwords_30] #remove stopwords

		#print("Completed normalizing phase 2 - remove stopwords...")
		#print("\nAfter removing stopwords, the number of terms is: " + str(len(normalized)) + '\n')
		
		normalized = [i.lower() for i in normalized] # lowercase
		#print("Completed normalizing phase 3 - lower tokens...")
		
		normalized = [i for i in normalized if not i in string.punctuation] # remove punctuation
		#print("Completed normalizing phase 4 - remove punctuation...")
		
		normalized = [i for i in normalized if not i == '``' and not i == "''"] # remove blank words
		#print("Completed normalizing phase 5 - remove blank words...")
		
		#Done normalizing document
		#print("Done normalizing document No. ", documentId)
		
		terms = normalized

		terms_num_after_processing += len(terms)
		
		# Create postings list for each term 
		for term in terms:
			if term in termPostingsList:
				# term is already in and has posting list. Append to existing PL
				if documentId not in termPostingsList[term]:
					termPostingsList[term].append(documentId)
			else:
				termPostingsList[term] = [documentId]

		# Sort before saving to block file.
		
		if (((sys.getsizeof(termPostingsList) / 1024 /1024) > memorysize) or 
			(index == len(documents)-1)): #or if we're up to the last document
			# sort termPostingsList
			sortedTerms = sorted(termPostingsList)
			termPostingsListSorted = OrderedDict()
			for item in sortedTerms:
				termPostingsListSorted[item] = termPostingsList[item]	
			termPostingsList = termPostingsListSorted
			termPostingsListSorted = {}
		
			# write to file every one hundred docs
			with open('DISK/BLOCK' + str(filenameincrementer) + ".txt", 'a+') as file:
				filenameincrementer += 1
				for plIndex, term in enumerate(termPostingsList):		
					file.write(str(term) + ":" + str(termPostingsList[term]) + "\n")
			terms = []
			termPostingsList = {}

	# print("\nBefore preprocessing, the number of terms is: " + str(terms_num_before_processing) + '\n')	
	# print("\nAfter preprocessing, the number of terms is: " + str(terms_num_after_processing) + '\n')	