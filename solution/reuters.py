import re
import os

class Extract:

	REUTERS_START_TAG = "<REUTERS"
	BODY_START_TAG = "<BODY>"
	BODY_END_TAG = "</BODY>"

	SGM_FILE_PATH = "reuters_corpus/"

	#Obtain each sgm file in the data directory and store them in an array
	def getSGMFiles(self):
		sgmFiles = []
		files = os.listdir(self.SGM_FILE_PATH)
		for file in files:
			if ".sgm" in str(file):
				sgmFiles.append(str(file))
		return sgmFiles
	#Iterate each sgm file and extract their content in the body tag.
	def getDocuments(self):
		documents = {}
		body = ""

		#Iterate each sgm file
		for fileName in self.getSGMFiles():
			with open(self.SGM_FILE_PATH + fileName) as file:
				count = 0
				body = ""

				bodyIsOpen = False
				currentReutersID = -1

				#Iterate each line
				for line in file:
					count += 1

					# if count > 50: break #just for quick testing

					if bodyIsOpen:
						#Look for the end of body tag
						lastLineInBody = line.find(self.BODY_END_TAG)
						if lastLineInBody != -1:
							body += line[ : lastLineInBody]
							documents[currentReutersID] = body
							body = ""
							bodyIsOpen = False
							currentReutersID = -1
						else:
							body += line
					else:
						#Look for the beginning of reuters tag
						reuterStart = line.find(self.REUTERS_START_TAG)

						if reuterStart != -1:
							#Get NEWID attribute
							currentReutersID = int(re.search("NEWID=\"(\d*)", line).group(1))
						#Look for the beginning of body tag
						bodyStart = line.find(self.BODY_START_TAG)

						if bodyStart != -1:
							bodyIsOpen = True
							firstLineInBody = line[bodyStart + len(self.BODY_START_TAG) : ]
							lastLineInBody = firstLineInBody.find(self.BODY_END_TAG)

							if lastLineInBody != -1:
								body = firstLineInBody[ : lastLineInBody]
								documents[currentReutersID] = body
								bodyIsOpen = False
								body = ""
								currentReutersID = -1
							else:
								body += firstLineInBody

		return documents

# test = Extract()
# doc = test.getDocuments()

# for kv in doc.items():
# 	print(kv)

# print(len(doc))
