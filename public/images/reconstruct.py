import os, pymongo, sys, random, time, csv
from shutil import copyfile

# load file names from all5k
images = {}
for root, dirs, files in os.walk('./all5k/'):
    for file in files:
        if file.startswith('.'):
            continue
        images[file] = file

# create a temporary directory
temp_dir = "./temp_dir/";
if not os.path.exists(temp_dir):
	os.makedirs(temp_dir)

# for all files
for root, dirs, files in os.walk('./all5k-reduced/'):
    for file in files:
        if file.startswith('.'):
            continue
        if images.has_key(file):# check if names matched
            # copy original file
            copyfile('./all5k-reduced/'+file, temp_dir+file)
