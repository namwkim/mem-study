import csv, pymongo, itertools

if __name__ == "__main__":
	client 	= pymongo.MongoClient('localhost', 27017)
	db 		= client.socialdoi
	db.budgets.remove({})

	budgets = {}
	with open('operating-budget.csv', 'r') as csvfile:
	    reader = csv.reader(csvfile)

	    reader.next()

	    for row in reader:
	    	key = row[0]+"/"+row[1]+"/"+row[2]+"/"+row[3]
	    	if budgets.has_key(key)==False:
	    		print row[3]
	    		budgets[key] = {
		    		"fiscalyear": row[0],
		     		"cabinet": row[1],
		     		"department": row[2],
		     		"program": row[3],
		     		# "expense_type": row[4],
		     		# "expense_category": row[5],
		     		"recommended": 0,
		     		"approved": 0,
		     		# "account_name": row[8],
		     		"fund": row[9],
		     		"fundtype": row[10],
		     		# "program_number": row[11],
		     		# "account_number": row[12]

		    		}
    		budgets[key]["recommended"] += int(float(row[6][1:]))
    		budgets[key]["approved"] += int(float(row[7][1:]))
	    	
	    	# print row[3]

	    	# if budgets.has_key(row[3])==False:
	    	# 	budgets[""]
	   
	    	# print record
	i = 0
	for k in budgets:
		if (budgets[k]["cabinet"]!="Education" and budgets[k]["approved"]>10000) or (budgets[k]["cabinet"]=="Education" and budgets[k]["approved"]>5000000):
			i+=1
			db.budgets.insert(budgets[k])
	print i
	# with open('budgets.csv', 'r') as csvfile:
	#     reader = csv.reader(csvfile)
	#     reader.next()
	#     for row in reader:	

	#     	record = {
	#     		"fiscalyear": row[0],
	#     		"cabinet": row[1],
	#     		"department": row[2],
	#     		"program": row[3],
	#     		"programID": row[4],
	#     		"fund": row[5],
	#     		"fundtype": row[6],
	#     		"actual": row[7][1:],
	#     		"approved": row[8][1:]
	#     	}
	#     	print record
	#     	db.budgets.insert(record)