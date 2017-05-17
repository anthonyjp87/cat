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


conn =sqlite3.connect('train_data.db')
c = conn.cursor()

ps = PorterStemmer()
stop_words = stopwords.words("english")
topics = []

with open('topics.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        topics.extend(row)

def strip( text ):
	text1 = text.lower()
	texttokens = word_tokenize(text1.translate(None, string.punctuation))
	ps_text_tokens = []
	for i in range(len(texttokens)):
		ps_text_tokens.append(ps.stem(texttokens[i]))

	text_filtered = []
	top_words = []
	extra_stop_words = ["wa","ha","thi","one","say","hi","like","said","1922committee","would","x95"]
	for w in ps_text_tokens:
		if w not in stop_words:
			if w not in extra_stop_words:
				text_filtered.append(w)

	fdist = FreqDist(text_filtered)
	top_words.extend(fdist.most_common(10))
	return top_words


def create_table():
	global topics
	for i in range(len(topics)):
		c.execute("CREATE TABLE IF NOT EXISTS analyzed_article (value TEXT)")
		c.execute("CREATE TABLE IF NOT EXISTS "+ topics[i] +  " (value TEXT, count INT DEFAULT 1, countln INT DEFAULT 1)")
create_table()

def table_exist(new_id):
	c.execute("CREATE TABLE IF NOT EXISTS "+ new_id +  " (value TEXT, count INT DEFAULT 1, countln INT DEFAULT 1)")
create_table()


def data_entry( popwords , topic):
	for index in range(len(popwords)):
		c.execute("SELECT rowid FROM "+ topic +" WHERE value = ?", (popwords[index],))
		data=c.fetchall()
		if len(data)==0:
			c.execute("SELECT COUNT(*) from "+ topic)
			result=c.fetchone()
			if result[0] < 1000:
				c.execute("INSERT INTO  "+ topic +" (value) VALUES (?)", (popwords[index],))
		else:
			c.execute("SELECT count FROM "+ topic +" WHERE value = ?", (popwords[index],))
			data2=c.fetchall()
			c.execute("UPDATE "+ topic +" SET count = ?  WHERE rowid= ? ",((data2[0][0]+1),data[0][0]))
	conn.commit()



articles = []
with open('TrainingData/training_data_title.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        articles.extend(row)

for index in range(len(articles)):
	f=open("TrainingData/"+ articles[index] +".json","r")
	s=f.read()
	book = json.loads(s)
	num_art= len(book['TrainingData'])

	print("Starting "+ articles[index])
	print( datetime.datetime.utcnow())



	for i in range(1, num_art, 1):
		extract = []
		article_topic = []
		ih =articles[index]+"_" + str(i+1).zfill(5) +""
		print(ih)
		c.execute("SELECT rowid FROM analyzed_article WHERE value = ?", (ih,))
		data=c.fetchall()

		if len(data)==0:
			c.execute("INSERT INTO analyzed_article (value) VALUES (?)", (ih,))
			conn.commit()

			article_topic.extend(book['TrainingData'][ih]['topics'])
			extract.append(book['TrainingData'][ih]['bodyText'])
			
			send = []
			send.extend(strip(str(extract)))

			out = []
			for i in range(len(send)):
					out.extend([send[i][0]])

			tl = len(article_topic)
			if tl==0:
					1
			else:
				for i in range (0, tl, 1):
					table_exist(article_topic[i])
					data_entry(out, article_topic[i])
	print("TrainingData/"+ articles[index] +" is complete.")
	print( datetime.datetime.utcnow())		




