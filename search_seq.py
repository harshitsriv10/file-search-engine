import re
import pickle
import os
from nltk import PorterStemmer
# from ranker import *
import time
from math import *
# from nltk import stopwords

from nltk.corpus import brown
word_list = brown.words()
word_set = set(word_list)



total_index_seq = pickle.load(open("save_seq.pkl","rb")) 

def one_word_query(word, invertedIndex):
	pattern = re.compile('[\W_]+')
	word = pattern.sub(' ',word)
	if word in invertedIndex.keys():
		return [filename for filename in invertedIndex[word].keys()]
	else:
		return []



# def phrase_query(string, invertedIndex):
# 	pattern = re.compile('[\W_]+')
# 	string = pattern.sub(' ',string)
# 	listOfLists, result = [],[]
# 	for word in string.split():
# 		listOfLists.append(one_word_query(word,invertedIndex))
# 	setted = set(listOfLists[0]).intersection(*listOfLists)
# 	for filename in setted:
# 		temp = []
# 		for word in string.split():
# 			temp.append(invertedIndex[word][filename][:])
# 		for i in range(len(temp)):
# 			for ind in range(len(temp[i])):
# 				temp[i][ind] -= i
# 		if set(temp[0]).intersection(*temp):
# 			result.append(filename)
# 	#return rankResults(result, string)
# 	return result


def SearchWord(word, InvertedIndex):
	pattern = re.compile('[\W_]+')
	word = pattern.sub(' ',word)
	if word in InvertedIndex.keys():
		return [file for file in InvertedIndex[word].keys()]
	else:
		return []

def phrase_query(phrase, invertedIndex):
	pattern = re.compile('[\W_]+')
	phrase = pattern.sub(' ',phrase)
	phrase=phrase.split()
#	phrase=Stem(phrase)
	lists=[]
	result=[]
	for word in phrase:
		lists.append(SearchWord(word,invertedIndex))
	setted = set(lists[0]).intersection(*lists)
	for i in setted:
		print(i)
	for file in setted:
		temp = []
		for word in phrase:
			temp.append(invertedIndex[word][file][:])
		if set(temp[0]).intersection(*temp):
			result.append((file,temp[0]))
	#return rankResults(result, string)
	return result



def SearchPhrase(phrase, InvertedIndex):
	pattern = re.compile('[\W_]+')
	phrase = pattern.sub(' ',phrase)
	phrase = phrase.split()
	#phrase=Stem(phrase)
	# phrase = processString(phrase)
	lists = []
	result = []
	for word in phrase:
		if(word in word_set):
			print(True)
		else:
			print(False)
		lists.append(SearchWord(word, InvertedIndex))
	settled = set(lists[0]).intersection(*lists)
	
	for i in settled:
		print(i)

	for file in settled:
		temp = []
		for word in phrase:
			temp.append(InvertedIndex[word][file][:])
		
		
		if(set(temp[0]).intersection(*temp)):
			result.append((file, temp[0]))
	return result

def check(string):
	temp=string
	startIndex = temp.find('\"')
	if startIndex != -1: 
		endIndex = temp.find('\"', startIndex + 1)
        if startIndex == 0  and endIndex == len(temp)-1: 
        	return True
	return False


total_index_seq = pickle.load(open("save_seq.pkl","rb"))

while (1):
	str = raw_input()
	print(str)
	boolean=check(str)
	print(boolean)
	anss=phrase_query(str,total_index_seq)
	print(anss)