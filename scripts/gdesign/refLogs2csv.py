import os, pymongo, sys, datetime, csv
from PIL import Image

def export2csv(dbname, collection, csvout, ext):#, filterList):
	# open log database
	client 	= pymongo.MongoClient('54.69.103.85', 27017)
	db 		= client[dbname]
	logs 	= db[collection]

	with open(csvout, 'wb') as clickfile:
		csvclick = csv.writer(clickfile)
		for log in logs.find({}):
			if len(log['logs'])==0:
				print "no logs are found for ", log['image']
				continue
			print 'saving clicks and descriptions from image - ', log['image']

			img  = log['image'] + ext

			for asmt in log['logs']:
				# print asmt
				user = asmt['id'].split("/")[1]

				# click data
				for click in asmt['clicks']:
					time = datetime.datetime.fromtimestamp(int(click['timestamp']) / 1e3).strftime('%Y-%m-%d %H:%M:%S')
					fx = click['data']['center_x']
					fy = click['data']['center_y']
					csvclick.writerow([time, img, user, fx, fy])

if __name__ == "__main__":
	if len(sys.argv) < 3:
	    print "provide a collection name and output filename."
	    sys.exit(0)
	#e.g python log2csv.py click.csv  desc.csv, ext
	export2csv(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]) #, sys.argv[3])
