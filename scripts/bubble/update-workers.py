import csv,sys

with open(sys.argv[2], 'wb') as f:
    csvwriter = csv.writer(f);
    with open(sys.argv[1], 'rb') as f:
        csvreader = csv.reader(f);
        header = next(csvreader);
        csvwriter.writerow(header)
        indices = []
        for i in xrange(0,len(header)):
            col = header[i]
            if "UPDATE-Nam Wook Kim" in col:
                print col
                indices.append(i)
        # find indices
        print indices
        for row in csvreader:
            for i in indices:
                row[i]="Revoke"
            csvwriter.writerow(row)
