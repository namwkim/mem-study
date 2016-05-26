import os, pymongo, sys, random, time, csv, urllib2, shutil
from PIL import Image

# load csv
url = 'https://raw.githubusercontent.com/massvis/dataset/master/csv_files/all5k_metadata.csv'
res = urllib2.urlopen(url)
cr  = csv.reader(res)
next(cr)

labelMap = {}
for row in cr:
    filename = os.path.splitext(row[0])[0]
    source   = row[2]
    # print filename, source
    labelMap[filename] = (filename, source)

# mkdir filtered
if not os.path.exists('filtered_all5k'):
	os.makedirs('filtered_all5k')
print 'label size', len(labelMap)
# filter image names
source_dir = "./all5k";
for root, dirs, files in os.walk(source_dir):
	print 'len', len(files)
	for file in files:
		if file.startswith('.'):
			continue
		# print file
		filename = os.path.splitext(file)[0]
		# print filename
		if labelMap.has_key(filename) and labelMap[filename][1]=="S":
			print labelMap[filename]
        		# move filtered images
        		shutil.move('./all5k/'+file, './filtered_all5k/'+file)
        	if os.path.isfile("./all5k/" + file):
                	try:
                    		im=Image.open("./all5k/" + file)
                	except IOError as msg:
                		print file, 'is not recognized (', msg,')'
				shutil.move('./all5k/'+file, './filtered_all5k/'+file)
                    		continue
    			ratio = im.size[0]/float(im.size[1])
    			if ratio<0.5 or ratio > 2.0:
    				print filename, ratio #, labelMap[filename][1]
    				shutil.move('./all5k/'+file, './filtered_all5k/'+file)
