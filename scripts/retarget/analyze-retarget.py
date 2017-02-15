# import os
# import pymongo
# import sys
# import datetime
# import csv
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy import stats
# def export2csv():
# 	dbauth = csv.reader(open('../../auth.txt', 'r')).next()
# 	dbauth[0] = dbauth[0].strip()
# 	dbauth[1] = dbauth[1].strip()
#
# 	dburl = 'mongodb://'+dbauth[0]+':'+dbauth[1]+'@localhost:27017/?authSource=admin'
#
# 	client = pymongo.MongoClient(dburl)
# 	db = client.retargetstudy
# 	logs = db.logs
# 	experiment = 1
# 	sentinels = ["47_113569013_faed4e79cd_b.png", "146_344098515_af4947bcfa_b.png"]
# 	if experiment == 1:
# 		imagetypes = ["Resized", "Edge_energy", "GT_imp","GT_imp_crop", "GT_imp_straight", "Jumbled"]
# 	else:
# 		imagetypes = ["Resized", "Edge_energy", "Pred_imp","Pred_imp_crop", "Pred_imp_straight", "Jumbled"]
# 	method_score_map = {}
# 	for imagetype in imagetypes:
# 		method_score_map[imagetype] = []
# 	for log in logs.find({'data.study': 'retarget','action': 'submit'}):
# 		if experiment != log['data']['experiment']:
# 			continue
# 		thumbnail_order_seen = log['data']['thumbnail_order_seen']
# 		scores_final = log['data']['scores_final']
# 		file_names_scene = log['data']['file_names_seen']
# 		for i, filename in enumerate(file_names_scene):
# 			if filename in sentinels:
# 				continue
# 			for j, imagetype in enumerate(thumbnail_order_seen[i]):
# 				method_score_map[imagetype].append(scores_final[i][j])
# 	for key, value in method_score_map.iteritems():
# 		print key, np.mean(value), np.std(value)

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



if __name__ == "__main__":
	# fromdb()
	with open('retarget-feb.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		header = next(reader)
		# print header
		# count = 0
		method_score_map = {}
		sentinels = ["47_113569013_faed4e79cd_b.png", "146_344098515_af4947bcfa_b.png"]
		for row in reader:
			if len(row[8].split(':'))==1:
				continue
			# print row
			# count+=1
			# print cond, row[4], row[6], row[7]
			# start = datetime.strptime(row[6], '%a %b %d %H:%M:%S PST %Y')
			# end = datetime.strptime(row[7], '%a %b %d %H:%M:%S PST %Y')
			# diff = (end-start).total_seconds()
			# print diff
			# print row[8]
			scores_final = row[8].split(':')[1].split(',')
			file_names_scene = row[9].split(':')[1].split(',')
			thumbnail_order_seen = row[10].split(':')[1].split(',')
			# print scores_final
			# print file_names_scene
			# print thumbnail_order_seen

			for i, imagetype in enumerate(thumbnail_order_seen):
				if method_score_map.has_key(imagetype)==False:
					method_score_map[imagetype] = []
				method_score_map[imagetype].append(int(scores_final[i]))


		for key1, value1 in method_score_map.iteritems():
			print key1, np.mean(value1), np.std(value1)
			for key2, value2 in method_score_map.iteritems():
				if key1==key2:
					continue;
				print '--', key2, ':', np.mean(value2),
				print '--', stats.ttest_rel(value1, value2)[1]<0.05
