import os
import sys
from shutil import copyfile

images = []
source_dir = "../stimuli/";
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.startswith('.'):
            continue
        images.append(file)

batchIdx    = 1
batchSize   = 360 #123

totalNum = len(images)
currIdx   = 1
for image in images:
    target_dir = "../batch-"+str(batchIdx)+"/";
    if not os.path.exists(target_dir):
    	os.makedirs(target_dir)
    copyfile(source_dir+image, target_dir+image)
    currIdx+=1
    if currIdx>batchSize:
        batchIdx+=1
        currIdx = 1
