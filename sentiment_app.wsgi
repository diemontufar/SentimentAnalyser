#!/usr/bin/python

import sys
import logging

logging.basicConfig(stream=sys.stderr)

sys.path.insert(0,"/Library/WebServer/Documents/SentimentAnalyser/")
sys.path.append('/Library/WebServer/Documents/SentimentAnalyser/web')
sys.path.append('/Library/WebServer/Documents/SentimentAnalyser/web/static/json/') #This wont be necessary 
sys.path.append('/Library/WebServer/Documents/SentimentAnalyser/web/services/')

from web import app as application
application.secret_key = 'lksafjhASAhjSfjsf'