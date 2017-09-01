import os, pymongo, sys, random, time, csv
from shutil import copyfile

if __name__ == "__main__":
    source_dir = "../stimuli-done/";
    target_dir = "../../bubble-db-pilot/targets/";
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    sources = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.startswith('.'):
                continue
            sources.append(file)

    sampled = random.sample(sources, 30)
    print sampled
    targets = [];
    for file in sampled:
        copyfile(source_dir+file, target_dir+file)
        targets.append(file)

    print len(targets)
