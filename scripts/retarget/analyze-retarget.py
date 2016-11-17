import os
import pymongo
import sys
import datetime
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
def export2csv():
	client = pymongo.MongoClient('54.69.103.85', 27017)
	db = client.retargetstudy
	logs = db.logs
	experiment = 1
	sentinels = ["47_113569013_faed4e79cd_b.png", "146_344098515_af4947bcfa_b.png"]
	if experiment == 1:
		imagetypes = ["Resized", "Edge_energy", "GT_imp","GT_imp_crop", "GT_imp_straight", "Jumbled"]
	else:
		imagetypes = ["Resized", "Edge_energy", "Pred_imp","Pred_imp_crop", "Pred_imp_straight", "Jumbled"]
	method_score_map = {}
	for imagetype in imagetypes:
		method_score_map[imagetype] = []
	for log in logs.find({'data.study': 'retarget','action': 'submit'}):
		if experiment != log['data']['experiment']:
			continue
		thumbnail_order_seen = log['data']['thumbnail_order_seen']
		scores_final = log['data']['scores_final']
		file_names_scene = log['data']['file_names_seen']
		for i, filename in enumerate(file_names_scene):
			if filename in sentinels:
				continue
			for j, imagetype in enumerate(thumbnail_order_seen[i]):
				method_score_map[imagetype].append(scores_final[i][j])
	for key, value in method_score_map.iteritems():
		print key, np.mean(value), np.std(value)
if __name__ == "__main__":
	export2csv()
