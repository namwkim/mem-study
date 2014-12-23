import os, pymongo, sys, datetime


def export2csv(csvfile):
	client 	= pymongo.MongoClient('localhost', 27017)
	db 		= client.bubblestudy
	logs	= db.logs.find()

	for log in logs:
		if log['action']!="explain":
			continue
		if log['data']['is_practice'] != "false":
			continue
		time = datetime.datetime.fromtimestamp(int(log['timestamp']) / 1e3).strftime('%Y-%m-%d %H:%M:%S')
		print str(time) + ", " + log['hit_id'] + ", " + log['assignment_id'] + ", " + log['worker_id'] + ', ' + log['data']['image'] + ', ' + log['data']['desc']
if __name__ == "__main__":
	export2csv(sys.argv[1])