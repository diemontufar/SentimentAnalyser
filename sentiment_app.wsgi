#!/usr/bin/python

import sys
import logging

logging.basicConfig(stream=sys.stderr)

sys.path.insert(0,"/Library/WebServer/Documents/SentimentAnalyser/")
sys.path.append('/Library/WebServer/Documents/SentimentAnalyser/web')

from web import app as application
application.secret_key = 'lksafjhASAhjSfjsf'