import os
import pymongo
import sys
import datetime
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from datetime import datetime
from dateutil import parser
from math import sqrt
# def fromdb():
#     client = pymongo.MongoClient('54.69.103.85', 27017)
#     db = client.retargetstudy
#     logs = db.logs
#     experiment = 0
#
#     count = 0
#     for log in logs.find({'data.study': 'thumbnail', 'action':'submit', 'hit_id': '3DFYDSXB2W0Q0E4ACPV6SDTBE1IJUV'}):
#         # print log['hit_id']
#         count += 1
#     print 'total records(DB)', count

def extract_cond(col):
    images = col.split(':')
    images = ''.join(images[1:])
    if len(images)==0:
        return False
    images = images.split(',')
    cond =  images[0].split('/')[5]
    return cond
if __name__ == "__main__":
    # fromdb()
    with open('thumbnail-jan-26.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        print header
        count = 0
        experiment = {
            'thumbnails0':[],
            'thumbnails8_pred':[]
        }

        for row in reader:
            # print row
            count+=1
            cond = extract_cond(row[8])
            if cond==False:
                continue;
            # condition = images[0].split('/')[5]
            # print 'condition', condition
            images = row[8].split(':')
            images = ''.join(images[1:])
            images = images.split(',')
            print cond, row[4], len(images), images
            # start = datetime.strptime(row[6], '%a %b %d %H:%M:%S PDT %Y')
            # end = datetime.strptime(row[7], '%a %b %d %H:%M:%S PDT %Y')
            # diff = (end-start).total_seconds()
            # print diff
            experiment[cond].append(len(images))

        finaldata = []
        print 'Total records:', count

        for key, values in experiment.iteritems():
            print '========================================='
            print 'Condition:',key
            median  = np.median(values)
            iqr75 	= np.percentile(values, 75)
            iqr25   = np.percentile(values, 25)
            iqr 	= iqr75-iqr25;
            print '--Count', len(values)
            print '--Min', np.min(values)
            print '--Max', np.max(values)
            print '--Median', median
            print '--IQR75', iqr75
            print '--IQR25', iqr25
            print '--IQR*3', iqr*3
            print '--Low Bar', (iqr25-3*iqr)
            print '--High Bar', (iqr75+3*iqr)
            filtered = []
            for val in values:
                if val<(iqr25-3*iqr) or val>(iqr75+3*iqr):
                    print val, ': outlier.'
                else:
                    filtered.append(val)
            print '--Median (Filtered)', np.median(filtered)
            print '--Mean (Filtered)', np.mean(filtered)
            print '--Std (Filtered)', np.std(filtered)

            finaldata.append(filtered)
        print 'p-value (ind.ttest):', stats.ttest_ind(finaldata[0], finaldata[1])[1]
        cohens_d = (np.mean(finaldata[0]) - np.mean(finaldata[1])) / (sqrt((np.std(finaldata[0]) ** 2 + np.std(finaldata[1]) ** 2) / 2))
        print 'cohens_d:', cohens_d
        # print '============= final =============='
        # for key, value in filtered.iteritems():
        #     print key, len(value)
        #     median  = np.median(value)
        #     iqr75 	= np.percentile(value, 75)
        #     iqr25   = np.percentile(value, 25)
        #     iqr 	= iqr75-iqr25;
        #     print '--Median', median
        #     print '--IQR75', iqr75
        #     print '--IQR25', iqr25
        #     print '--IQR*3', iqr*3
