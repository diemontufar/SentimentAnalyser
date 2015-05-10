#########################################################################################################
#
# Author: 		Diego Montufar
# Date: 		Apr/2015
# Name: 		settings.py
# Description: 	Performs Sentiment, geo location and gender analysis for streamed tweets as they come.
#              	Logs will be written in a file for each quadrant defined in the settings i.e. log_harvester_TEST_1.txt
#
# Execution:   	python harvester_classifier.py 1
# Output:      	log_harvester_TEST_1.txt
#
#########################################################################################################

#Email default configurations:
smtp_server = 'smtp.gmail.com'
from_address = 'foo@gmail.com'
to_address = 'bar@gmail.com'
from_password = 'bar_pass'
def_subject = 'Harvesting process status update'
smtp_port = 587

#Local CouchDB 
server = 'http://localhost:5984/'
vm_ip = 'node1:localhost' #just a description to be included on emails
database = '' #initialize empty
location = '' #initialize empty
admin_user = '<user>' #Futon admin username
admin_pass = '<pass>' #Futon admin pass

#Initialize variables for each quadrant
consumer_key = '' #initialize empty
consumer_secret = '' #initialize empty
access_token = '' #initialize empty
access_secret = '' #initialize empty
region_quadrant = '' #initialize empty
#Bounding Box:
locations = [] #initialize empty

#Define Quadrant initialization:
# Description: 	This method will be called from the harvester_classifier.py in order to assign quadrants
# 				and its corresponding authorization keys for the streaming API.
#				Defining more than one quadrant should be specified exactly the same as the example 
#				given below, but considering separated if statements and each of them with different Authorization keys.
#				Each quadrant (if more than one) must be executed independently (i.e. N background processes)
# Diclaimer:	Try not to use the same credentials more than 1 or 2 times since you may have problems
#				during the streaming due to limits imposed by the Twitter API itself.
# Disclaimer 2:	API credentials provided here are just an example. None of them will work at all.
#
def defineQuadrant(quadrant):

	global consumer_key
	global consumer_secret
	global access_token
	global access_secret
	#Bounding Box:
	global locations
	global location
	global database
	global region_quadrant

#Node 1 configuration: Test
#Test:
	if quadrant == '1': #method parameter
		database = 'test' #name of the couchdb where you want to store tweets
		location = 'TEST' #description to be included on emailing services
		region_quadrant = '1' #description to be included on emailing services, may be the same as the value of quadrant
		consumer_key = '1rryuUcww935qsmu7fkk2Taena' #Twitter API credentias (example)
		consumer_secret = 'mcii2QVvbbJMh7D0omT9auWhiJUpM3qhHt21lUck9UptoDv6yXb' #Twitter API credentias (example)
		access_token = '3184636436-qUAD1TcPYENWl3MnxyuqA7tq4RqVcoRzoF891cMc' #Twitter API credentias (example)
		access_secret = 'Et3exDs83RpjEKw6HNfGSfEKQNcolUZJVoMGAjmNEpQmdd' #Twitter API credentias (example)
		#Bounding Box:
		locations = [145.0544,-39.1549,148.2020,-35.7746] #Define a bounding box where the tweets should come from
