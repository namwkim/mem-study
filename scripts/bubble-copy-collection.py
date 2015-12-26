
import os, pymongo, sys, datetime, csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from collections import Counter


if __name__ == "__main__":
	# open remote database
	client 	= pymongo.MongoClient('54.69.103.85', 27017)
	db 		= client.bubblestudy
	fromColl = db.logs32_Dec.find({})
	print fromColl.count()

	localClient = pymongo.MongoClient('localhost', 27017)
	localDb 	= localClient.bubblestudy
	toColl 		= localDb.logs32_Dec
	toColl.remove({})
	
	print 'Start copying refined logs from remote to local db'
	i=0
	for log in fromColl:
		i+=1
		print i
		toColl.insert(log)

	print 'Done (Total:', i, ")"