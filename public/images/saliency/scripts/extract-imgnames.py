# extract previously used images (from bubble study)
# it should be 202 images
import os
import pymongo
import sys
import random
import time
import csv
from shutil import move
# extract-imgtypes.py
client = pymongo.MongoClient('54.69.103.85', 27017)
db = client.bubblestudy

imageNames = {}
colNames = ["16", "24", "32", "24_Dec", "32_Dec", "40_Dec", "32_Feb"]

for colName in colNames:
    print 'extracting image names from ', ("refinedLogs"+colName)
    logs = db["refinedLogs"+colName]
    for log in logs.find():
        imageNames[log["image"]+".png"] = True
print 'count:', len(imageNames.values())

source_dir = "../stimuli/";
target_dir = "../stimuli-done/";
if not os.path.exists(target_dir):
	os.makedirs(target_dir)

for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.startswith('.'):
            continue
        if imageNames.has_key(file):
            print file
            move(source_dir+file, target_dir+file)
