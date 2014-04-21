import urllib2
import os
#import nltk
import re
from bs4 import BeautifulSoup
import db
import psycopg2

def getListOfSentenceOfWord(list_of_sentence,word,list_file_names):
	#dict_word_sentence[word]=[]
	words=word.split(' ')
	for file_name in list_file_names:
		page = urllib2.urlopen('file:///home/ananda/brown_tei/'+file_name).read()
		soup=BeautifulSoup(page)
		for node in soup.findAll('p'):
			for sentence in node.findAll('s'):
				sent = sentence.get_text()

				for w in sentence.findAll('w'):
					#print ''.join(word.findAll(text=True))
					for word in words:
						if word == w.get_text():

							print word
							list_of_sentence.append(str(sent))
			
	return list_of_sentence
	
def getFrequency(word):
	
	frequency=0
	word=getProperWord(word)

	list_file_names=getListOfFileNames()
	for file_name in list_file_names:
		page = urllib2.urlopen('file:///home/ananda/brown_tei/'+file_name).read()
		soup=BeautifulSoup(page)
		for node in soup.findAll('p'):
			for sentence in node.findAll('s'):
				sent = sentence.get_text()
				print sent

				matches=re.findall(word,sent)
				if matches!=[]:
					# think it should be frequency+len(matches) in the senetnce...sentence can hv multiple occurance of the same word...check
				#	frequency=frequency+1
					print sent
					break

	#return frequency

def parseCorpus():
	list_file_names=getListOfFileNames()
	stopwords=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
	adjposlist=['JJ', 'JJR', 'JJS', 'JJT']
	nounposlist=['NN', 'NN$', 'NNS', 'NNS$', 'NP', 'NP$', 'NPS', 'NPS$', 'NR']
	adverbposlist=['RB', 'RBR', 'RBT', 'RN', 'RP', 'WRB']
	verbposlist=['VB', 'VBD', 'VBG', 'VBP', 'VBZ', 'VBN']
	#list_file_names = ['a01.xml']
	conn_string = "host='localhost' dbname='englishWords' user='postgres' password='Ashish123'"
	conn = psycopg2.connect(conn_string)
	for file_name in list_file_names:
		print 'FILE: ',file_name
		page = urllib2.urlopen('file:///C:/Users/ashikulkarni/Documents/FinalYearProject/NLP/corpus/brown_tei/'+file_name).read()
		soup=BeautifulSoup(page)
		paraList =[]
		paraList = soup.findAll('p')
		for ptag in paraList:
			if(ptag.findAll('s')!=[]):
				wordVector=[]
				#wordVector = str(ptag.get_text()).strip().split()
				words = []
				words = ptag.findAll('w')
				for wtag in words:
					inputword = str(wtag.get_text().lower())
					pos = wtag['type']
					flag = True
					if pos in adjposlist:
						pos='a'
					elif pos in nounposlist:
						pos='n'
					elif pos in adverbposlist:
						pos='r'
					elif pos in verbposlist:
						pos='v'
					else:
						flag = False
					if (flag)and(inputword not in stopwords):
						wordVector.append(inputword)
				print wordVector
					

				for wtag in words:
					inputword = str(wtag.get_text().lower())
					pos = wtag['type']
					flag = True
					if pos in adjposlist:
						pos='a'
					elif pos in nounposlist:
						pos='n'
					elif pos in adverbposlist:
						pos='r'
					elif pos in verbposlist:
						pos='v'
					else:
						flag = False
					if (flag)and(inputword not in stopwords):
						db.insertFrequencyInDB(inputword,pos,wordVector)
		break					


def getListOfFileNames():
	list_file_names=[]
	for file_name in os.listdir("C:/Users/ashikulkarni/Documents/FinalYearProject/NLP/corpus/brown_tei"):
		if file_name.endswith(".xml"):
			list_file_names.append(file_name)
	return list_file_names


def partOfSpeech(sentence):
	return nltk.pos_tag(nltk.word_tokenize(sentence))


def getProperWord(word):
	if word.find('_')!=-1:
		list_char=list(word)
		index=list_char.index('_')
		list_char[index]=' '
		word=''.join(list_char)
	return word


def getSentence(word):
	word=getProperWord(word)
	list_of_sentence=[]
	#list_file_names=getListOfFileNames()
	list_file_names=['a01.xml']
	return getListOfSentenceOfWord(list_of_sentence,word,list_file_names)