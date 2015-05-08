
import os, pymongo, sys, datetime, csv, json, itertools
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from collections import Counter

def rank(key, data):
	result = []

	data = sorted(filter(lambda x : x.has_key(key) and x[key]!='' , data), key=lambda x : x[key])
	for k, g in itertools.groupby(data, lambda x : x[key]):
		result.append({ "key" : k, 'size': len(list(g))})
	result = sorted(result, key=lambda x: x['size']);	
	return result
def compare(data1, data2):
	if len(data1)!=len(data2):
		print "fucked up"
	for d0, d1 in zip(data1, data2):
		# print t
		print d0['key'], ", ", d0['size'] ,", ", d0['key'], ", ",  d1['size']
if __name__ == "__main__":
	# open remote database
	client 	= pymongo.MongoClient('54.69.103.85', 27017)
	db 		= client.socialdoi
	filtered 	= db.naviHistLogsCtrl.find({'action':'survey'})
	interests 	= db.naviHistLogsCtrl.find({'action':'finish'});
	navigation 	= db.naviHistLogsCtrl.find({'action':'select'});

	#collect survey data
	survey = {}
	for log in filtered:
		key = log['hit_id']+'/'+log['assignment_id']
		if survey.has_key(key):
			print 'A worker participated in multiple hits! : ' + key  ## ERROR1: Duplicate Participation					
		else:
			survey[key] = log;


	# aggregate navigation histories
	userSpecified = [];
	for log in interests:
		if survey.has_key(log['hit_id']+'/'+log['assignment_id'])==False: # if no survey exists, discard this data
			continue	
		userSpecified = userSpecified + json.loads(log['data']['selectedPrograms']);
	autoLogged = [];	
	for log in navigation:
		if survey.has_key(log['hit_id']+'/'+log['assignment_id'])==False: # if no survey exists, discard this data
			continue
		if (log['data']['is_practice']=='false'):
			autoLogged.append(log['data']['selectedBudget']);	

	#print size;
	print len(autoLogged)
	print len(userSpecified)

	# ranking programs
	autoCabinet = rank('cabinet', autoLogged)
	autoDept	= rank('department', autoLogged)
	autoProgram = rank('program', autoLogged)

	userCabinet = rank('cabinet', userSpecified)
	userDept	= rank('department', autoLogged)
	userProgram = rank('program', userSpecified)	
	print "Cabinet =============="
	compare(userCabinet[-10:], autoCabinet[-10:])
	print "Department =============="
	compare(userDept[-10:], autoDept[-10:])
	print "Program =============="
	compare(userProgram[-3:], autoProgram[-3:])
	print userProgram[-10:]
	# print autoProgram;
	# localClient = pymongo.MongoClient('localhost', 27017)
	# localDb 	= localClient.socialdoi
	# print 'Start copying records'
	# i=0
	# for log in allLogs:
	# 	i+=1
	# 	print i
	# 	localDb.logs.insert(log)

	print 'Done.'