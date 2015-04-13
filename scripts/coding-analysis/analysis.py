import os, pymongo, sys, datetime, csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from collections import Counter
def compareRatings(expertRatingFilename):
	
	# open log database
	client 	= pymongo.MongoClient('54.69.103.85', 27017)
	db 		= client.coding
	logs 	= db.logs
	#collect survey data
	crowdRating = {}
	ratings = logs.find({'action':'evalute', 'data.is_practice':'false'})
	for rating in ratings:
		imageName 	= rating['data']['image'].split('/')[4].rstrip('.png').lower()
		pid 		= rating['data']['pid']
		quality 	= int(rating['data']['rating'])
		key 		= imageName+":"+pid
		if crowdRating.has_key(key)==False:
			crowdRating[key] = []
		crowdRating[key].append(quality)
		#print imageName, pid, quality

	print crowdRating
	# read image-description pairs
	expertRating = {}
	with open(expertRatingFilename, 'rU') as csvfile:	
		codingreader = csv.reader(csvfile)
		next(codingreader, None); # skip header
		
		
		curImage = ""
		removed  = False
		for row in codingreader:
			if row[1] == "":# -> image number
				# if row[1] == "REMOVED":
				# 	removed = True
				# else:
				# 	removed = False

				curImage = row[9].split("=")[3].split(".")[0].lower()
				
				
				
			elif removed!=True:
				#print '---'
				#print curImage, row[0], row[9]
				key = curImage + ":"+row[0]
				if expertRating.has_key(key)==False:
					expertRating[key] = []
				expertRating[key].append(int(row[1]))
				#codings = codingMap[curImage]
				#coding = Coding(curImage, row[1], row[2], row[3], row[4], row[5], row[6].split(','), row[7], row[8], row[9])
				#codings.append(coding)
				#print curImage, row[1], row[2], row[3], row[4], row[5], row[6].split(','), row[7], row[8]
	print expertRating

	crowdvals = []
	expertvals = []
	for key in crowdRating:
		crowd  = crowdRating[key]
		expert = expertRating[key]
		c = Counter(crowd);
		val, cnt =  c.most_common()[0]
		convVal = convert(val, 1.0, 5.0, 0.0, 3.0);
		crowdvals.append(convVal)
		expertvals.append(np.mean(expert))
		print convVal, expert
	paired_sample = stats.ttest_rel(expertvals, crowdvals)
	print "The t-statistic is %.3f and the p-value is %.3f." % paired_sample

	# Plot values
	x = np.arange(len(crowdvals))
	width = 0.35

	plt.subplots()
	rects1 = plt.bar(x, crowdvals,  width, color='r')
	rects2 = plt.bar(x+width, expertvals, width, color='y')
	plt.title('Crowd vs Expert Ratings')
	plt.legend( (rects1[0], rects2[0]), ('Crowd', 'Expert') )
	plt.show()

def convert(oldVal, oldMin, oldMax, newMin, newMax):
	newVal = (((oldVal - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin
	return newVal
if __name__ == "__main__":
	#e.g python log2csv.py click.csv  desc.csv filter.csv
	compareRatings(sys.argv[1])