import os, pymongo, sys, datetime, csv, itertools

if __name__ == "__main__":
	# open log database
	#client 	= pymongo.MongoClient('54.69.103.85', 27017)
	client 	= pymongo.MongoClient('localhost', 27017)
	db 		= client.bubblestudy
	logs 	= db.logs


	#collect survey data
	filtered 	= logs.find({'action':'survey'})
	survey = {}
	for log in filtered:
		key = log['hit_id']+'/'+log['assignment_id']
		if survey.has_key(key):
			print 'A worker participated in multiple hits! : ' + key  ## ERROR1: Duplicate Participation					
		else:
			survey[key] = log;
	 		
	#print survey

	#collect text-description
	filtered 	= logs.find({'action':'explain', 'data.is_practice':'false'})
	#print filtered

	desc = {}
	for log in filtered:
		if survey.has_key(log['hit_id']+'/'+log['assignment_id'])==False: # if no survey exists, discard this data
			continue
		key = log['hit_id']+'/'+log['assignment_id']+ '/' + log['data']['image']
		if desc.has_key(key):
			print 'Duplicate text description found! : ' + key
			continue
		else:
			desc[key] = log;

	#print desc

	#collect click data
	filtered 	= logs.find({'action':'click', 'data.is_practice':'false'})
	clicks = []
	for x in filtered:
		if survey.has_key(x['hit_id']+'/'+x['assignment_id']) and \
		 	desc.has_key(x['hit_id']+'/'+x['assignment_id']+ '/' + x['data']['image']):
		 	clicks.append(x)
	#print clicks


	#group by images 
	
	sortedByImage = sorted(clicks, key=lambda x : x['data']['image'])
	for k, g in itertools.groupby(sortedByImage, key=lambda x : x['data']['image']):		
	    groupClicks = list(g)
	    sortedByAsmt = sorted(groupClicks, key=lambda x : x['hit_id']+'/'+x['assignment_id'])
	    assignments = []

	    #group by assignments
	    for ak, ag in itertools.groupby(groupClicks, key=lambda x : x['hit_id']+'/'+x['assignment_id']):		
	    	asmt = {}
	    	asmt["id"]		= ak
	    	asmt["clicks"] 	= list(ag)
	    	asmt["desc"] 	= desc[ak+'/'+k]
	    	asmt["survey"] 	= survey[ak]
	    	assignments.append(asmt)

	    #save back to database
	    imageName = k.split("/")[-1].split(".")[0]
	    print 'saving... ', imageName	    
	    db.refinedLogs.insert({ "image": imageName, "logs": assignments })
	

	

