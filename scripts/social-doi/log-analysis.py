import os, pymongo, sys, random, csv, itertools


if __name__ == "__main__":
	client 	= pymongo.MongoClient('localhost', 27017)
	db 		= client.socialdoi
	logs	= db.logs


	# group by participants
		# 1. interest item count
		# 2. navigation count
		# 3. time (start-experiment, finish)
		