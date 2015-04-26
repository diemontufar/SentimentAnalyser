################################################################################
#
# Author: Diego Montufar
# Date: Apr/2015
# Name: batch_classifier.py
# Description: Performs Sentiment, geo location and gender analysis in all documents from a database
#			   defined in the batch_settings.py file. If a document has already
#              one of the mentioned fields defined on its structure, it will be ignored.
#			   Log will be written in a file i.e. log_dbname.txt
#
# Execution:   python batch_classifier.py test
# Output:      log_test.txt
#
################################################################################

import batch_settings as settings #Custom Settings
import sys #system library
import os #dealing with files
import couchdb #couchdb connection to databases
import json #json documents management
import time #record elapsed time

import tweet_classifier.classifier as classifier #Sentiment classifier
from genderizer.genderizer import Genderizer #Gender classifier

#You need to provide an argument which is the name of the database
database_arg = str(sys.argv[1]) 
LOG_FILE = 'log_' + database_arg + '.txt'


#Get the document from couchdb by ID
def getDocument(id):
	doc = db.get(id)
	return doc

#Verify if tweet has already sentiment analysis field
def hasAlreadySentiment(doc):
	try:
		obj = doc["sentiment_analysis"]
	except KeyError:
		return False

	return True

#Verify if tweet has already gender field
def hasAlreadyGender(doc):
	try:
		obj = doc["user"]["gender"]
	except KeyError:
		return False

	return True

#Get the document's text field
def retrieveDocText(doc):
	text = doc['text'] #Get the text of the tweet
	return text

#Get the document's language
def retrieveLang(doc):
	lang = doc['lang'] #Get the text of the tweet
	return lang

#Update Document with new fields (sentiment results)
def updateSentimentDoc(doc,sentiment,polarity,subjectivity):
	doc["sentiment_analysis"] = json.loads('{"sentiment": "%s","polarity": %.2f,"subjectivity": %.2f}' % (sentiment,polarity,subjectivity))
	return doc

#Update the Palce field of the tweet when it is populated in order to follow GeoJson format for polygons
def updatePlaceDoc(doc):
	if doc["place"] is not None:
		place_coordinates = doc["place"]["bounding_box"]["coordinates"][0]
		tmp_coordinates = []
		if place_coordinates[0] != place_coordinates[1]:
			tmp_coordinates.insert(0,place_coordinates[0])
			tmp_coordinates.insert(1,place_coordinates[1])
			tmp_coordinates.insert(2,place_coordinates[2])
			tmp_coordinates.insert(3,place_coordinates[3])
			tmp_coordinates.insert(4,place_coordinates[0])
			doc["place"]["bounding_box"]["coordinates"][0] = tmp_coordinates
		else:
			doc["place"]["bounding_box"] = None
	return doc

#Write line in log file
def writeLog(line):
	results_file = open(LOG_FILE, 'a')
	results_file.write(line+'\n')
	results_file.close()

#Create connection with couchdb database
server = couchdb.Server(settings.server)
server.resource.credentials = (settings.admin_user, settings.admin_pass)

############PERFORM TWEET ANALYSIS IN BULK MODE########################
os.remove(LOG_FILE) if os.path.exists(LOG_FILE) else None
processed_tweets = 0
ignored_tweets = 0
initial = time.time()
writeLog("Batch Process initiated at: " + str(time.strftime("%c")))
success = False

try:
	#Just use existing DB
	db = server[database_arg]
	success = True
except:
	writeLog("Error while accessing couchdb database!")

for id in db:
	doc = getDocument(id)
	tweet = retrieveDocText(doc)
	lang = retrieveLang(doc)
	analysed_result = classifier.doSentimentAnalysis(tweet)

	if lang == 'en': #only analyse english texts
		if not hasAlreadySentiment(doc):
			doc = updateSentimentDoc(doc,analysed_result["sentiment"],analysed_result["polarity"],analysed_result["subjectivity"])
			processed_tweets += 1
		else:
			ignored_tweets += 1
	else: #otherwise ignore it!
		ignored_tweets += 1

	#Update place bounding box
	doc = updatePlaceDoc(doc)

	#Update gender:
	if not hasAlreadyGender(doc):
		name = doc['user']['name']
		name_list = name.split()

		if name_list is not None and len(name_list)>=1:
			name = name_list[0]
			gender = Genderizer.detect(firstName = name)
			doc['user']['gender'] = gender
		else:
			doc['user']['gender'] = None

	doc = db.save(doc)

#End execution, print statistics and elapsed time:
if success:
	elapsed_time = time.time() - initial
	writeLog("Batch process for database: " + database_arg)
	writeLog("Processed Tweets: " + str(processed_tweets + ignored_tweets))
	writeLog("Analysed Tweets: " + str(processed_tweets))
	writeLog("Ignored Tweets: " + str(ignored_tweets))
	writeLog("___________Starting to compact database_____________")
	initiated = db.compact()
	writeLog("Compaction succeeded: " + str(initiated))
	writeLog("done!")
	str_end = "Execution time: %0.2f min." % (elapsed_time/60)
	writeLog(str_end)
	writeLog("Batch Process finished at: " + str(time.strftime("%c")))
else:
	writeLog("Batch process terminated with an error!")
