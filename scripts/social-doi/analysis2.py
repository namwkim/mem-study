
import os, pymongo, sys, datetime, csv, json, itertools
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from collections import Counter

# def rank(key, data):list
# 	result = []

# 	data = sorted(filter(lambda x : x.has_key(key) and x[key]!='' , data), key=lambda x : x[key])
# 	for k, g in itertools.groupby(data, lambda x : x[key]):
# 		result.append({ "key" : k, 'size': len(list(g))})
# 	result = sorted(result, key=lambda x: x['size'], reverse=True);	
# 	return result
# def compare(data1, data2, upto):
# 	if len(data1)!=len(data2):
# 		print "fucked up"
# 	l = max(len(data1), len(data2))
# 	for i in xrange(l):
# 		if (i+1)>upto: 
# 			continue
# 		print 'rank ------------------------------------ ', i+1
# 		if i<len(data1):
# 			print data1[i]['key'], ": ", data1[i]['size']
# 		if i<len(data2):
# 			print data2[i]['key'], ": ", data2[i]['size']

if __name__ == "__main__":
	# open remote database
	client 	= pymongo.MongoClient('54.69.103.85', 27017)
	db 		= client.socialdoi
	filteredCtrl 	= db.naviHistLogsCtrl2.find({'action':'survey'})
	interestsCtrl 	= db.naviHistLogsCtrl2.find({'action':'finish'});
	navigationCtrl 	= db.naviHistLogsCtrl2.find({'action':'select'});

	filteredTrmt 	= db.naviHistLogsTreatment2.find({'action':'survey'})
	interestsTrmt 	= db.naviHistLogsTreatment2.find({'action':'finish'});
	navigationTrmt 	= db.naviHistLogsTreatment2.find({'action':'select'});
	



	#collect survey data
	surveyCtrl = {}
	for log in filteredCtrl:
		key = log['hit_id']+'/'+log['assignment_id']
		if surveyCtrl.has_key(key):
			print 'A worker participated in multiple hits! : ' + key  ## ERROR1: Duplicate Participation					
		else:
			surveyCtrl[key] = log;

	surveyTrmt = {}
	for log in filteredTrmt:
		key = log['hit_id']+'/'+log['assignment_id']
		if surveyTrmt.has_key(key):
			print 'A worker participated in multiple hits! : ' + key  ## ERROR1: Duplicate Participation					
		else:
			surveyTrmt[key] = log;


	# aggregate navigation histories
	control = [];
	for log in interestsCtrl:
		if surveyCtrl.has_key(log['hit_id']+'/'+log['assignment_id'])==False: # if no survey exists, discard this data
			continue	
		control.append(int(log['data']['timespan']));
	treatment = [];	
	for log in interestsTrmt:
		if surveyTrmt.has_key(log['hit_id']+'/'+log['assignment_id'])==False: # if no survey exists, discard this data
			continue
		treatment.append(int(log['data']['timespan']));	

	#print size;
	print "--------- Control ---------"
	cmd 	= np.median(control)
	ciqr75 	= np.percentile(control, 75)
	ciqr25 	= np.percentile(control, 25)
	ciqr 	= (ciqr75-ciqr25);
	print "median: ", cmd
	print "1.5*iqr: ", 1.5*ciqr



	for val in control:
		if val<(cmd-1.5*ciqr) or val>(cmd+1.5*ciqr):
			print val
			control.remove(val);
	print "meam: ", np.mean(control)
	print "std: ", np.std(control)
	print control
	print "--------- Treatment ---------"
	tmd 	= np.median(treatment)
	tiqr75 	= np.percentile(treatment, 75)
	tiqr25 	= np.percentile(treatment, 25)
	tiqr 	= (tiqr75-tiqr25)
	print "median: ", tmd
	print "1.5*iqr: ", 1.5*tiqr
	for val in treatment:
		if val<(tmd-1.5*tiqr) or val>(tmd+1.5*tiqr):
			print val
			treatment.remove(val);
	print "meam: ", np.mean(treatment)
	print "std: ", np.std(treatment)
	print treatment

	print stats.ttest_ind(treatment, control)
	# # ranking programs
	# autoCabinet = rank('cabinet', autoLogged)
	# autoDept	= rank('department', autoLogged)
	# autoProgram = rank('program', autoLogged)

	# userCabinet = rank('cabinet', userSpecified)
	# userDept	= rank('department', autoLogged)
	# userProgram = rank('program', userSpecified)	
	# print "Cabinet ===================================================================================="
	# # compare(userCabinet, autoCabinet, 10)
	# print "Department ===================================================================================="
	# # compare(userDept, autoDept, 10)
	# print "Program ===================================================================================="
	# compare(userProgram, autoProgram, 10)
	
	# print userProgram[-10:]
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