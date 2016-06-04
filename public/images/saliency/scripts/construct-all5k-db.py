import os, pymongo, sys, random, time, csv

if __name__ == "__main__":
    client  = pymongo.MongoClient('localhost', 27017)
    db = client.saliency
    imgCol = db.images
    imgCol.remove({})

    source_dir = "../../all5k";
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.startswith('.'):
                continue

            result = imgCol.insert_one({'filename':file})
            print file, "'s id:", result.inserted_id
