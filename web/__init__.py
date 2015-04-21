################################################################################
#
# Author: Diego Montufar
# Date: Apr/2015
# Name: __init__.py
# Description:  Here we define the available web services which can be accessed by
#				following the app.route path as URL.
# Dependencies: Flask, indexer
#
################################################################################

from flask import Flask , render_template
from services import indexer
import os
# __file__ refers to the file settings.py 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')
APP_STATIC_JSON = os.path.join(APP_STATIC, 'json')

app = Flask(__name__)

#Service: Main web page index.html is called
#Parameters: none
#Parameters: index.html
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

#Service: perform custom searches based on elasticsearch queries in json format
#Parameters: <jsonQuery> is a json object which must follow the elasticsearch query structure
#return: a json object containing the matched results
@app.route('/customSearch/<jsonQuery>')
def getCustomSearch(jsonQuery):
	doc_type = 'tweet'
	return indexer.customSearch(jsonQuery,doc_type)

#Service: 
#Parameters: 
#return: 
@app.route('/customGeoSearch/<term>/<suburb>')
def getCustomGeoSearch(term,suburb):
	doc_type = 'tweet'
	return indexer.getTweetsBySuburb(term,suburb,doc_type)

#Service: return a json 
#Parameters: <jsonQuery> is a json object which must follow the elasticsearch query structure
#return: a json object containing the matched results
@app.route('/sentimentTotals/<jsonQuery>')
def getSentimentTotals(jsonQuery):
	doc_type = 'tweet'
	return indexer.statisticsByTerm(jsonQuery,doc_type)

#Service: Get a list of the suburbs of main cities of AU: ABS 2011
#Parameters: none
#return: a json object containing a list of suburbs
@app.route('/listSuburbs')
def listSuburbsAU():
	return open(APP_STATIC_JSON+"/suburbs.json", 'r').read()

#Service: Get GeoJson File containing information relatd to countries of birth by suburb of AU
#Parameters: <state> the code of the state: i.e: VIC, TAS, etc
#return: GeoJson object
@app.route('/culturesByCity/<state>')
def listCulturesByCityAU(state):
	return indexer.getCultures(state)

#main
if __name__ == "__main__":
	app.run(debug=True)