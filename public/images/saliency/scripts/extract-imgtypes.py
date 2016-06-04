import os
import pymongo
import sys
import random
import time
import csv
# extract-imgtypes.py
client = pymongo.MongoClient('localhost', 27017)
db = client.saliency
checks = db.checks

imgType = {}
for chk in checks.find():
    if chk['rater'] != "Nam":
        continue
    if "is_graphic" in chk and chk["is_graphic"] == "true":
        imgType[chk['image']] = 'graphic_design'
    elif "is_table" in chk and chk["is_table"] == "true":
        imgType[chk['image']] = 'table'
    elif "is_infographic" in chk and chk["is_infographic"] == "true":
        imgType[chk['image']] = 'infographic'
    else:
        imgType[chk['image']] = 'datavis'

source_dir = "../stimuli/";
with open('image_types.csv', 'wb') as clickfile:
    csvtype = csv.writer(clickfile)
    csvtype.writerow(['image','type'])
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.startswith('.'):
                continue
            if imgType.has_key(file):
                csvtype.writerow([file,imgType[file]])
