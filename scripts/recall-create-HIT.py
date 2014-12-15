from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
import os, pymongo, sys

######  AMT CONFIGURATION PARAMETRS  ######

SANDBOX = True  # Select whether to post to the sandbox (using fake money), or live MTurk site (using REAL money)
HIT_URL = "https://study.namwkim.org/recall"  # Provide the URL that you want workers to sent sent to complete you task

NUMBER_OF_HITS = 5  # Number of different HITs posted for this task
NUMBER_OF_ASSIGNMENTS = 20  # Number of tasks that DIFFERENT workers will be able to take for each HIT
LIFETIME = 60 * 60 * 24 * 7  # How long that the task will stay visible if not taken by a worker (in seconds)
REWARD = 0.5  # Base payment value for completing the task (in dollars)
DURATION = 60*20  # How long the worker will be able to work on a single task (in seconds)
APPROVAL_DELAY = 60*60*24*7  # How long after the task is completed will the worker be automatically paid if not manually approved (in seconds)


# HIT title (as it will appear on the public listing)
TITLE = 'Visualization Recall Study'
# Description of the HIT that workers will see when deciding to accept it or not
DESCRIPTION = 'See a visualization image and describe it!'
# Search terms for the HIT posting
KEYWORDS = ['Image', 'Visualization', 'Describe']


# Your Amazon Web Services Access Key (private)
AWS_ACCESS_KEY = ''
# Your Amazon Web Services Secret Key (private)
AWS_SECRET_KEY = ''
# Your Amazon Web Services IAM User Name (private)

######  BUBBLE CONFIGURATION PARAMETRS  ######
BASE_URI = "/images/recall-db/"
#######################################


def create_hits(keyfile):
	# read a keyfile
	with open(keyfile, 'r') as f:
		AWS_ACCESS_KEY = f.readline().split('=')[1].rstrip('\r\n')
		AWS_SECRET_KEY = f.readline().split('=')[1].rstrip('\r\n')

	print AWS_ACCESS_KEY
	print AWS_SECRET_KEY

	if SANDBOX:
		mturk_url = 'mechanicalturk.sandbox.amazonaws.com'
		preview_url = 'https://workersandbox.mturk.com/mturk/preview?groupId='
	else:
		mturk_url = 'mechanicalturk.amazonaws.com'
		preview_url = 'https://mturk.com/mturk/preview?groupId='

	q = ExternalQuestion(external_url=HIT_URL, frame_height=800)
	conn = MTurkConnection(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, host=mturk_url)
	hitIDs = []
	for i in range(0, NUMBER_OF_HITS):
		create_hit_rs = conn.create_hit(question=q, lifetime=LIFETIME, max_assignments=NUMBER_OF_ASSIGNMENTS, title=TITLE, keywords=KEYWORDS, reward=REWARD, duration=DURATION, approval_delay=APPROVAL_DELAY, annotation=DESCRIPTION)
		print(preview_url + create_hit_rs[0].HITTypeId)
		print("HIT ID: " + create_hit_rs[0].HITId)

		# save HIT IDs
		hitIDs.append(create_hit_rs[0].HITId); 

	# collect target image filenames
	targets = []
	for root, dirs, files in os.walk("../public/images/recall-db/"):		
		for file in files:		
			if file.startswith('.'):
				continue
			targets.append(file)

	# open db connection
	client 	= pymongo.MongoClient('localhost', 27017)
	db 		= client.recallstudy
	images	= db.images

	#remove existing documents
	images.remove({})

	# calculate the number of images for each HIT
	hitSize = len(targets)/len(hitIDs);

	hitIdx 	= 0
	hitID 	= hitIDs[hitIdx]
	count 	= 0
	for i in range(len(targets)):
		count +=1
		images.insert({"hit_id": hitID, "img_url": BASE_URI+targets[i] }) # insert an image into the db with HIT ID assigned
		if count>=hitSize:
			count   = 0
			hitIdx += 1
			if hitIdx>=len(hitIDs):
				break
			hitID 	= hitIDs[hitIdx]

	# for image in images.find():
	# 	print image
	print("HIT SIZE: " + str(hitSize));
    
if __name__ == "__main__":
	create_hits(sys.argv[1])
