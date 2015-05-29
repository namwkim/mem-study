
import os, pymongo, sys, datetime, csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from collections import Counter

if __name__ == "__main__":
	# open remote database
	

	localClient = pymongo.MongoClient('localhost', 27017)
	localClient.drop_database("bubblestudy");
 	localClient.admin.command('copydb',
                         fromdb='bubblestudy',
                         todb='bubblestudy',
                         fromhost='54.69.103.85:27017')
