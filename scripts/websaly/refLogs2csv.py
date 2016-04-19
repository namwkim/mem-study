import os, pymongo, sys, datetime, csv
from PIL import Image

def export2csv(collection, csvout):#, filterList):
	# open log database
	client 	= pymongo.MongoClient('54.69.103.85', 27017)
	db 		= client.websalystudy
	logs 	= db[collection]


	imageMap = {}
	for root, dirs, files in os.walk("./targets_websaly"):
		for file in files:
			if file.startswith('.'):
				continue
			im=Image.open("./targets_websaly/" + file)
			imageMap[file] = im.size

	with open(csvout, 'wb') as clickfile:
		csvclick = csv.writer(clickfile)
		for log in logs.find({}):
			if len(log['logs'])==0:
				print "no logs are found for ", log['image']
				continue
			print 'saving clicks and descriptions from image - ', log['image']

			img  = log['image'] + ".png"

			for asmt in log['logs']:
				# print asmt
				user = asmt['id'].split("/")[1]

				# click data
				for click in asmt['clicks']:
					time = datetime.datetime.fromtimestamp(int(click['timestamp']) / 1e3).strftime('%Y-%m-%d %H:%M:%S')

					if imageMap[img]==1360:
						# print "--image-dim", imageMap[img]
						fx = (1.360)*float(click['data']['center_x'])
						fy = (1.360)*float(click['data']['center_y'])
					else:
						# print "--image-dim", imageMap[img]
						fx = (1.366)*float(click['data']['center_x'])
						fy = (1.366)*float(click['data']['center_y'])
					csvclick.writerow([time, img, user, fx, fy])


if __name__ == "__main__":
	if len(sys.argv) < 3:
	    print "provide a collection name and output filename."
	    sys.exit(0)
	#e.g python log2csv.py click.csv  desc.csv
	export2csv(sys.argv[1], sys.argv[2]) #, sys.argv[3])
