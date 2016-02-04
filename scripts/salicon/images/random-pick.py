import os, pymongo, sys, random, time, csv, shutil

def random_sampling():
	# collect test candidate images
	allImages = []
	src_dir = "./train"
	for root, dirs, files in os.walk(src_dir):
		for file in files:
			if file.startswith('.'):
				continue
			if file.endswith('.jpg')==False:
				continue
			allImages.append(file)

	#create folder if not exists
	des_dir = "./targets"
	if not os.path.exists(des_dir):
		os.makedirs(des_dir)

	#clear folder if exists
	for root, dirs, files in os.walk(des_dir):
		for file in files:
			os.remove(des_dir+"/"+file)

	#randomly copy 50 images from the source folder
	picked = random.sample(allImages, 51)
	print "51 images selected:"
	for file in picked:
		shutil.copyfile(src_dir+"/"+file, des_dir+"/"+file)
		print "src", src_dir+"/"+file
		print "dst", des_dir+"/"+file

if __name__ == "__main__":
	random_sampling()
