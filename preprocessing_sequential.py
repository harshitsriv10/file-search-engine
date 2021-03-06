import re
import pickle
import os
from nltk import PorterStemmer
# from ranker import *
import time
from math import *
# from nltk import stopwords

def normalize(freqList):
	den = 0
	for num in freqList:
		den = den + num*num
	den = sqrt(den)
	if(den == 0):
		return freqList
	for i in range(len(freqList)):
		freqList[i] = freqList[i]/den
	return freqList

def Stem(phrase):
	phrase = phrase.lower()
	pattern = re.compile('[\W_]+')
	phrase = pattern.sub(' ',phrase)
	re.sub(r'[\W]+','',phrase)
	ListOfWords = phrase.split()
	# for word in phrase.split():
		# ListOfWords.append(PorterStemmer().stem(word))
	return ListOfWords


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def newFiles():
	try:
		with open('SavedList.pkl', 'rb') as f:
			CurrentFiles = pickle.load(f)
	except:
		CurrentFiles = []

	newList = []
	for root, directories, filenames in os.walk('data'):
		for filename in filenames:
			newList.append(filename)

	UpdatedFiles = []
	for file in newList:
		if not(file in CurrentFiles):
			UpdatedFiles.append(file)

	with open('SavedList.pkl', 'wb') as f:
		pickle.dump(newList, f)
	return UpdatedFiles

def make_indices(filenames):
	termlists = {}
	F = open('test1.txt','r')
	F = F.readlines()
	for i in range(len(F)):
		F[i] = F[i].strip()
	F = set(F)	
	root = "/home/harshitsriv/Downloads/Python_google_search/data/"
	try:
		total_index = pickle.load(open("save.pkl","rb"))
	except:
		total_index = {}
	for filename in filenames:
		#
		termlists= open(os.path.join(root, filename),'r').readlines()
		# print(termlists)
		# fileIndex = {}
		for index, line in enumerate(termlists):
			line=Stem(line)
			# print(line)
			for word in line:
				if not(word in F):
					if word in total_index.keys():
						if filename in total_index[word].keys():
							total_index[word][filename].append(index)
						else:
							total_index[word][filename] = [index]
							total_index[word][filename].append(index)
					else:
						total_index[word] = {filename: [index]}


	pickle.dump(total_index, open("save.pkl","wb"))
	return total_index

def make_indices_seq(filenames):
	termlists = {}
	F = open('test1.txt','r')
	F = F.readlines()
	for i in range(len(F)):
		F[i] = F[i].strip()
	F = set(F)	
	root = "/home/harshitsriv/Downloads/Python_google_search/data/"
	try:
		total_index = pickle.load(open("save_seq.pkl","rb"))
	except:
		total_index = {}
	for filename in filenames:
		pattern = re.compile('[\W_]+')
		termlists= open(os.path.join(root,filename),'r').read().lower()
		termlists= pattern.sub(' ',termlists)
		re.sub(r'[\W_]+','', termlists)
		termlists=termlists.split()
		#print(termlists)
		# fileIndex = {}
		for index, line in enumerate(termlists):
			line=Stem(line)
			# print(line)
			for word in line:
				if not(word in F):
					if word in total_index.keys():
						if filename in total_index[word].keys():
							total_index[word][filename].append(index)
						else:
							total_index[word][filename] = [index]
							total_index[word][filename].append(index)
					else:
						total_index[word] = {filename: [index]}


	pickle.dump(total_index, open("save_seq.pkl","wb"))
	return total_index

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

def rank_finder(inverted_index, document_list):
	unique_word_count = len(inverted_index)
	no_documents = len(document_list)
	document_weight = []
	mapping = {}
	i = 0
	for document in document_list:
		mapping[i] = document
		i+=1
		temp_list = []
		j = 0
		for word in inverted_index.keys():
			# print(word)
			mapping[word] = j
			j += 1
			if document in inverted_index[word].keys():
				temp_list.append(len(inverted_index[word][document]))
			else:
				temp_list.append(0)
		temp_list = normalize(temp_list)
		document_weight.append(temp_list)

	j = 0
	for word in inverted_index.keys():
		idf = log(1+(no_documents/len(inverted_index[word])))
		for i in range(no_documents):
			document_weight[i][j] *= idf
		j+=1

	for i in range(len(document_weight)):
		document_weight[i] = normalize(document_weight[i])	
	print(document_weight)
	pickle.dump(document_weight, open("ranking.pkl","wb"))
	pickle.dump(mapping, open("mapping.pkl","wb"))


def rank_finder_seq(inverted_index, document_list):
	unique_word_count = len(inverted_index)
	no_documents = len(document_list)
	document_weight = []
	mapping = {}
	i = 0
	for document in document_list:
		mapping[i] = document
		i+=1
		temp_list = []
		j = 0
		for word in inverted_index.keys():
			# print(word)
			mapping[word] = j
			j += 1
			if document in inverted_index[word].keys():
				temp_list.append(len(inverted_index[word][document]))
			else:
				temp_list.append(0)
		temp_list = normalize(temp_list)
		document_weight.append(temp_list)

	j = 0
	for word in inverted_index.keys():
		idf = log(1+(no_documents/len(inverted_index[word])))
		for i in range(no_documents):
			document_weight[i][j] *= idf
		j+=1

	for i in range(len(document_weight)):
		document_weight[i] = normalize(document_weight[i])	
	print(document_weight)
	pickle.dump(document_weight, open("ranking_seq.pkl","wb"))
	pickle.dump(mapping, open("mapping_seq.pkl","wb"))


def run():
	filenames = newFiles()
	tic1 = time.clock()
	total_index = make_indices(filenames)
	total_index_seq = make_indices_seq(filenames)
	#print(total_index)
	#print(total_index_seq)
	try:
		with open('SavedList.pkl', 'rb') as f:
			CurrentFiles = pickle.load(f)
	except:
		CurrentFiles = []
	rank_finder(total_index, CurrentFiles)
	rank_finder_seq(total_index_seq, CurrentFiles)
	tic = time.clock()
	print(tic-tic1)

run()