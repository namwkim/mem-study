import os
import pymongo
import sys
import datetime
import csv
import itertools
from itertools import tee, izip
import numpy as np

if __name__ == "__main__":
    # open log database
    client = pymongo.MongoClient('54.69.103.85', 27017)
    # client 	= pymongo.MongoClient('localhost', 27017)
    db = client.gdesignstudy
    logs = list(db.refLogs30x50.find())

    filterRates = []
    assignments = []
    avgClicks = []
    for log in logs:
        # reconstruct filtering rate
        filterRates.append(float(15-len(log['logs']))/15*100.0)
        assignments.append(len(log['logs']))
        clicks = []
        for assignment in log['logs']:
            clicks.append(len(assignment['clicks']))
        avgClicks.append(np.mean(clicks))
        # print log['image'] , " #of participants: ", len(log['logs'])

    print 'AVG.FILTERRATE-% (MEAN, STD):', "M={0:.2f}".format(np.mean(filterRates))+', '+\
        "SD={0:.2f}".format(np.std(filterRates))
    print 'AVG.ASMT-MIN (MEAN, STD):', "M={0:.2f}".format(np.mean(assignments))+', '+\
        "SD={0:.2f}".format(np.std(assignments))+" (min={0:.2f}".format(min(assignments))+')'
    print 'AVG.CLICK PER IMAGE (MEAN, STD):', "M={0:.2f}".format(np.mean(avgClicks))+', '+\
        "SD={0:.2f}".format(np.std(avgClicks))
    
