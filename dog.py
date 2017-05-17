import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
import string
import csv
import sqlite3
from cStringIO import StringIO
import datetime
import random


ps = PorterStemmer()
stop_words = stopwords.words("english")

conn =sqlite3.connect('test_data.db')
c = conn.cursor()

conn2 =sqlite3.connect('train_data.db')
c2 = conn2.cursor()

c2.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables =[c2.fetchall()]

def strip( text ):
	text1 = text.lower()
	texttokens = word_tokenize(text1.translate(None, string.punctuation))
	ps_text_tokens = []
	for i in range(len(texttokens)):
		ps_text_tokens.append(ps.stem(texttokens[i]))

	text_filtered = []
	top_words = []
	extra_stop_words = ["wa","ha","thi","one","say","hi","like","said"]
	for w in ps_text_tokens:
		if w not in stop_words:
			if w not in extra_stop_words:
				text_filtered.append(w)

	fdist = FreqDist(text_filtered)
	top_words.extend(fdist.most_common(10))
	return top_words

def create_table(title):
	c.execute("CREATE TABLE IF NOT EXISTS '" + title + "'(category TEXT,count INT DEFAULT 1)")



def check_table (word, article):
	for i in range(len(tables[0])):
		c2.execute("SELECT rowid FROM "+ tables[0][i][0] +" WHERE value = ?", (word,))
		data=c2.fetchall()
		if len(data)!=0:
			inc_table((tables[0][i][0]),article)

def inc_table(topic, article):
	c.execute("SELECT rowid FROM '"+ article +"' WHERE category = ?", (topic,))
	data=c.fetchall()
	if len(data)==0:
		c.execute("INSERT INTO '"+ article +"'(category) VALUES (?)", (topic,))
	else:
		c.execute("SELECT count FROM '"+ article +"' WHERE category = ?", (topic,))
		data2=c.fetchall()	
		c.execute("UPDATE '"+ article +"' SET count = ?  WHERE rowid= ? ",((data2[0][0]+1),data[0][0]))
	conn.commit()		




# #PRACTICE TRAIN DATA DON'T FUCK WITH THIS

# c.execute("CREATE TABLE IF NOT EXISTS analyzed_article (value TEXT, cat0 TEXT, cat1 TEXT, cat2 TEXT, cat3 TEXT, cat4 TEXT, cat5 TEXT, TP INT)")

# test_articles = []
# with open('TrainingData/training_data_title.csv') as csvfile:
#     readCSV = csv.reader(csvfile, delimiter=',')
#     for row in readCSV:
#         test_articles.extend(row)


# for index in range(len(test_articles)):
# 	rand_test_articles = random.sample(test_articles,len(test_articles))
# 	f=open("TrainingData/"+ rand_test_articles[index] +".json","r")
# 	s=f.read()
# 	book = json.loads(s)
# 	num_art= len(book['TrainingData'])

# 	for i in range(1, num_art, 1):
# 		extract = []
# 		ih = rand_test_articles[index]+"_" + str(i).zfill(5) +""
# 		create_table(ih)

# 		c.execute("SELECT rowid FROM analyzed_article WHERE value = ?", (ih,))
# 		data=c.fetchall()

# 		if len(data)==0:
# 			c2.execute("SELECT rowid FROM analyzed_article WHERE value = ?", (ih,))
# 			data2=c2.fetchall()

# 			if len(data2)==0:
# 				topics = book['TrainingData'][ih]['topics']
# 				if len(topics)!=0:
# 					t0 = [None, None, None, None, None, None]
# 					for i in range(len(topics)):
# 						t0[i]=(topics[i])
# 					c.execute("INSERT INTO analyzed_article (value, cat0, cat1, cat2, cat3, cat4, cat5) VALUES (?, ?, ?, ?, ?, ?, ?)", (ih,t0[0],t0[1],t0[2],t0[3],t0[4],t0[5]))
# 					conn.commit()

# 					extract.append(book['TrainingData'][ih]['bodyText'])
# 					send = []
# 					send.extend(strip(str(extract)))
# 					for i in range(len(send)):
# 						check_table(send[i][0],ih)
# 				print("working on "+ ih)
# 			else:
# 				print(ih + " already Exists in Train DB")
# 		else:
# 			print(ih + " already Exists in Test DB")
				


			

##OPEN TEST DATA DONT FUCK WITH THIS CODE. 
f=open("TestData.json","r")
s=f.read()
book = json.loads(s)
num_art= len(book['TestData'])

#return pop word and article nane
for index in range(1, num_art, 1):
	extract = []
	ih ="TestData_" + str(index).zfill(5) +""
	print(ih)
	create_table(ih)
	extract.append(book['TestData'][ih]['bodyText'])
	send = []
	send.extend(strip(str(extract)))
	for i in range(len(send)):
		check_table(send[i][0],ih)




