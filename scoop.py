import sqlite3
import math

#This will take the test DB which contains all info on test articles and assign the 'actual flag' to denote criteria selection
#Calculate hit/miss ratio

conn =sqlite3.connect('test_data.db')
c = conn.cursor()

# # #Actualizer: Add Actual to all test data tables. TO DO: get to skip if exist
	c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name!='analyzed_article';")
	tables =c.fetchall()	
	for i in range(len(tables)):
		print(tables[i][0])
		c.execute("ALTER TABLE '"+tables[i][0]+"' ADD  actual INT")
		conn.commit()


#Selector: The selector sets the 'actual' flag to yes for all tables in the test DB
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name!='analyzed_article';")
tables =c.fetchall()	

for i in range(len(tables)):
	print(tables[i][0])
	c.execute("SELECT count,rowid,category FROM '"+tables[i][0]+"'")
	data = c.fetchall()
	top_row=(sorted(data,key=lambda data: data[0],reverse=True)[:3])

	for i0 in range((len(top_row))):
		c.execute("UPDATE '"+ tables[i][0] +"' SET actual = ?  WHERE rowid= ? ",((1),top_row[i0][1]))
	conn.commit()	



#Calculate Scores:
# true positive (TP), false positive (FP), true negative (TN) and false negative (FN) number of documents(N)
# Precision = TP / (TP + FP)
# Recall = TP / (TP + FN)
# Accuracy = (TP + TN)/N
# Error = (FP + FN)/N
# F1 = 2*Recall*Precision/(Recall + Precision)

# TP = items in Analyzed_cats == items in actualized columns 

#get list of actualized for each actualized 

c.execute("SELECT COUNT(*) from analyzed_article")
N = c.fetchone()


for i in range(len(tables)):
	c.execute("SELECT category FROM '"+tables[i][0]+"' WHERE actual = 1")
	data1 = c.fetchall()

	c.execute("SELECT cat0,cat1,cat2,cat3,cat4 FROM analyzed_article WHERE value='"+tables[i][0]+"'")
	data2 = c.fetchall()
	TP = 0
	for i0 in range(len(data1)):
		if data1[i0][0] in data2[0]:
			TP +=1
	c.execute("UPDATE 'analyzed_article' SET TP = ? WHERE value='"+tables[i][0]+"'",(TP,))
	conn.commit()

c.execute("SELECT SUM(TP) from analyzed_article")
S = c.fetchone()
print("Accuracy " +str(S[0]/float(N[0])))




