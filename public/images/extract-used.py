import os, pymongo, sys, random, time, csv
from shutil import copyfile

if __name__ == "__main__":
    source_dir = "./bubble-db/targets_blurred/";
    target_dir = "./bubble-db-pilot/targets_blurred/";
    sources = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.startswith('.'):
                continue
            sources.append(file)
    filter_dirs = ["./bubble-db-pilot/targets"];

    filters = []
    for filter_dir in filter_dirs:
        # print filter_dir
        for root, dirs, files in os.walk(filter_dir):
            for file in files:
                if file.startswith('.'):
                    continue
                filters.append(file)
    targets = [];
    for file in sources:
        if file in filters:
            print file
            copyfile(source_dir+file, target_dir+file)
            targets.append(file)

    print len(targets)
