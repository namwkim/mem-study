import os
import pymongo
import sys
import datetime
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import itertools
def export2csv():
    client = pymongo.MongoClient('54.69.103.85', 27017)
    db = client.retargetstudy
    logs = db.logs
    condition = 1
    if condition == 1:
        finename = 'retarget-offline-GT.csv'
    else:
        finename = 'retarget-offline-Pred.csv'
    csvfile = open(finename, 'w')
    writer = csv.writer(csvfile)
    count = 0
    for log in logs.find({'data.study': 'retarget','hit_id':'OFFLINE', 'data.experiment':condition, 'action': 'submit'}):
        count +=1
        print log['worker_id']
        record = []
        record.append(log['hit_id'])
        record.append('HitTitle')
        record.append('Annotation')
        record.append(log['assignment_id'])
        record.append(log['worker_id'])
        record.append('Status')
        record.append('AcceptTime')
        record.append('SubmitTime')
        scores_final = ",".join(map(lambda x : str(x), list(itertools.chain.from_iterable(log['data']['scores_final']))))
        file_names_seen = ",".join(log['data']['file_names_seen'])
        thumbnail_order_seen = ",".join(map(lambda x : str(x), list(itertools.chain.from_iterable(log['data']['thumbnail_order_seen']))))
        record.append("scores_final:" + scores_final)
        record.append("file_names_seen:" + file_names_seen)
        record.append("thumbnail_order_seen:" + thumbnail_order_seen)
        writer.writerow(record)
    print count, 'results found.'
    condition = 1
    if condition == 1:
        finename = 'color-offline-GT.csv'
    else:
        finename = 'color-offline-Pred.csv'
    csvfile = open(finename, 'w')
    writer = csv.writer(csvfile)
    count = 0
    for log in logs.find({'data.study': 'color','hit_id':'OFFLINE', 'data.experiment':condition, 'action': 'submit'}):
        count +=1
        print log['worker_id']
        record = []
        record.append(log['hit_id'])
        record.append('HitTitle')
        record.append('Annotation')
        record.append(log['assignment_id'])
        record.append(log['worker_id'])
        record.append('Status')
        record.append('AcceptTime')
        record.append('SubmitTime')
        scores_final = ",".join(map(lambda x : str(x), list(itertools.chain.from_iterable(log['data']['scores_final']))))
        file_names_seen = ",".join(log['data']['file_names_seen'])
        thumbnail_order_seen = ",".join(map(lambda x : str(x), list(itertools.chain.from_iterable(log['data']['thumbnail_order_seen']))))
        record.append("scores_final:" + scores_final)
        record.append("file_names_seen:" + file_names_seen)
        record.append("thumbnail_order_seen:" + thumbnail_order_seen)
        writer.writerow(record)
    print count, 'results found.'

if __name__ == "__main__":
	export2csv()
