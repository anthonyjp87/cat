import csv
import json
import sqlite3

conn =sqlite3.connect('send.db')
c = conn.cursor()

conn2 =sqlite3.connect('test_data.db')
c2 = conn2.cursor()

topics=[]
with open('topics.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        topics.extend(row)

c.execute("CREATE TABLE IF NOT EXISTS send (article TEXT)")

topics_in_db = []
c.execute("PRAGMA table_info(send);")
topics_in_db.extend([tup[1] for tup in c.fetchall()])

for i in range(len(topics)): 
	if topics[i] in topics_in_db:
		1
	else: 
		c.execute("ALTER TABLE send ADD  "+topics[i]+" INT")
		conn.commit()

#for table in test_data, create ROW in Send. If 'actual' flag == column: 1
c2.execute("SELECT name FROM sqlite_master WHERE type='table';")
data = c2.fetchall()

for i in range(len(data)):
	c2.execute("SELECT category FROM "+data[i][0]+ " WHERE actual = 1")
	data2 =[tup[0] for tup in c2.fetchall()]
	c.execute("SELECT rowid FROM send WHERE article = ?", (data[i][0],))
	d1 = c.fetchall()
	if len(d1)==0:
		c.execute("INSERT INTO send (article) VALUES (?)", (data[i][0],))
		conn.commit()	
		for i1 in range(len(data2)):
			if data2[i1] in topics:
				print(data2[i1]+ " data is in topics" +data[i][0] )
				c.execute("UPDATE send SET '"+data2[i1]+"' = ? WHERE article = ?",(1,data[i][0]) )
				conn.commit()	
		
		





