from flask import Flask , render_template
import indexer

app = Flask(__name__)

#Service: main template web page
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

#Service: perform customs search based on elasticsearch queries in json format
@app.route('/customSearch/<jsonQuery>')
def doCustomSearch(jsonQuery):
	doc_type = 'tweet'
	return indexer.customSearch(jsonQuery,doc_type)

#Service: perform search based in a term in order to populate chart and table
@app.route('/chartTableSearch/<jsonQuery>')
def doChartTableSearch(jsonQuery):
	doc_type = 'tweet'
	return indexer.statisticsByTerm(jsonQuery,doc_type)

#main
if __name__ == "__main__":
	app.run(debug=True)