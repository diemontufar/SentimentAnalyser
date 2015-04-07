from flask import Flask , jsonify, render_template
from textblob import TextBlob
import indexer

app = Flask(__name__)

#Service: main template web page
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

#Service: perform basic searches by field
@app.route('/simpleSearch/<text>')
def doSimpleSearch(text):
	return str(indexer.simpleCount('twitterall.text:'+text)) #This must be reviewed

#Service: perform customs search based on elasticsearch queries in json format
@app.route('/customSearch/<jsonQuery>')
def doCustomSearch(jsonQuery):
	doc_type = 'tweet'
	return str(indexer.customSearch(jsonQuery,doc_type))

#Test Services:
@app.route('/test_json/pie')
def getPieData():
	return open("/Users/diogonal/Documents/Git Projects/SentimentAnalyser/web/static/test_json/results.json", 'r').read()

@app.route('/test_json/tweetfeed')
def getResultsData():
	enc='utf-8'
	return open("/Users/diogonal/Documents/Git Projects/SentimentAnalyser/web/static/test_json/tweet.json", 'r',encoding=enc).read()


#main
if __name__ == "__main__":
	app.run(debug=True)