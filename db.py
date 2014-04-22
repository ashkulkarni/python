import psycopg2
import wordMethods
import operator
import collections
import expectionFilesToDB as e
from stemming.porter2 import stem
def insertIntoDB(word_id,lemma,ss_type,synset_offset,sense_number,contextwords):
	conn_string = "host='localhost' dbname='complete_wordsDB' user='postgres' password='dnana'"

	conn = psycopg2.connect(conn_string)

	cursor = conn.cursor()
 	print lemma

 	#frequency=wordMethods.getFrequency(lemma)
 	#print frequency
	cursor.execute('INSERT INTO wordlistDB VALUES (%s, %s, %s, %s, %s,%s,%s,%s)', (word_id,lemma,synset_offset,'',sense_number,ss_type,0,contextwords))
 	conn.commit();
	conn.close();

def getAllWordsFromDB():

	wordsFromDB=[]
	conn_string = "host='localhost' dbname='complete_wordsDB' user='postgres' password='dnana'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	cursor.execute('select word from word_list');
	rows=cursor.fetchall()
	for row in rows:
		if row[0][0]!='\'':
			if(row[0]!='a'):
				wordsFromDB.append(row[0])
	return wordsFromDB
	conn.commit()
	conn.close()

#word vector and inputwords are converted to lower case 
def checkWordinWordVector(word,wordVector,stemmedWordlist):
	if word in wordVector:
		return True
		#print 'Hit: ',word
	else:
		stemWord = stem(word)
		if stemWord in wordVector:
			return True
		else:
			if stemWord in stemmedWordlist:
				return True
			else:
				return False

	
	
def insertFrequencyInDB(inputword,pos,wordVector,stemmedWordlist):
	conn_string = "host='localhost' dbname='englishWords' user='postgres' password='Ashish123'"
	synsetid_contextwords={}
	wordMapContextHit ={}
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()

	cursor.execute('select synset_offset,contextwords from wordlistdb where word=%s and ss_type=%s',[inputword,pos])
	rows=cursor.fetchall()
	if rows==[]:
		exceptionRows = e.returnCorrectWord(inputword,pos,cursor)
		if exceptionRows ==[]:
			rows = lemmatization(inputword,pos,cursor)
		else:
			for row in exceptionRows:
				inputword = row[0]
			#print "ExceptionList: "+inputword
			cursor.execute('select synset_offset,contextwords from wordlistdb where word=%s and ss_type=%s',[inputword,pos])
			rows=cursor.fetchall()
	
	for row in rows:
		synset_offset = row[0]
		contextwords = row[1]
		wordMapContextHit[synset_offset]=0
		contextwords = contextwords[1:-1].split(',')
		for word in contextwords:
			hit =checkWordinWordVector(word.lower(),wordVector,stemmedWordlist)
			if(hit):
				#print 'Hit Offset: ',synset_offset
				wordMapContextHit[synset_offset]=wordMapContextHit[synset_offset]+1



			cursor.execute('select contextwords from wordlistdb where word=%s',[word])
			resultContextWords = cursor.fetchall()
			maxHit1level=0
			for eachRow in resultContextWords:
				contextWordsRow = eachRow[0]
				contextWordsRow = contextWordsRow[1:-1].split(',')
				countHits=0
				for wordlevel1 in contextWordsRow:
					hitlevel1 = checkWordinWordVector(wordlevel1.lower(),wordVector,stemmedWordlist)
					if(hitlevel1):
						countHits = countHits+1
				if(countHits > maxHit1level):
					maxHit1level = countHits

			wordMapContextHit[synset_offset]=wordMapContextHit[synset_offset]+maxHit1level
	#print wordMapContextHit
	if(wordMapContextHit!={}):
		targetSynsetId=max(wordMapContextHit.iteritems(), key=operator.itemgetter(1))[0]
		#targetSynsetId=1
		frequency = 0;
		print 'target synsetId: ',targetSynsetId
		cursor.execute('select frequency from wordlistdb where synset_offset=%s and word=%s and ss_type=%s',[targetSynsetId,inputword,pos])
		frequencyRows=cursor.fetchall()
		#print 'Freq: ',frequencyRows
		for frequencyRow in frequencyRows:
			frequency=frequencyRow[0]
			frequency=frequency+1

		cursor.execute('UPDATE wordlistdb set frequency=%s where synset_offset=%s and word=%s and ss_type=%s',[frequency,targetSynsetId,inputword,pos])
	conn.commit()
	#conn.close()
	

def lemmatization(inputword,pos,cursor):
	ending=""
	orderedRules=collections.OrderedDict()
	rows = []
	if(pos=='n'):
		nounRules(orderedRules)
		if(inputword.endswith('ful')):
			ending="ful"
			head,sep,tail = inputword.rpartition("ful")
			inputword = head+tail
	elif pos=='v':
		verbRules(orderedRules)
	elif pos == 'a':
		adjRules(orderedRules)
	elif pos == 'r':
		return rows
	rootWord=""
	for key,valueList in orderedRules.iteritems():
		if rows != []:
			#print "lemmatization: "+inputword
			#print "RootWord: "+rootWord
			break
		rootWord=inputword
		head,sep,tail = rootWord.rpartition(key)
		rootWord = head+valueList[0]+tail+ending
		cursor.execute('select synset_offset,contextwords from wordlistdb where word=%s and ss_type=%s',[rootWord,pos])
		rows=cursor.fetchall()
		if (rows==[]) and (len(valueList)>1):
			rootWord=inputword
			head,sep,tail = rootWord.rpartition(key)
			rootWord = head+valueList[1]+tail+ending
			cursor.execute('select synset_offset,contextwords from wordlistdb where word=%s and ss_type=%s',[rootWord,pos])
			rows=cursor.fetchall()

	return rows


def nounRules(nRules):
	nRules["s"] = [""]
	nRules["ses"] = ["s"]
	nRules["xes"] = ["x"]
	nRules["zes"] = ["z"]
	nRules["ches"] = ["ch"]
	nRules["shes"] = ["sh"]
	nRules["men"] = ["man"]
	nRules["ies"] = ["y"]

def verbRules(vRules):
	vRules["s"]=[""]
	vRules["ies"]=["y"]
	vRules["es"]=["e",""]
	vRules["ed"]=["e",""]
	vRules["ing"]=["e",""]

def adjRules(aRules):
	aRules=collections.OrderedDict()
	aRules["er"]=["","e"]
	aRules["est"]=["","e"]



def stemmingWordList(inflectedWordlist):
	stemmedWordlist = []
	for word in inflectedWordlist:
		stemmedWordlist.append(stem(word))
	return stemmedWordlist



		#root words







	# for row in rows:
	# 	synsetid_contextwords[row[0]]=row[1]
	# print synsetid_contextwords
	#wordsFromDB=getAllWordsFromDB()
	#for word in wordsFromDB:
	#	print 'Word',word
	#	frequency=wordMethods.getFrequency(word)
		
	#	print 'Frequency',frequency
	#	cursor.execute('UPDATE wordlistdb set frequency=%s where word=%s',[frequency,word]