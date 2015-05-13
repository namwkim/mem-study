
import os, pymongo, sys, datetime, csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from collections import Counter


if __name__ == "__main__":
	# open remote database
	client 	= pymongo.MongoClient('54.69.103.85', 27017)
	db 		= client.bubblestudy
	refinedLogs = db.refinedLogs.find({})
	print refinedLogs.count()

	localClient = pymongo.MongoClient('localhost', 27017)
	localDb 	= localClient.bubblestudy
	
	localDb.refinedLogs.remove({})
	print 'Start copying refined logs from remote to local db'
	i=0
	for log in refinedLogs:
		i+=1
		print i
		localDb.refinedLogs.insert(log)

	print 'Done (Total:', i, ")"