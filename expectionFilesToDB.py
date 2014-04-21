import psycopg2

def insertIntoAdjException(exceptionfile):
	conn_string = "host='localhost' dbname='englishWords' user='postgres' password='Ashish123'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()

	f=open(exceptionfile,'r')
	for line in f:
		words=line.split()
		print words[0]
		print words[1]
		cursor.execute('insert into adjexceptions VALUES(%s ,%s)',(str(words[0]),str(words[1])))
	conn.commit()
	conn.close()

def insertIntoVerbException(exceptionfile):
	conn_string = "host='localhost' dbname='englishWords' user='postgres' password='Ashish123'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()

	f=open(exceptionfile,'r')
	for line in f:
		words=line.split()
		print words[0]
		print words[1]
		cursor.execute('insert into verbexceptions VALUES(%s ,%s)',(str(words[0]),str(words[1])))
	conn.commit()
	conn.close()

def insertIntoAdverbException(exceptionfile):
	conn_string = "host='localhost' dbname='englishWords' user='postgres' password='Ashish123'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()

	f=open(exceptionfile,'r')
	for line in f:
		words=line.split()
		print words[0]
		print words[1]
		cursor.execute('insert into adverbexceptions VALUES(%s ,%s)',(str(words[0]),str(words[1])))
	conn.commit()
	conn.close()

def insertIntoNounException(exceptionfile):
	conn_string = "host='localhost' dbname='englishWords' user='postgres' password='Ashish123'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()

	f=open(exceptionfile,'r')
	for line in f:
		words=line.split()
		print words[0]
		print words[1]
		cursor.execute('insert into nounexceptions VALUES(%s ,%s)',(str(words[0]),str(words[1])))
	conn.commit()
	conn.close()

def returnCorrectWord(inputword,posTag,cursor):
	
	if posTag=='a':
		cursor.execute('select root from adjexceptions where inflected=%s',[inputword])
		rows=cursor.fetchall()
		return rows

	if posTag=='n':
		cursor.execute('select root from nounexceptions where inflected=%s',[inputword])
		rows=cursor.fetchall()
		return rows

	if posTag=='v':
		cursor.execute('select root from verbexceptions where inflected=%s',[inputword])
		rows=cursor.fetchall()
		return rows

	if posTag=='r':
		cursor.execute('select root from adverbexceptions where inflected=%s',[inputword])
		rows=cursor.fetchall()
		return rows


