from boto.mturk.connection import MTurkConnection, MTurkRequestError
from boto.mturk.question import ExternalQuestion
from boto.mturk.qualification import LocaleRequirement, PercentAssignmentsApprovedRequirement, Qualifications, Requirement
import os, sys, random, time, csv, math

######  AMT CONFIGURATION PARAMETRS  ######

SANDBOX = True# Select whether to post to the sandbox (using fake money), or live MTurk site (using REAL money)
HIT_URL = "https://study.namwkim.org/retarget/annotate?url=input-gd_t1_3.txt"  # Provide the URL that you want workers to sent sent to complete you task
##TEMPORARY COMMENT: batch 10 has 40 HITS
NUMBER_OF_HITS = 1  # Number of different HITs posted for this task
# HIT_SIZE = 3 #  NUMBER OF HITS x HIT_SIZE ~ IMAGE SIZE
NUMBER_OF_ASSIGNMENTS = 10  # Number of tasks that DIFFERENT workers will be able to take for each HIT
LIFETIME = 60 * 60 * 24 * 7  # How long that the task will stay visible if not taken by a worker (in seconds)
REWARD = 0.2  # Base payment value for completing the task (in dollars)
DURATION = 60*45  # How long the worker will be able to work on a single task (in seconds)
APPROVAL_DELAY = 60*60*24*7  # How long after the task is completed will the worker be automatically paid if not manually approved (in seconds)


# HIT title (as it will appear on the public listing)
TITLE = 'Marking important regions in a graphic design'
#TODO: update time
# Description of the HIT that workers will see when deciding to accept it or not
DESCRIPTION = ("This HIT should take at most 12 minutes to complete. In this HIT, you will be presented with a series of images. You will be asked to mark the important regions in each graphic design image.")
# Search terms for the HIT posting
KEYWORDS = ['Easy', 'Mark', 'Region', 'Image', 'Graphic Design']


# Your Amazon Web Services Access Key (private)
AWS_ACCESS_KEY = ''
# Your Amazon Web Services Secret Key (private)
AWS_SECRET_KEY = ''
# Your Amazon Web Services IAM User Name (private)

#######################################

def create_blocklist(conn, qualtype, blockfile):
	if blockfile is not None:
		with open(blockfile, 'r') as f:
			reader = csv.reader(f)
			workers = []
			for row in reader:
				workers.append(row[0])
				# assign qualification for past workers to prevent from accepting this hit
				try:
					conn.assign_qualification(qualification_type_id = qualtype[0].QualificationTypeId,
						worker_id=row[0], value="50")
				except MTurkRequestError:
					print "Assign Qualification Failed - No worker found (id:"+ row[0] + ")"
			print "# of workerers participated before: ", len(workers)

def create_hits(keyfile, blockfile):

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


	# Calculate number of hits
	print "NUMBER OF HITS:", NUMBER_OF_HITS
	# Create External Question
	q = ExternalQuestion(external_url=HIT_URL, frame_height=800)
	conn = MTurkConnection(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, host=mturk_url)

	# Create a block list
	qname = "Nam Wook Kim - Qualification to Prevent Retakes ("+time.strftime("%S-%M-%H-%d-%m-%Y")+")"
	qualtype = conn.create_qualification_type(name=qname,
		description="This qualification is for people who have worked for me on this task before.",
	    status = 'Active',
	    keywords="Worked for me before",
	    auto_granted = False)
	create_blocklist(conn, qualtype, blockfile) # Assign qualifications to prevent workers from previous HITs
	# print qualtype[0]
	# Create Qualifications
	quals = Qualifications()
	# check to see if workers have the qualification only assigned for workers from previous HITs
	# print 'QualType:', qualtype[0].QualificationTypeId
	quals.add(Requirement(qualification_type_id = qualtype[0].QualificationTypeId, comparator="DoesNotExist"))
	# demographic qualifications
	# quals.add(PercentAssignmentsApprovedRequirement(comparator="GreaterThan", integer_value="95"))
	quals.add(LocaleRequirement(comparator="EqualTo", locale="US"))
	# TODO

	#Create HITs
	for i in range(0, NUMBER_OF_HITS):
		create_hit_rs = conn.create_hit(question=q, lifetime=LIFETIME, max_assignments=NUMBER_OF_ASSIGNMENTS, title=TITLE, keywords=KEYWORDS, reward=REWARD, duration=DURATION, approval_delay=APPROVAL_DELAY, description=DESCRIPTION, qualifications=quals)
		print(preview_url + create_hit_rs[0].HITTypeId)
		print("HIT ID: " + create_hit_rs[0].HITId)


if __name__ == "__main__":
	blockfile = None
	if len(sys.argv) < 3:
		print "block list is not provided"
	else:
		blockfile = sys.argv[2]
	create_hits(sys.argv[1], blockfile)
