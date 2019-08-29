import sys
import reuters
from preprocess import preprocess
from spimi import spimi
import query as q


def generateindex(memorysize):

	extractFunctions = reuters.Extract();
	
	print("\n--------------------------------------------")
	# Step 1: Get Documents
	print("Fetching Documents...\n")
	documents = extractFunctions.getDocuments()
	# print '   --> Total number of documents before preprocessing: ' + str(len(documents)) + '\n'
	
	# Step 2: Tokenize/Normalize/Remove Stopwords and then Save Blocks
	print("Preprocessing and saving blocks...\n")
	preprocess(documents, memorysize)

	# Step 3: SPIMI algorithm
	print("Performing SPIMI...\n")
	spimi()
	
	print("Complete.")
	print("--------------------------------------------\n")

def query():
	query = q.SPIMIQuery()
	while True: # keep running the program 
		keyword = raw_input("\nPlease enter your query, using AND / OR for boolean queries  \n")
		print("\nYou entered: \"" + keyword + "\"")
		result = query.runQuery(keyword)

if __name__ == '__main__':
	generateindex(int(sys.argv[1]))
	query()