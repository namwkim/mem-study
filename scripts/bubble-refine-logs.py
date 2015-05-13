import os, pymongo, sys, datetime, csv, itertools

if __name__ == "__main__":
	# open log database
	#client 	= pymongo.MongoClient('54.69.103.85', 27017)
	client 	= pymongo.MongoClient('localhost', 27017)
	db 		= client.bubblestudy
	logs 	= db.logs24
	toCopy 	= db.refinedLogs24
	toCopy.remove({})

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

	#collect desc-change data
	filtered 	= logs.find({'action':'desc-change', 'data.is_practice':'false'})
	descChanges = {}
	for x in filtered:
		if survey.has_key(x['hit_id']+'/'+x['assignment_id']) and \
		 	desc.has_key(x['hit_id']+'/'+x['assignment_id']+ '/' + x['data']['image']):
		 	if descChanges.has_key(x['data']['image']))==False:
				descChanges[x['data']['image'])] = {}
			if descChanges[x['data']['image'])].has_key(x['hit_id']+'/'+x['assignment_id']):
				descChanges[x['data']['image'])][x['hit_id']+'/'+x['assignment_id']] = []
		 	descChanges[x['data']['image'])][x['hit_id']+'/'+x['assignment_id']].append(x);


	#clear existing collection
	


	#group by images 
	
	sortedByImage = sorted(clicks, key=lambda x : x['data']['image'])
	for k, g in itertools.groupby(sortedByImage, key=lambda x : x['data']['image']):	
		#save back to database
		imageName = k.split("/")[-1].split(".")[0]	
		print 'saving... ', imageName
		groupClicks = list(g)
		sortedByAsmt = sorted(groupClicks, key=lambda x : x['hit_id']+'/'+x['assignment_id'])
		assignments = []
		#group by assignments
		for ak, ag in itertools.groupby(sortedByAsmt, key=lambda x : x['hit_id']+'/'+x['assignment_id']):
	    	#sort clicks
			sortedClicks = sorted(ag, key=lambda x: x['timestamp'])	    	

			#sort desc-changes
			sortedDescChgs = sorted(descChanges[k][ak], key=lambda x: x['timestamp'])
			asmt = {}
			asmt["id"]		= ak
			asmt["clicks"] 	= sortedClicks
			asmt["desc"] 	= desc[ak+'/'+k]
			asmt["survey"] 	= survey[ak]
			asmt["desc_change"] = sortedDescChgs

			assignments.append(asmt)
			print 'assignment ID: ', ak, ', click counts: ', len(asmt["clicks"])

		

		print len(assignments)
		toCopy.insert({ "image": imageName, "logs": assignments }) 
	

	

