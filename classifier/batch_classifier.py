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

sys.path.insert(0,settings.working_directory)
sys.path.append(settings.tweet_classifier_module)

import couchdb #couchdb heper
import json #json documents management

import tweet_classifier.classifier as classifier #classifier helper


#Get the document from couchdb by ID
def getDocument(id):
	doc = db.get(id)
	return doc

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
def updateDoc(doc,sentiment,polarity,subjectivity):
	doc["sentiment_analysis"] = json.loads('{"sentiment": "%s","polarity": %.2f,"subjectivity": %.2f}' % (sentiment,polarity,subjectivity))
	doc = db.save(doc)
	# print(str(doc[0]) + ";" + str(doc[1]))
	# print("Document updated")

server = couchdb.Server(settings.server)
server.resource.credentials = (settings.admin_user, settings.admin_pass)

############PERFORM SENTIMENT ANALYSIS IN BULK MODE########################
try:
	#Just use existing DB
	db = server[settings.database]
except:
	print("Error while accessing couchdb data base!");

i=0
for id in db:
	doc = getDocument(id)
	tweet = retrieveDocText(doc)
	lang = retrieveLang(doc)
	analysed_result = classifier.doSentimentAnalysis(tweet)

	if lang == 'en': #only analyse english texts
		# print("ID: " + id + ", Tweet: " + tweet + " -> " + sentiment) #Original tweet
		if not hasAlreadySentiment(doc):
			updateDoc(doc,analysed_result["sentiment"],analysed_result["polarity"],analysed_result["subjectivity"])
			print("ID: " + id + ", Tweet: " + analysed_result["text"] + " -> " + analysed_result["sentiment"] + ", polarity: " + str(analysed_result["polarity"]) + ", subjectivity: " + str(analysed_result["subjectivity"])) #parsed tweet
	else: #otherwise ignore it!
		print("ID: " + id + ", Tweet: " + " -> " + "ignored!")