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

#Service: 		Main web page index.html is called
#Description:	
#Parameters: 	none
#output: 	index.html
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

#Service: 		
#Description:	Perform custom searches based on elasticsearch queries in json format
#Parameters: 	<jsonQuery> is a json object which must follow the elasticsearch query structure
#output: 		a json object containing the matched results
@app.route('/genericSearch/<jsonQuery>')
def getGenericSearch(jsonQuery):
	return indexer.genericSearch(jsonQuery)

#Service: 		
#Parameters: 	
#output: 		
@app.route('/genericGeoSearch/<term>/<suburbCode>/<startP>/<sizeP>/<startDate>/<endDate>')
def getGenericGeoSearch(term,suburbCode,startP,sizeP,startDate,endDate):
	return indexer.getTweetsBySuburb(term,suburbCode,startP,sizeP,startDate,endDate)

#Service: 	
#Description:		
#Parameters: 	
#output: 		
@app.route('/sentimentTotals/<term>/<suburbCode>/<startDate>/<endDate>')
def getSentimentTotals(term,suburbCode,startDate,endDate):
	return indexer.statisticsByTerm(term,suburbCode,startDate,endDate)

#Service:		
#Description: 	Get a list of the suburbs of main cities of AU: ABS 2011
#Parameters: 	
#output: 		
@app.route('/suburbsByCountry/<countryCode>')
def getSuburbsList(countryCode):
	return indexer.getSuburbsList(countryCode)


#Service:		
#Description: 	Get GeoJson File containing information relatd to countries of birth by suburb of AU
#Parameters: 	<state> the code of the state: i.e: VIC, TAS, etc
#return: 		GeoJson object
@app.route('/culturesByState/<stateCode>')
def getCulturesByState(stateCode):
	return indexer.getCulturesByState(stateCode)

#Service: 
#Description:
#Parameters: 
#return: 
@app.route('/languagesByCountry/<countryCode>')
def getLanguagesByCountry(countryCode):
	return indexer.getLanguages(countryCode)

#Service: 
#Description:
#Parameters: 
#return: 
@app.route('/tweetsByCountryOfBirth/<term>/<stateCode>/<suburbCode>/<startDate>/<endDate>')
def getTweetsByCountryOfBirth(term,stateCode,suburbCode,startDate,endDate):
	return indexer.getTweetsByCountryOfBirth(term,stateCode,suburbCode,startDate,endDate)

#Service: 
#Description:
#Parameters: 
#return: 
# @app.route('/genericAggregation/<jsonQuery>')
# def getGenericAgg(jsonQuery):
# 	return indexer.getGenericAgg(jsonQuery)


#Service: 
#Description:
#Parameters: 
#return: 
@app.route('/topListBySuburb/<term>/<suburbCode>/<field>/<size>/<startDate>/<endDate>')
def getTopList(term,suburbCode,field,size,startDate,endDate):
	return indexer.getTopListBySuburb(term,suburbCode,field,size,startDate,endDate)

#main
if __name__ == "__main__":
	app.run(debug=True)