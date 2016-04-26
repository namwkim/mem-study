import os
import pymongo
import sys
import random
import time
import csv, shutil

target_dir = "targets_gdesign/"
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

count = 1
source_dir = "/Users/namwkim85/Downloads/importanceTest/"
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.startswith('.'):
            continue
        filename, file_extension = os.path.splitext(file)
        if file_extension=='.jpg':
            isfile = len(filename.split("_"))
            if isfile==4:
                print file, count
                count+=1
                shutil.copy2(source_dir+file, target_dir+file)
