#########################################################################################################
#
# Author: Diego Montufar
# Date: Apr/2015
# Name: harvester_classifier.py
# Description: Performs Sentiment, geo location and gender analysis for streamed tweets as they come.
#              Logs will be written in a file for each quadrant defined in the settings i.e. log_harvester_TEST_1.txt
#
# Execution:   python harvester_classifier.py 1
# Output:      log_harvester_TEST_1.txt
#
#########################################################################################################
import json #json docs
#Twitter Streaming API connection
from tweepy.streaming import StreamListener
from tweepy import Stream, OAuthHandler
import couchdb #couchdb connection
import settings #settings defining quadrants, API keys and tokens
import emailer #emailing services
import time #record date and time
import atexit #catch termination
import random #generate random process ID
import sys #sys
from signal import signal, SIGTERM #detect termination by the system
from sys import exit
import tweet_classifier.classifier as classifier #Sentiment Classifier
from genderizer.genderizer import Genderizer #Gender classifier

proc_id = int(random.random() * 1000)
quadrant = str(sys.argv[1]) #get the quadrant argument from command line
settings.defineQuadrant(quadrant) #Assign corresponding quadrant to this process

#Streaming Listener
class listener(StreamListener):

    tweet_count = 0
    processed_tweets = 0
    ignored_tweets = 0
    
    def on_data(self, data):
        #Load Json from Twitter API
        tweet = json.loads(data)
        try:
            tweet["_id"] = str(tweet['id']) #Get the ID
            lang = tweet['lang']
            name = tweet['user']['name']

            #Gender Analysis:
            name_list = name.split()
            name = name_list[0]

            gender = Genderizer.detect(firstName = name)
            tweet['user']['gender'] = gender

            #Sentiment Analysis
            analysed_result = classifier.doSentimentAnalysis(str(tweet['text']))

            if str(lang) == 'en': #only analyse english texts
                if not hasAlreadySentiment(tweet):
                    tweet = updateSentimentDoc(tweet,analysed_result["sentiment"],analysed_result["polarity"],analysed_result["subjectivity"])
                    self.processed_tweets += 1
                else:
                    self.ignored_tweets += 1
            else: #otherwise ignore it!
                self.ignored_tweets += 1

            #Update place coordinates to work with GeoJson
            tweet = updatePlaceDoc(tweet)

            doc = db.save(tweet) #Save tweet into CouchDB
            # print("Obtained Tweet ID: " + str(tweet['id']))
            self.tweet_count += 1
            if (self.tweet_count%10000 == 0):
                #Notify when 10000 new tweets have been stored on database
                msg_update = '10K new tweets on database: ' + settings.database
                emailer.sendEmail(message=str(msg_update))
        except:
            writeLog("Twitter API error")
            pass
        return True
    
    def on_error(self, status):
        writeLog("Error during streaming"+str(status))
        sys.exit()
        
def writeLog(msg):
    file_name = "log_harvester_" + settings.location + "_" + settings.region_quadrant + ".dat"
    with open(file_name, "a") as myfile:
        myfile.write(msg + "\n")
    myfile.close()

#Verify if tweet has already sentiment analysis field
def hasAlreadySentiment(doc):
    try:
        obj = doc["sentiment_analysis"]
    except KeyError:
        return False

    return True

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

#Instance Listener object
listnerTweet = listener()

#Handler function to perform in case of program interruption
def exit_handler():
    error_msg = 'Server has interrupted harvesting process. \n'
    error_msg = error_msg + 'Process terminated at: ' + time.strftime('%c') + '\n'
    error_msg = error_msg + 'Location: ' + settings.location + ', Quadrant: ' + settings.region_quadrant + '\n'
    error_msg = error_msg + 'VM: ' + settings.vm_ip + '\n'
    error_msg = error_msg + 'Process Id: ' + str(proc_id) + '\n'
    error_msg = error_msg + 'Total tweets received: %d' % listnerTweet.tweet_count 
    writeLog(error_msg)
    emailer.sendEmail(message=str(error_msg))
    writeLog("--------------------------------------")


#Starting process
writeLog("--------------------------------------")
writeLog("Starting streaming process...")
atexit.register(exit_handler)
signal(SIGTERM, exit_handler)
#API authentication
auth = OAuthHandler(settings.consumer_key,settings.consumer_secret)
auth.set_access_token(settings.access_token,settings.access_secret)
twitterStream = Stream(auth, listnerTweet)
server = couchdb.Server(settings.server)
server.resource.credentials = (settings.admin_user, settings.admin_pass)


try:
    #Create DB if does not exist
    db = server.create(settings.database)
    writeLog("Database: " + settings.database + " doesn't exist. Proceeding with creation...")
except:
    #Just use existing DB
    db = server[settings.database]
    notice_msg = 'Server has initiated harvesting process \n'
    notice_msg = notice_msg + 'Process initiated at: ' + time.strftime('%c') + '\n'
    notice_msg = notice_msg + 'Location: ' + settings.location + ', Quadrant: ' + settings.region_quadrant + '\n'
    notice_msg = notice_msg + 'Process Id: ' + str(proc_id) + '\n'
    notice_msg = notice_msg + 'Server: ' + settings.server + '\n'
    notice_msg = notice_msg + 'Database: ' + settings.database + '\n'
    notice_msg = notice_msg + 'VM: ' + settings.vm_ip + '\n'
    writeLog(notice_msg)
    emailer.sendEmail(message=str(notice_msg))

#Streams not terminate unless the connection is closed, blocking the thread. 
#Tweepy offers a convenient async parameter on filter so the stream will run on a new thread.
twitterStream.filter(locations = settings.locations)