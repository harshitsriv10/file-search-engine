from math import *
import pickle


def comp(elem):
	return elem[2]

def comp1(elem):
	return elem[0]

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

def score(FileList):
	start = FileList[0]
	end = start
	count = 0
	paragraphs = []

	for line in FileList:
		if(line-end <= 2):											#parameter importance
			end = line
			count+=1
		else:
			paragraphs.append((start, end, count))
			start = end = line
			count = 1

	paragraphs.append((start, end, count))

	paragraphs.sort(key=comp, reverse=True)
	return paragraphs

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
	# print(document_weight)
	pickle.dump(document_weight, open("ranking.pkl","wb"))
	pickle.dump(mapping, open("mapping.pkl","wb"))
	return (document_weight,mapping)


def queryRank(inverted_index, QueryWords, document_list):
	queryFreq = []
	no_documents = len(document_list)

	try:
		document_weight = pickle.load(open("ranking.pkl","rb"))
		mapping = pickle.load(open("mapping.pkl", "rb"))
	except:
		document_weight = rank_finder(inverted_index, document_list)
		mapping = document_weight[1]
		document_weight = document_weight[0]
	print(document_weight)
	for i in range(len(document_weight[0])):
		queryFreq.append(0)
	
	for word in QueryWords:
		if word in mapping.keys():
			queryFreq[mapping[word]]+=1
		else:
			print(word, "does not appear in any document")
	
	for i in range(len(document_weight[0])):
		queryFreq[i] = queryFreq[i]/len(QueryWords)
	inp = 0
	for word in inverted_index.keys():
		idf = log(1+(no_documents/len(inverted_index[word])))
		queryFreq[inp] = idf*queryFreq[inp]
		inp+=1
	
	queryFreq = normalize(queryFreq)

	ranking = []

	for i in range(len(document_weight)):
		dot_result = 0
		for j in range(len(document_weight[0])):
			dot_result += document_weight[i][j]*queryFreq[j]
		ranking.append((dot_result, mapping[i]))

	ranking.sort(key=comp1, reverse=True)
	return ranking



def Ranking(QueryResults, inverted_index, QueryWords, document_list):
	fileNames = []
	for file in QueryResults.keys():
		QueryResults[file] = score(QueryResults[file])

	ranking = queryRank(inverted_index, QueryWords, document_list)
	print(ranking)
	return ranking


# a={'a':{'f1':[1], 'f2':[2]}, 'b':{'f1':[1], 'f2':[2]}, 'c':{'f1':[1,2]}}
# b = ['f1', 'f2']
# rank_finder(a,b)

