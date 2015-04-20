################################################################################
#
# Author: Diego Montufar
# Date: Apr/2015
# Name: batch_classifier.py
# Description: Performs Sentiment analysis in all documents from a database
#			   defined in the batch_settings.py file. If a document has already
#              sentiment_analysis defined on its structure, pass.
#
################################################################################

import batch_settings as settings #Custom Settings
import sys
import os
import subprocess

sys.path.insert(0,settings.working_directory)
sys.path.append(settings.tweet_classifier_module)

INDEXER_DIR = os.path.dirname(settings.indexer_module)
INDEX_SCRIPT = os.path.join(INDEXER_DIR, settings.create_index_script)
LOG_FILE = 'log.txt'

import couchdb #couchdb heper
import json #json documents management
import time #record elapsed time

import tweet_classifier.classifier as classifier #classifier helper


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

############PERFORM SENTIMENT ANALYSIS IN BULK MODE########################
os.remove(LOG_FILE) if os.path.exists(LOG_FILE) else None
processed_tweets = 0
ignored_tweets = 0
initial = time.time()
writeLog("Batch Process initiated at: " + str(time.strftime("%c")))
success = False

try:
	#Just use existing DB
	db = server[settings.database]
	success = True
except:
	writeLog("Error while accessing couchdb database!")

for id in db:
	doc = getDocument(id)
	tweet = retrieveDocText(doc)
	lang = retrieveLang(doc)
	analysed_result = classifier.doSentimentAnalysis(tweet)

	if lang == 'en': #only analyse english texts
		# print("ID: " + id + ", Tweet: " + tweet + " -> " + sentiment) #Original tweet
		if not hasAlreadySentiment(doc):
			doc = updateSentimentDoc(doc,analysed_result["sentiment"],analysed_result["polarity"],analysed_result["subjectivity"])
			processed_tweets += 1
			# print("Processed")
			# print("ID: " + id + ", Tweet: " + analysed_result["text"] + " -> " + analysed_result["sentiment"] + ", polarity: " + str(analysed_result["polarity"]) + ", subjectivity: " + str(analysed_result["subjectivity"])) #parsed tweet
		else:
			ignored_tweets += 1
	else: #otherwise ignore it!
		ignored_tweets += 1
		# print("Ignored")
	doc = updatePlaceDoc(doc)
	doc = db.save(doc)

#End execution, print statistics:
if success:
	elapsed_time = time.time() - initial
	writeLog("Processed Tweets: " + str(processed_tweets + ignored_tweets))
	writeLog("Analysed Tweets: " + str(processed_tweets))
	writeLog("Ignored Tweets: " + str(ignored_tweets))
	writeLog("__________________________________________________")
	writeLog("Starting indexing Batch process at: " + str(time.strftime("%c")))
	#Execute batch indexing process
	result = subprocess.check_output([INDEX_SCRIPT])
	writeLog(str(result))
	writeLog("done!")
	#Finalizing indexing
	str_end = "Execution time: %0.2f min." % (elapsed_time/60)
	writeLog(str_end)
	writeLog("Batch Process finished at: " + str(time.strftime("%c")))
else:
	writeLog("Batch process terminated with an error!")
