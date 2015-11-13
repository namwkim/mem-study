
import os, pymongo, sys, datetime, csv

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "provide a filename to save worker ids"
        sys.exit(0)
    # open remote database
    client 	= pymongo.MongoClient('54.69.103.85', 27017)
    db 		= client.bubblestudy
    logs = db.logs24_Nov.find({})
    print logs.count()

    workers = dict()
    with open(sys.argv[1], 'wb') as f:
        writer = csv.writer(f)
        for log in logs:
            if workers.has_key(log["worker_id"]):
                continue
            workers[log["worker_id"]] = log["worker_id"]
            print workers[log["worker_id"]]
            writer.writerow([log["worker_id"]])
    print "extractioin finished!"
