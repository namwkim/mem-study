import os
import pymongo
import sys
import datetime
import csv
from PIL import Image

def export2csv(colname, clickout, descout):  # , filterList):
    # open log database
    client = pymongo.MongoClient('54.69.103.85', 27017)
    db = client.websalystudy
    logs = db[colname]

    imageMap = {}
    for root, dirs, files in os.walk("./targets_websaly"):
        for file in files:
            if file.startswith('.'):
                continue
            im=Image.open("./targets_websaly/" + file)
            imageMap[file] = im.size

    with open(descout, 'wb') as descfile:
        csvdesc = csv.writer(descfile,quoting=csv.QUOTE_NONNUMERIC)
        with open(clickout, 'wb') as clickfile:
            csvclick = csv.writer(clickfile)
            for log in logs.find({}):
                if len(log['logs']) == 0:
                    print "no logs are found for ", log['image']
                    continue
                print 'saving clicks and descriptions from image - ', log['image']

                img = log['image'] + ".png"

                for asmt in log['logs']:
                    # print asmt
                    user = asmt['id'].split("/")[1]

                    # click data
                    for click in asmt['clicks']:
                        time = datetime.datetime.fromtimestamp(
                            int(click['timestamp']) / 1e3).strftime('%Y-%m-%d %H:%M:%S')

                        if imageMap[img]==1360:
                            # print "--image-dim", imageMap[img]
                            fx = (1.360)*float(click['data']['center_x'])
                            fy = (1.360)*float(click['data']['center_y'])
                        else:
                            # print "--image-dim", imageMap[img]
                            fx = (1.366)*float(click['data']['center_x'])
                            fy = (1.366)*float(click['data']['center_y'])
                        # fx = click['data']['center_x']
                        # fy = click['data']['center_y']
                        csvclick.writerow([time, img, user, fx, fy])

                    # desc data
                    time = datetime.datetime.fromtimestamp(
                        int(asmt['desc']['timestamp']) / 1e3).strftime('%Y-%m-%d %H:%M:%S')
                    desc = asmt['desc']['data']['desc'].replace('\n', ' ').replace('\r', '')
                    row = [time, img, user, 0, 'final', desc]
                    csvdesc.writerow(
                        [s.encode('utf-8') if isinstance(s, unicode) else s for s in row])

                    # desc change data
                    groupId = 1
                    for diff in asmt['diffs']:
                        time = datetime.datetime.fromtimestamp(
                            int(diff['timestamp']) / 1e3).strftime('%Y-%m-%d %H:%M:%S')
                        for chg in diff['data']['desc_log']:
                            chgType = 'unchanged'
                            if chg.has_key('added'):
                                chgType = 'added'
                            elif chg.has_key('removed'):
                                chgType = 'removed'
                                # if isinstance(chg['value'], unicode) else
                                # chg['value']
                            val = chg['value'].replace('\n', ' ').replace('\r', '')
                            row = [time, img, user, groupId, chgType, val]
                            csvdesc.writerow(
                                [s.encode('utf-8') if isinstance(s, unicode) else s for s in row])
                            groupId += 1


if __name__ == "__main__":
    # e.g python log2csv.py click.csv  desc.csv
    export2csv(sys.argv[1], sys.argv[2], sys.argv[3])  # , sys.argv[3])
