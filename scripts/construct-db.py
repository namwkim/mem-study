import os, pymongo
for root, dirs, files in os.walk("../public/images/db/"):
	client 	= pymongo.MongoClient('localhost', 27017)
	db 		= client.mem_study
	images	= db.images
	#remove existing documents
	images.remove({})

	#create a new image database
	new_images = []
	for file in files:		
		if file.startswith('.'):
			continue
		new_images.append({'url':file})
	images.insert(new_images)
	for image in images.find():
		print image
