#########################################################################################################
#
# Author:       Diego Montufar
# Date:         Apr/2015
# Name:         indexer_settings.py
# Description:  Define server URLs, databases and elasticsearch index. This file is called from inside the indexer module.
#
#########################################################################################################

#Elasticsearch index:
es_index = 'twitterall'
es_docType = 'tweet'

#Couchdb Database and credentials
server = 'http://localhost:5984/'
cultures_database = 'cultures'
languages_database = 'languages'
suburbs_database = 'suburbs'
