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
@app.route('/customGeoSearch/<term>/<suburbCode>/<startP>/<sizeP>')
def getCustomGeoSearch(term,suburbCode,startP,sizeP):
	doc_type = 'tweet'
	return indexer.getTweetsBySuburb(term,suburbCode,startP,sizeP,doc_type)

#Service: return a json 
#Parameters: <jsonQuery> is a json object which must follow the elasticsearch query structure
#return: a json object containing the matched results
@app.route('/sentimentTotals/<term>/<suburbCode>')
def getSentimentTotals(term,suburbCode):
	doc_type = 'tweet'
	return indexer.statisticsByTerm(term,suburbCode,doc_type)

#Service: Get a list of the suburbs of main cities of AU: ABS 2011
#Parameters: none
#return: a json object containing a list of suburbs
@app.route('/listSuburbs/<countryCode>')
def listSuburbsAU(countryCode):
	return indexer.getSuburbs(countryCode)


#Service: Get GeoJson File containing information relatd to countries of birth by suburb of AU
#Parameters: <state> the code of the state: i.e: VIC, TAS, etc
#return: GeoJson object
@app.route('/culturesByCity/<stateCode>')
def listCulturesByCityAU(stateCode):
	return indexer.getCultures(stateCode)

#Service: 
#Parameters: 
#return: 
@app.route('/languagesByCountry/<countryCode>')
def listLanguagesByCountry(countryCode):
	return indexer.getLanguages(countryCode)


@app.route('/tweetsByCountryOfBirth/<term>/<stateCode>/<suburbCode>')
def getTweetsByCountryOfBirth(term,stateCode,suburbCode):
	return indexer.getTweetsByCountryOfBirth(term,stateCode,suburbCode)


@app.route('/customAggregation/<jsonQuery>')
def getCustomAgg(jsonQuery):
	doc_type = 'tweet'
	return indexer.getCustomAgg(doc_type,jsonQuery)


#Good!
@app.route('/topListBySuburb/<term>/<suburbCode>/<field>/<size>')
def getTopList(term,suburbCode,field,size):
	doc_type = 'tweet'
	return indexer.getTopListBySuburb(doc_type,term,suburbCode,field,size)




#main
if __name__ == "__main__":
	app.run(debug=True)