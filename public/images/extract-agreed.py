import os, pymongo, sys, random, time, csv
from shutil import move

# extract ratings
client  = pymongo.MongoClient('localhost', 27017)
db = client.saliency
checks = db.checks
zoya = {}
nam  = {}
images = {}
for chk in checks.find():
    images[chk['image']] = chk['image']
    if chk['rater']=="Nam":
        nam[chk['image']] = chk["use"]
    else:
        zoya[chk['image']] = chk["use"]
# divide images disagreed & agreed
imgAgreed = {}

aCnt = 0
dCnt = 0
for img in images.values():
    try:
        if zoya[img]==nam[img]:
            aCnt += 1
            imgAgreed[img] = True
        else:
            dCnt += 1
            imgAgreed[img] = False
    except KeyError:
        dCnt += 1
        imgAgreed[img] = False
print "agreed:", aCnt
print "disagreed:", dCnt
# move agreed to a separate folder
source_dir = "./all5k/";
target_dir = "./all5k-agreed/";
if not os.path.exists(target_dir):
	os.makedirs(target_dir)

for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.startswith('.'):
            continue
        if imgAgreed.has_key(file) and imgAgreed[file]==True:
            move(source_dir+file, target_dir+file)
