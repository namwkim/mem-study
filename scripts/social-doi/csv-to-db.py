import csv, pymongo

if __name__ == "__main__":
	client 	= pymongo.MongoClient('localhost', 27017)
	db 		= client.socialdoi
	db.budgets.remove({})
	with open('budgets.csv', 'r') as csvfile:
	    reader = csv.reader(csvfile)
	    reader.next()
	    for row in reader:	

	    	record = {
	    		"fiscalyear": row[0],
	    		"service": row[1],
	    		"department": row[2],
	    		"project": row[3],
	    		"projectID": row[4],
	    		"fund": row[5],
	    		"fundtype": row[6],
	    		"actual": row[7][1:],
	    		"approved": row[8][1:]
	    	}
	    	print record
	    	db.budgets.insert(record)