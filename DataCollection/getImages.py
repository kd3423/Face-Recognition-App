# https://www.instagram.com/explore/tags/<TagName>/?__a=1
import requests as re
import pymongo
from pymongo import MongoClient
import random
import numpy as np
# from instagram.client import InstagramAPI
import json 
connection = MongoClient()

db = connection['PrecogTaskB']
data = db['ArvindKejriwal'].find()
flist = []
for post in data:
	try:
		flist.append(post['cacheId'])
		# print(post['pagemap']['cse_image'][0]['src'])
		f = open(str('./PrecogTaskB/'+post['cacheId'])+'.jpg','wb')
		f.write(re.get(post['pagemap']['cse_image'][0]['src']).content)
		f.close()
		print(str(post['cacheId'])+' Done')
	except:
		print('No image found!!!')