from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.qualification import LocaleRequirement, PercentAssignmentsApprovedRequirement, Qualifications
import os, pymongo, sys, random, csv, itertools

######  AMT CONFIGURATION PARAMETRS  ######

SANDBOX = True  # Select whether to post to the sandbox (using fake money), or live MTurk site (using REAL money)
HIT_URL = "https://study.namwkim.org/socialdoi"  # Provide the URL that you want workers to sent sent to complete you task

NUMBER_OF_HITS = 1  # Number of different HITs posted for this task
NUMBER_OF_ASSIGNMENTS = 3  # Number of tasks that DIFFERENT workers will be able to take for each HIT
LIFETIME = 60 * 60 * 24 * 7  # How long that the task will stay visible if not taken by a worker (in seconds)
REWARD = 1.0  # Base payment value for completing the task (in dollars)
DURATION = 60*45  # How long the worker will be able to work on a single task (in seconds)
APPROVAL_DELAY = 60*60*24*1  # How long after the task is completed will the worker be automatically paid if not manually approved (in seconds)


# HIT title (as it will appear on the public listing)
TITLE = 'Budget Challenge'
# Description of the HIT that workers will see when deciding to accept it or not
DESCRIPTION = ("In this HIT you will be presented with a tree visualization of a government budget, and asked to find at least five most interesting budget programs. This HIT should take about 15 minutes to complete.")
# Search terms for the HIT posting
KEYWORDS = ['Easy', 'Budget', 'Visualization', 'Find', 'Programs', 'Interest']


# Your Amazon Web Services Access Key (private)
AWS_ACCESS_KEY = ''
# Your Amazon Web Services Secret Key (private)
AWS_SECRET_KEY = ''
# Your Amazon Web Services IAM User Name (private)

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

	# Create External Question
	q = ExternalQuestion(external_url=HIT_URL, frame_height=800)
	conn = MTurkConnection(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, host=mturk_url)

	# Create Qualifications
	quals = Qualifications()
	quals.add(PercentAssignmentsApprovedRequirement(comparator="GreaterThan", integer_value="95"))
	quals.add(LocaleRequirement(comparator="EqualTo", locale="US"))

	#Create HITs
	hitIDs = []
	for i in range(0, NUMBER_OF_HITS):
		create_hit_rs = conn.create_hit(question=q, lifetime=LIFETIME, max_assignments=NUMBER_OF_ASSIGNMENTS, title=TITLE, keywords=KEYWORDS, reward=REWARD, duration=DURATION, approval_delay=APPROVAL_DELAY, description=DESCRIPTION, qualifications=quals)
		print(preview_url + create_hit_rs[0].HITTypeId)
		print("HIT ID: " + create_hit_rs[0].HITId)

		# save HIT IDs
		hitIDs.append(create_hit_rs[0].HITId); 

	# open db connection
	client 	= pymongo.MongoClient('localhost', 27017)
	db 		= client.socialdoi
	db.budgets.remove({})

	budgets = {}
	with open('operating-budget.csv', 'r') as csvfile:
	    reader = csv.reader(csvfile)

	    reader.next()

	    for row in reader:
	    	key = row[0]+"/"+row[1]+"/"+row[2]+"/"+row[3]
	    	if budgets.has_key(key)==False:
	    		print row[3]
	    		budgets[key] = {
		    		"fiscalyear": row[0],
		     		"cabinet": row[1],
		     		"department": row[2],
		     		"program": row[3],
		     		# "expense_type": row[4],
		     		# "expense_category": row[5],
		     		"recommended": 0,
		     		"approved": 0,
		     		# "account_name": row[8],
		     		"fund": row[9],
		     		"fundtype": row[10],
		     		# "program_number": row[11],
		     		# "account_number": row[12]

		    		}
    		budgets[key]["recommended"] += int(float(row[6][1:]))
    		budgets[key]["approved"] += int(float(row[7][1:]))
	    	
	    	# print row[3]

	    	# if budgets.has_key(row[3])==False:
	    	# 	budgets[""]
	   
	    	# print record
	i = 0
	for k in budgets:
		if (budgets[k]["cabinet"]!="Education" and budgets[k]["approved"]>10000) or (budgets[k]["cabinet"]=="Education" and budgets[k]["approved"]>5000000):
			i+=1
			db.budgets.insert(budgets[k])
	print("# OF BUDGET PROGRAMS: " + str(i));
    
if __name__ == "__main__":
	create_hits(sys.argv[1])

