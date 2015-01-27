from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.qualification import LocaleRequirement, PercentAssignmentsApprovedRequirement, Qualifications
import os, pymongo, sys, itertools

######  AMT CONFIGURATION PARAMETRS  ######

SANDBOX = True  # Select whether to post to the sandbox (using fake money), or live MTurk site (using REAL money)
HIT_URL = "https://study.namwkim.org/recall"  # Provide the URL that you want workers to sent sent to complete you task

NUMBER_OF_HITS = 37  # Number of different HITs posted for this task
NUMBER_OF_ASSIGNMENTS = 9  # Number of tasks that DIFFERENT workers will be able to take for each HIT
LIFETIME = 60 * 60 * 24 * 7  # How long that the task will stay visible if not taken by a worker (in seconds)
REWARD = 0.5  # Base payment value for completing the task (in dollars)
DURATION = 60*20  # How long the worker will be able to work on a single task (in seconds)
APPROVAL_DELAY = 60*60*24*7  # How long after the task is completed will the worker be automatically paid if not manually approved (in seconds)


# HIT title (as it will appear on the public listing)
TITLE = 'Visualization Recall Study'
# Description of the HIT that workers will see when deciding to accept it or not
DESCRIPTION = 'Describe a visualization image!'
# Search terms for the HIT posting
KEYWORDS = ['Image', 'Visualization', 'Describe']


# Your Amazon Web Services Access Key (private)
AWS_ACCESS_KEY = ''
# Your Amazon Web Services Secret Key (private)
AWS_SECRET_KEY = ''
# Your Amazon Web Services IAM User Name (private)

######  CONFIGURATION PARAMETRS  ######
BASE_URI = "/images/recall-db/Group"
ST_BASE = ".png"
ST_PARAGRAPH = "-paragraph.png"
ST_TITLE = "-title.png"
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


	# collect target image filenames
	targets = []
	for root, dirs, files in os.walk("../public/images/recall-db/"):		
		if len(dirs)==0: # loop over sub-directories
			# create an instance

			#cleanup
			for file in files:
				if file.startswith('.'):# skip hidden  or _DS_Store
					continue
				splited = file.split(".")
				
				if len(splited)>2: #png.jpg, png.gif to png
					print 'strange filename found: ', file 
					# os.rename(os.path.join(root, file), os.path.join(root, splited[0]+"."+splited[1]))
			

			filtered = itertools.ifilter(lambda x: x.endswith("png"), files)
			filtered = itertools.imap(lambda x: x.strip('.png'), filtered)

			names = []
			for key, group in itertools.groupby(filtered, lambda x: x.split('-')[0]):
				#groups.append(sorted(group))
				names.append(key)
			instances = []
			instances = instances + [[names[0] + ST_BASE, 		names[1] + ST_PARAGRAPH, 	names[2] + ST_TITLE]]
			instances = instances + [[names[2] + ST_TITLE, 		names[0] + ST_BASE, 		names[1] + ST_PARAGRAPH]]
			instances = instances + [[names[1] + ST_PARAGRAPH, 	names[2] + ST_TITLE, 		names[0] + ST_BASE]]

			instances = instances + [[names[2] + ST_BASE, 		names[0] + ST_PARAGRAPH, 	names[1] + ST_TITLE]]
			instances = instances + [[names[1] + ST_TITLE, 		names[2] + ST_BASE, 		names[0] + ST_PARAGRAPH]]
			instances = instances + [[names[0] + ST_PARAGRAPH, 	names[1] + ST_TITLE, 		names[2] + ST_BASE]]

			instances = instances + [[names[1] + ST_BASE, 		names[2] + ST_PARAGRAPH, 	names[0] + ST_TITLE]]
			instances = instances + [[names[0] + ST_TITLE, 		names[1] + ST_BASE, 		names[2] + ST_PARAGRAPH]]
			instances = instances + [[names[2] + ST_PARAGRAPH, 	names[0] + ST_TITLE, 		names[1] + ST_BASE]]
			targets.append(instances)

	

	q = ExternalQuestion(external_url=HIT_URL, frame_height=800)
	conn = MTurkConnection(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, host=mturk_url)

	# Create Qualifications
	quals = Qualifications()
	quals.add(PercentAssignmentsApprovedRequirement(comparator="GreaterThan", integer_value="95"))
	quals.add(LocaleRequirement(comparator="EqualTo", locale="US"))
		
	hitIDs = []
	for i in range(0, NUMBER_OF_HITS):
		create_hit_rs = conn.create_hit(question=q, lifetime=LIFETIME, max_assignments=NUMBER_OF_ASSIGNMENTS, title=TITLE, keywords=KEYWORDS, reward=REWARD, duration=DURATION, approval_delay=APPROVAL_DELAY, annotation=DESCRIPTION, qualifications=quals)
		print(preview_url + create_hit_rs[0].HITTypeId)
		print("HIT ID: " + create_hit_rs[0].HITId)

		# save HIT IDs
		hitIDs.append(create_hit_rs[0].HITId); 


	# open db connection
	client 	= pymongo.MongoClient('localhost', 27017)
	db 		= client.recallstudy
	images	= db.images
	progress= db.progress
	#remove existing documents
	images.remove({})
	progress.remove({})

	# calculate the number of images for each HIT
	for i in range(0, NUMBER_OF_HITS):
		
		hitID = hitIDs[i]
		#print "HIT ID : ", hitID
		instances = targets[i]
		for j in range(len(instances)):
			print "Group: ", i+1, " Instance: ", j+1
			progress.insert({"group": i+1, "instance" : j+1, "count" : 0 })
			assignment = {"hit_id": hitID, "group": i+1, "instance" : (j+1), "img_urls": [] }
			for filename in instances[j]:
				if j<10:
					assignment["img_urls"].append( (BASE_URI+'0'+str(i+1)+"/"+filename) )
				else:
					assignment["img_urls"].append( (BASE_URI+str(i+1)+"/"+filename) )					
			images.insert(assignment)
   	 
if __name__ == "__main__":
	create_hits(sys.argv[1])
