################################################################################
#
# Author: Diego Montufar
# Date: Apr/2015
# Name: batch_settings.py
# Description: Here you define settings and parameters needed for the batch.py module.
#				configuration (cfg) files are required and must be defined.
#
################################################################################

import os
# import ConfigParser

#Here we are defining the config file parsers
APP_ROOT 			= os.path.dirname(os.path.abspath('.')) # refers to application_top
SERVER_CONFIG 		= APP_ROOT + '/server_configurations.cfg' 
DIRECTORY_CONFIG 	= APP_ROOT + '/directory_configurations.cfg' 
SECURITY_CONFIG 	= APP_ROOT + '/security_configurations.cfg' 

# serverParser = ConfigParser.RawConfigParser()   
# serverParser.read(SERVER_CONFIG)
# directoryParser = ConfigParser.RawConfigParser()   
# directoryParser.read(DIRECTORY_CONFIG)
# securityParser = ConfigParser.RawConfigParser()   
# securityParser.read(SECURITY_CONFIG)


########################## APP CONFIGURATIONS ###################################
#Local CouchDB 
server = 'http://localhost:5984/'
database = 'twitterall_2'
admin_user = 'diogonal'
admin_pass = 'dgl0588'

#Directories
working_directory = "/Library/WebServer/Documents/SentimentAnalyser/classifier"
tweet_classifier_module = "/Library/WebServer/Documents/SentimentAnalyser/classifier/tweet_classifier"
indexer_module = "/Library/WebServer/Documents/SentimentAnalyser/indexer/"
create_index_script = "configure_index.sh"

# print(serverParser.get('local_couchdb_server'))