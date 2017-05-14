import os, pymongo, sys, datetime, csv


def export2csv(collection, csvout):#, filterList):
	# open log database
	# open log database
	dbauth = csv.reader(open('../../auth.txt', 'r')).next()
	dbauth[0] = dbauth[0].strip()
	dbauth[1] = dbauth[1].strip()

	dburl = 'mongodb://'+dbauth[0]+':'+dbauth[1]+'@54.69.103.85:27017/?authSource=admin'

	client = pymongo.MongoClient(dburl)
	db 		= client.osiestudy
	
	logs 	= db[collection]

	with open(csvout, 'wb') as clickfile:
		csvclick = csv.writer(clickfile)
		for log in logs.find({}):
			if len(log['logs'])==0:
				print "no logs are found for ", log['image']
				continue
			print 'saving clicks and descriptions from image - ', log['image']

			img  = log['image'] + ".jpg"

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
	#e.g python log2csv.py click.csv  desc.csv
	export2csv(sys.argv[1], sys.argv[2]) #, sys.argv[3])
