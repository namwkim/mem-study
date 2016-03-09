import ijson,sys,os,csv, datetime

NUM_IMAGES = 51
# read 51 images for BubbleView
targets = []
for root, dirs, files in os.walk("./images/targets"):
    for file in files:
        if file.startswith('.'):
            continue
        targets.append(file)

# find the annotations for the images
imgIds = []
imgNames = {}
f = open(sys.argv[1], 'r')
i = 0
for img in ijson.items(f, "images.item"):
    if img['file_name'] in targets:
        imgIds.append(img['id'])
        imgNames[img['id']] = img['file_name']
        i+=1
        print img['id'], i
        if i==NUM_IMAGES:
            break
f.close()
print imgIds
print "extracting fixations"
csvwriter = csv.writer(open(sys.argv[2], 'wb'))
fixations = []
f = open(sys.argv[1], 'r')
for ann in ijson.items(f, "annotations.item"):
    if ann["image_id"] in imgIds:
        workderID   = ann["worker_id"]
        imgName     = imgNames[ann["image_id"]]
        print imgName, workderID
        for coord in ann["fixations"]:
            curTime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            csvwriter.writerow([curTime, imgName, workderID, coord[0], coord[1]])

print 'saving fixations into a csv file'
