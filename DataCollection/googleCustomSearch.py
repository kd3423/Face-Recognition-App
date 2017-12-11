import json
import time

from googleapiclient.discovery import build
import pymongo
from pymongo import MongoClient
connection = MongoClient()
db = connection['PrecogTaskB']
def getService():
    service = build("customsearch", "v1",
            developerKey="AIzaSyDMGZ2AQA0cOvnt5g0-h-L6zv064fu-NyU")

    return service

def main():
	count = 0
	pageLimit = 40
	try:
		service = getService()
		startIndex = 1
		response = []

		for nPage in range(0, pageLimit):
		    print("Reading page number:",nPage+1)

		    response.append(service.cse().list(
		        q='narendra modi', #Search words
		        cx='004360402827201415602:toibiuh8tvm',  #CSE Key
		        lr='lang_en', #Search language
		        start=startIndex
		    ).execute())

		    startIndex = response[nPage].get("queries").get("nextPage")[0].get("startIndex")
		    # time.sleep(2) 
	except:
		print('Cannot get more Data!!!')
	
	for j in response:
		for k in j['items']:
			try:
				check = 0
				find_result = db['NarendraModi'].find({"cacheId" : str(k['cacheId'])})
				for j in find_result:
					if j['cacheId'] == k['cacheId']:
						print("present")
						check = 1
					# else:
					# 	print("added to database")
					# 	db[tagName].insert(i)
				if check == 0:
					db['NarendraModi'].insert(k)
					print("added")
					count+=1
					print(count)
			except:
				print('Cannot write to mongo')
				# print(k)
main()