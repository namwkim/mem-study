import os
import pymongo
import sys
import random
import time
import csv
import math


# collect target image filenames
targets = {}
image_folder = "../../images/annotate/"
for root, dirs, files in os.walk(image_folder):
	for filename in files:
		if filename.startswith('.') or filename.endswith('jpg') == False:
			continue

		splited = filename.split('_')
		# print splited[0]
		if targets.has_key(splited[0]) == False:
			targets[splited[0]] = []
		targets[splited[0]].append(filename)
# shuffle
maxVar = 0
for key,value in targets.iteritems():
	random.shuffle(value)
	print key, len(value)
	if len(value)>maxVar:
		maxVar = len(value)

# generate files, each of which contains 11 files
base = './hit'
for i in xrange(maxVar):
	print i
	with open(base+str(i), 'w') as f:
		files = []
		for value in targets.values():
			if i<len(value):
				files.append(image_folder+value[i])
			else:
				files.append(image_folder+random.choice(value))
		ridx = random.randrange(len(files)+1)
		rfname = random.choice(files)
		print 'insert filer at', ridx, rfname
		files.insert(ridx, rfname)
		for j, filepath in enumerate(files):
			f.write(filepath)
			if j<len(files)-1:
				f.write('\n')
