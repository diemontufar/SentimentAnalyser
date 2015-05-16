#!/usr/bin/python

################################################################################
#
# Author: 		Diego Montufar
# Date: 		Apr/2015
# Name: 		sentiment_app.wsgi
# Description:  WSGI is the Web Server Gateway Interface. It is a specification that describes 
#			    how a web server communicates with web applications, and how web applications 
#			    can be chained together to process one request. 
#			    WSGI is a Python standard described in detail in PEP 3333
# Dependencies: None
#
################################################################################


import sys
import logging

#Enable error messages on the server (for debugging)
logging.basicConfig(stream=sys.stderr)

#We need to define where is located our web module
sys.path.insert(0,"/var/www/html/SentimentAnalyser/")
sys.path.append('/var/www/html/SentimentAnalyser/web')
sys.path.append('/var/www/html/SentimentAnalyser/web/services/')

#Import web module
from web import app as application
application.secret_key = 'lksafjhASAhjSfjsf' #use a random secret key


