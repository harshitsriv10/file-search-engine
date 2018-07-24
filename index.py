import re
import pickle
import os
from nltk import PorterStemmer
from ranker import *


def Stem(phrase):
	pattern = re.compile('[\W_]+')
	phrase = pattern.sub(' ',phrase)
	re.sub(r'[\W]+','',phrase)
	ListOfWords = phrase.split()
	# ListOfWords=Stem(phrase)
	# pos_deleted = []
	# for i in range(len(ListOfWords)):
	# 	if ListOfWords[i] in F:
	# 		pos_deleted.append(i)
	# pos_deleted = pos_deleted[::-1]

	# for i in pos_deleted:
	# 	# print(ListOfWords[i])
	# 	ListOfWords.pop(i)
	# for i in range(len(ListOfWords)):
		# ListOfWords[i] = PorterStemmer().stem(ListOfWords[i])
	return ListOfWords


def process_files(filenames):
	file_to_lines = {}
	for file in filenames:
		file_to_lines[file]=open(file,'r').read().lower();
		# p=re.compile(r'[^\s\.][^\.\n]+')
		file_to_lines[file] = file_to_lines[file].splitlines()
		# file_to_lines[file]=p.findall(file_to_lines[file])
		# print(file_to_lines[file])
	return file_to_lines


def index_one_file(termlist):
	fileIndex = {}
	for index, line in enumerate(termlist):
		# pattern = re.compile('[\W_]+')
		# line=pattern.sub(' ',line)
		# line=line.split()
		# print(line)
		line=Stem(line)
		# print(line)
		for word in line:
			if word in fileIndex.keys():
				fileIndex[word].append(index)
			else:
				fileIndex[word] = [index]
	return fileIndex

regdex = {}

def make_indices(filenames):
	termlists = {}
	for file in filenames:
		termlists[file]=open(file,'r').read().lower();
		# p=re.compile(r'[^\s\.][^\.\n]+')
		termlists[file] = termlists[file].splitlines()
		# file_to_lines[file]=p.findall(file_to_lines[file])
		# print(file_to_lines[file])
	# return file_to_lines

	# F = open('test1.txt','r')
	# F = F.readlines()
	# for i in range(len(F)):
	# 	F[i] = F[i].strip()
	# F = set(F)	
	# F = list(F)
	F = []
	for filename in termlists.keys():
			#
			fileIndex = {}
			for index, line in enumerate(termlists[filename]):
				line=Stem(line)
				for word in line:
					if word in fileIndex.keys():
						fileIndex[word].append(index)
					else:
						fileIndex[word] = [index]
			#
			regdex[filename] = fileIndex

def fullIndex():
	total_index = {}
	try:
		total_index = pickle.load(open("save.pkl","rb"))
	except:
		total_index = {}

	for filename in regdex.keys():
		for word in regdex[filename].keys():
			if word in total_index.keys():
				if filename in total_index[word].keys():
					total_index[word][filename].extend(regdex[filename][word][:])
				else:
					total_index[word][filename] = regdex[filename][word]
			else:
				total_index[word] = {filename: regdex[filename][word]}
	pickle.dump(total_index, open("save.pkl","wb"))
	return total_index

def newFiles():
	CurrentFiles = []
	try:
		with open('SavedList.pkl', 'rb') as f:
			CurrentFiles = pickle.load(f)
	except:
		CurrentFiles = []


	newList = []
	for root, directories, filenames in os.walk('data'):
		for filename in filenames:
			newList.append(os.path.join(root, filename))

	UpdatedFiles = []

	for file in newList:
		if not(file in CurrentFiles):
			UpdatedFiles.append(file)

	with open('SavedList.pkl', 'wb') as f:
		pickle.dump(newList, f)

	return UpdatedFiles



def SearchWord(word, InvertedIndex):
	pattern = re.compile('[\W_]+')
	word = pattern.sub(' ',word)
	if word in InvertedIndex.keys():
		return [file for file in InvertedIndex[word].keys()]
	else:
		return []

def SearchPhrase(phrase, InvertedIndex):
	# pattern = re.compile('[\W_]+')
	# phrase = pattern.sub(' ',phrase)
	# phrase = phrase.split()
	# phrase=Stem(phrase)
	# phrase = processString(phrase)
	lists = []
	result = {}
	for word in phrase:
		lists.append(SearchWord(word, InvertedIndex))
	settled = set(lists[0]).intersection(*lists)
	
	for i in settled:
		print(i)

	result2 = {}
	for file in settled:
		temp = []
		for word in phrase:
			temp.append(InvertedIndex[word][file][:])
		t = (set(temp[0])).intersection(*temp) 
		if(t):
			result[file] = list(t)
		t1 = (set(temp[0])).union(*temp)
		if(t1):
			result2[file] = list(t1)

	print(result) 
	#

	# for file in result.keys():
	# 	result[file] = score(result[file])
	#
	return (result, result2)

import time
filenames = newFiles()
for file in filenames:
	print(file)
document_list = pickle.load(open('SavedList.pkl', 'rb'))
# ans=process_files(filenames)
tic1 = time.clock()
# make_indices(filenames)
tic = time.clock()
print(tic-tic1)
# total_index = fullIndex()
# print(ans1)	
# ans2=fullIndex(ans1)
toc = time.clock()
print(toc-tic)
total_index = pickle.load(open('save.pkl', 'rb'))
print(total_index)
while (1):
	str = raw_input()
	# print(str)
	if(str==""):
		break
	str = Stem(str)
	anss=SearchPhrase(str,total_index)
	print(anss)
	rankFiles = Ranking(anss[0], total_index, str, document_list)
	print(rankFiles)
	for i in range(len(rankFiles)):
		if rankFiles[i][1] in anss[0].keys():
			print(rankFiles[i][1], anss[0][rankFiles[i][1]])

	if(len(anss[0]) == 0):
		print("No matches Found")
		for i in range(len(rankFiles)):
			if rankFiles[i][1] in anss[1].keys():
				print(rankFiles[i][1], anss[1][rankFiles[i][1]])



