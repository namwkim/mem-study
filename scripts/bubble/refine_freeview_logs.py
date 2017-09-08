import os
import pymongo
import sys
import datetime
import csv
import itertools
from itertools import tee, izip
import numpy as np


def pairwise(iterable):
	"s -> (s0,s1), (s1,s2), (s2, s3), ..."
	a, b = tee(iterable)
	next(b, None)
	return izip(a, b)


def getKey(log):
	return log['hit_id'] + '/' + log['assignment_id'] + '/' + log['worker_id']


def splitKey(key):
	splited = key.split("/")
	return {'hit_id': splited[0], 'assignment_id': splited[1], 'worker_id': splited[2]}

if __name__ == "__main__":
	print sys.argv
	if len(sys.argv) < 3:
		print "provide 1) collection to refine 2) another collection to insert"
		sys.exit(0)

	# open log database
	dbauth = csv.reader(open(sys.argv[1], 'r')).next()
	dbauth[0] = dbauth[0].strip()
	dbauth[1] = dbauth[1].strip()

	dburl = 'mongodb://'+dbauth[0]+':'+dbauth[1]+'@54.69.103.85:27017/?authSource=admin'

	client = pymongo.MongoClient(dburl)
	db 		= client[sys.argv[2]]

	fromCol = db[sys.argv[3]]
	toCol = db[sys.argv[4]]
	toCol.remove({})

	# filter data

	# 1. create temp database containing filtered data
	tempHits = {}
	# sort and group by hit id
	sortedLogs = sorted(fromCol.find({}), key=lambda x: x['hit_id'])
	for k, g in itertools.groupby(sortedLogs, key=lambda x: x['hit_id']):
		tempHits[k] = list(g)

	print "# of HITs: ", len(tempHits.values())

	print 'filtering bad data...'
	hits = {}

	for hitID, hitData in tempHits.iteritems():  # loop over hits
		# sort by assignment id
		sortedLogs = sorted(hitData, key=lambda x: x['assignment_id'])
		print "============== ", hitID, " =============="
		assignments = {}
		# loop over assignment
		for k, g in itertools.groupby(sortedLogs, key=lambda x: x['assignment_id']):
			sortedLogs = sorted(list(g), key=lambda x: x['worker_id'])
			workers = {}
			 # loop over workers
			for wk, wg in itertools.groupby(sortedLogs, key=lambda x: x['worker_id']):
				# sort logs by timestamp
				sortedLogs = sorted(list(wg), key=lambda x: x['timestamp'])
				survey = filter(lambda x: x['action'] == "survey", sortedLogs)
				start = filter(lambda x: x['action'] == "start-experiment", sortedLogs)
				if len(survey) == 1 and len(start) == 1:
					workers[wk] = sortedLogs
			# there should be only one participant
			if len(workers.values()) == 1:
				assignments[k] = workers.values()[0]
			# elif len(workers.values()) > 1:
			# 	print "AssignmentID:", k, ' -  multiple workers participated'
			# else:
			# 	print "AssignmentID:", k, ' - no workers participated'

		if len(assignments.values()) == 0:
			print 'no assignments found: ', len(workers.values())
		else:
			print '# assignments', len(assignments.keys())
			hits[hitID] = assignments

	print 'constructing refined logs...'
	images = {}
	descMap = {}  # to find duplicate description
	CLICK_THRESHOLD = 1
	for hitID, hitData in hits.iteritems():
		for asmtID, asmtData in hitData.iteritems():
			# for workerID, workerData in asmtData.iteritems():
			print asmtID, ' len: ', len(asmtData)

			# start = filter(lambda x: x['action'] == "start-experiment", asmtData)
			# clicks = filter(lambda x: x['action'] == "click" and x['data']['is_practice'] == "false", asmtData)
			# survey = filter(lambda x: x['action'] == "survey", asmtData)

			start = filter(lambda x: x['action'] == "start-experiment", asmtData)
			clicks = filter(lambda x: x['action'] == "click" and x['data']['is_practice'] == "false" and x['data'].has_key('image'), asmtData)
			survey = filter(lambda x: x['action'] == "survey", asmtData)
			noclicks = filter(lambda x: x['action'] == "click" and x['data']['is_practice'] == "false" and x['data'].has_key('image')==False, asmtData)
			print asmtID, "'s invalid click count:", len(noclicks)

			for imageName, imageClicks in itertools.groupby(clicks, key=lambda x: x['data']['image']):
				imageName = imageName.split("/")[-1]#.split(".")[0]
				imageClicks = list(imageClicks)
				if images.has_key(imageName)==False:
					images[imageName] = { 'image': imageName, 'logs': [] }

				# 2) too small clicks (how can they describe without revealing images, suspicious!)
				if len(imageClicks)<=CLICK_THRESHOLD:
					print asmtID, ", ", imageName, " has too small click counts (=", len(imageClicks), ")"
					continue

				print 'saving... ', imageName, " (clicks = ", len(imageClicks), ")"
				images[imageName]['logs'].append({
						'id': hitID+"/"+asmtID,
						'clicks': imageClicks,
						'survey': survey[0] #there should be one survey
					});

	for image, imageData in images.iteritems():
		# 3) outlier removal
		# calc stats
		clickCounts = []
		for log in imageData['logs']:
			clickCounts.append(len(log['clicks']))
		if not clickCounts:
			print "ERROR: clickCounts is empty"
			continue
		median 	= np.median(clickCounts)
		iqr75 	= np.percentile(clickCounts, 75)
		iqr25   = np.percentile(clickCounts, 25)
		iqr 	= iqr75-iqr25;

		filtered = []
		for log in imageData['logs']:
			val = len(log['clicks'])
			if val<(iqr25-3*iqr) or val>(iqr75+3*iqr):
				print log['id'], " is removed as an outlier! (clickCount: ", val, ")"
			else:
				filtered.append(log)

		imageData['logs'] = filtered

		print image , " #of participants: ", len(imageData['logs'])
		print "median click count: ", median, ", iqr range: ", iqr25, " ~ ", iqr75
		# print len(imageData['logs'])
		toCol.insert(imageData)

	print len(images), " images saved."
