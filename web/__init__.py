from flask import Flask , render_template
from services import indexer
import os
# __file__ refers to the file settings.py 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')
APP_STATIC_JSON = os.path.join(APP_STATIC, 'json')

app = Flask(__name__)

#Service: main template web page
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

#Service: perform customs search based on elasticsearch queries in json format
@app.route('/customSearch/<jsonQuery>')
def getCustomSearch(jsonQuery):
	doc_type = 'tweet'
	return indexer.customSearch(jsonQuery,doc_type)

#Service: perform search based in a term in order to populate chart and table
@app.route('/sentimentTotals/<jsonQuery>')
def getSentimentTotals(jsonQuery):
	doc_type = 'tweet'
	return indexer.statisticsByTerm(jsonQuery,doc_type)

#Service: Get a list of the suburbs of main cities of AU: ABS 2011
@app.route('/listSuburbs')
def listSuburbsAU():
	return open(APP_STATIC_JSON+"/suburbs.json", 'r').read()


#main
if __name__ == "__main__":
	app.run(debug=True)