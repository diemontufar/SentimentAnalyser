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

from datetime import timedelta
from flask import make_response, request, current_app, jsonify
from functools import update_wrapper

# __file__ refers to the file settings.py 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')
APP_STATIC_JSON = os.path.join(APP_STATIC, 'json')

app = Flask(__name__)

try:
	unicode = unicode
except NameError:
	# 'unicode' is undefined, must be Python 3
	str = str
	unicode = str
	bytes = bytes
	basestring = (str,bytes)
else:
	# 'unicode' exists, must be Python 2
	str = str
	unicode = unicode
	bytes = str
	basestring = basestring

def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):
	
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

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
@app.route('/genericSearch/<jsonQuery>',methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def getGenericSearch(jsonQuery):
	return jsonify(indexer.genericSearch(jsonQuery))

#Service: 		
#Parameters: 	
#output: 		
@app.route('/genericGeoSearch/<term>/<suburbCode>/<startP>/<sizeP>/<startDate>/<endDate>',methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def getGenericGeoSearch(term,suburbCode,startP,sizeP,startDate,endDate):
	return jsonify(indexer.getTweetsBySuburb(term,suburbCode,startP,sizeP,startDate,endDate))

#Service: 	
#Description:		
#Parameters: 	
#output: 		
@app.route('/sentimentTotals/<term>/<suburbCode>/<startDate>/<endDate>',methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def getSentimentTotals(term,suburbCode,startDate,endDate):
	return jsonify(indexer.statisticsByTerm(term,suburbCode,startDate,endDate))

#Service:		
#Description: 	Get a list of the suburbs of main cities of AU: ABS 2011
#Parameters: 	
#output: 		
@app.route('/suburbsByCountry/<countryCode>',methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def getSuburbsList(countryCode):
	return jsonify(indexer.getSuburbsList(countryCode))


#Service:		
#Description: 	Get GeoJson File containing information relatd to countries of birth by suburb of AU
#Parameters: 	<state> the code of the state: i.e: VIC, TAS, etc
#return: 		GeoJson object
@app.route('/culturesByState/<stateCode>',methods=['GET', 'OPTIONS']) 
@crossdomain(origin='*')
def getCulturesByState(stateCode):
	return jsonify(indexer.getCulturesByState(stateCode))

#Service: 
#Description:
#Parameters: 
#return: 
@app.route('/languagesByCountry/<countryCode>',methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def getLanguagesByCountry(countryCode):
	return jsonify(indexer.getLanguages(countryCode))

#Service: 
#Description:
#Parameters: 
#return: 
@app.route('/tweetsByCountryOfBirth/<term>/<stateCode>/<suburbCode>/<startDate>/<endDate>',methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def getTweetsByCountryOfBirth(term,stateCode,suburbCode,startDate,endDate):
	return jsonify(indexer.getTweetsByCountryOfBirth(term,stateCode,suburbCode,startDate,endDate))


#Service: 
#Description:
#Parameters: 
#return: 
@app.route('/topListBySuburb/<term>/<suburbCode>/<field>/<size>/<startDate>/<endDate>',methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def getTopList(term,suburbCode,field,size,startDate,endDate):
	return jsonify(indexer.getTopListBySuburb(term,suburbCode,field,size,startDate,endDate))

#Service: 
#Description:
#Parameters: 
#return: 
@app.route('/sentimentTotalsByCity/<term>/<startDate>/<endDate>',methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def getSentimentTotalsByCity(term,startDate,endDate):
	return jsonify(indexer.getAllSentimentTotalsByCity(term,startDate,endDate))


#Service: 
#Description:
#Parameters: 
#return: 
@app.route('/topListByCity/<field>/<size>/<startTimestamp>/<endTimestamp>',methods=['GET','OPTIONS'])
@crossdomain(origin='*')
def getAllTopListByCity(field,size,startTimestamp, endTimestamp):
	return jsonify(indexer.getAllTopListsByCity(field,size,startTimestamp, endTimestamp))


#Service: 
#Description:
#Parameters: 
#return: 
@app.route('/cultureTotalsByCity/<term>/<stateCode>/<startTimestamp>/<endTimestamp>',methods=['GET','OPTIONS'])
@crossdomain(origin='*')
def getAllLanguagesTotalsByCity(term, stateCode, startTimestamp, endTimestamp):
	return jsonify(indexer.getAllLanguagesTotalsByCity(term, stateCode, startTimestamp, endTimestamp))


#Service: 
#Description:
#Parameters: 
#return: 
@app.route('/sentimentTotalsByCity/<term>/<stateCode>/<startTimestamp>/<endTimestamp>',methods=['GET','OPTIONS'])
@crossdomain(origin='*')
def getAllSentimentByCity(term,stateCode, startTimestamp, endTimestamp):
	return jsonify(indexer.getAllSentimentByCity(term,stateCode, startTimestamp, endTimestamp))


#Service: 
#Description:
#Parameters: 
#return: 
@app.route('/sentimentAnalysis/<text>',methods=['GET','OPTIONS'])
@crossdomain(origin='*')
def getSentimentAnalysis(text):
	return jsonify(indexer.getSentimentAnalysis(text))


#main
if __name__ == "__main__":
	app.run(debug=True)