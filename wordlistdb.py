import psycopg2
import db
import sys
import re
import pprint

def indexSenses(datafile):
	filep=open(datafile,'r')
	fileadj=open('./dict/data.adj','r')
	filenoun=open('./dict/data.noun','r')
	fileverb=open('./dict/data.verb','r')
	fileadv=open('./dict/data.adv','r')
	
	
	stopwords=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
	word_id=0
	for line in filep:
		sense_key,synset_offset,sense_number,tag_cnt=line.strip().split()
		lemma,lex_sense = sense_key.split('%')
		ss_type,lex_file,lex_id,head_word,head_id = lex_sense.split(':')
		typeint = int(ss_type)
		contextwords=[]
		contextstring=""
		if typeint == 1:
			ss_type = 'n'
			offset = int(synset_offset)
			filenoun.seek(offset)
			dataline = filenoun.readline().strip().split('|')
			contextstring=re.sub('[^A-Za-z0-9-]+', ' ',dataline[1]).lower()
			words=contextstring.split()
			for word in words:
				if word not in stopwords:
					contextwords.append(word)

		elif typeint == 2:
			ss_type = 'v'
			offset = int(synset_offset)
			fileverb.seek(offset)
			dataline = fileverb.readline().strip().split('|')
			contextstring=re.sub('[^A-Za-z0-9-]+', ' ',dataline[1]).lower()
			words=contextstring.split()
			for word in words:
				if word not in stopwords:
					contextwords.append(word)

		elif typeint == 3 or typeint==5:
			ss_type = 'a'
			offset = int(synset_offset)
			fileadj.seek(offset)
			dataline = fileadj.readline().strip().split('|')
			contextstring=re.sub('[^A-Za-z0-9-]+', ' ',dataline[1]).lower()
			words=contextstring.split()
			for word in words:
				if word not in stopwords:
					contextwords.append(word)

		elif typeint == 4:
			ss_type = 'r'
			offset = int(synset_offset)
			fileadv.seek(offset)
			dataline = fileadv.readline().strip().split('|')
			contextstring=re.sub('[^A-Za-z0-9-]+', ' ',dataline[1]).lower()
			words=contextstring.split()
			for word in words:
				if word not in stopwords:
					contextwords.append(word)

		m=re.match("^[a-z]",lemma)
		if m:
			word_id=word_id+1
			db.insertIntoDB(word_id,lemma,ss_type,synset_offset,sense_number,contextwords)


