import os, pymongo, sys, random, time, csv
from shutil import copyfile


# extract stimuli from agreed images
client  = pymongo.MongoClient('54.69.103.85', 27017)
db = client.saliency
checks = db.checks

imgToUse = {}
imgCnt = 0
for chk in checks.find():
    if chk['rater']=="Zoya" and chk["use"]=="true":
        imgToUse[chk['image']] = True
        imgCnt += 1

print "stimuli size:", imgCnt

# move the images to the final stimuli folder
source_dir = "./all5k-reduced/";
target_dir = "./saliency-db/";
if not os.path.exists(target_dir):
	os.makedirs(target_dir)

for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.startswith('.'):
            continue
        if imgToUse.has_key(file):
            imgToUse[file] = False
            copyfile(source_dir+file, target_dir+file)

for img in imgToUse:
    if imgToUse[img]==True:
        print img
