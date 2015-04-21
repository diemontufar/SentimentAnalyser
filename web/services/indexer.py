import indexer_settings as settings
import elasticsearch #elasticsearch library
import couchdb #couchdb library
import json

es = elasticsearch.Elasticsearch()  # use default of localhost, port 9200

#Perform a search in a index based on a particular text
def simpleSearch(query):
    matches = es.search(index=settings.es_index, q=query)
    #hits = matches['hits']['hits']
    return json.dumps(matches, indent=4) 

#Perform a search in a index based on a custom json query
def customSearch(jsonQuery, docType):
    matches = es.search(index=settings.es_index, doc_type=docType, body=jsonQuery)
    return json.dumps(matches, indent=4) 

#Count the number of ocurrences in a index based on a json query
def count(jsonQuery, docType):
    num = es.count(index=settings.es_index, doc_type=docType, body=jsonQuery)
    counter = num['count']
    return int(counter)

#TODO: this must be dynamic!!!!
def getRegions():
    return '"regions":{"NSW":{"name":"NewSouthWales","sentiment":"positive","positive":123,"neutral":15,"negative":65},"NT":{"name":"NorthernTerritory","sentiment":"positive","positive":456,"neutral":156,"negative":46},"QLD":{"name":"Queensland","sentiment":"negative","positive":25,"neutral":133,"negative":250},"SA":{"name":"SouthAustralia","sentiment":"negative","positive":12,"neutral":45,"negative":90},"TAS":{"name":"Tasmania","sentiment":"neutral","positive":123,"neutral":247,"negative":39},"VIC":{"name":"Victoria","sentiment":"positive","positive":421,"neutral":9,"negative":117},"WA":{"name":"WesternAustralia","sentiment":"negative","positive":50,"neutral":34,"negative":129}'

#Specific Web services
# def tweetsByTerm(jsonQuery, docType):
#     matches = es.search(index=settings.es_index, doc_type=docType, body=jsonQuery)
#     return json.dumps(matches, indent=4) 
def statisticsByTerm(jsonQuery, docType):
    # matches = es.search(index=settings.es_index, doc_type=docType, body=jsonQuery)
    total = count(jsonQuery, docType) #count total number of tweets
    
    #Modify jsonQuery in order to get counts and build a response
    newJsonQuery = json.loads(jsonQuery);

    boolean_filter = json.loads('{"bool":{"must":[{"term":{"lang":"en"}},{"term":{"sentiment":"positive"}}]}}')
    newJsonQuery['query']['filtered']['filter'] = boolean_filter
    total_positive = count(newJsonQuery, docType)

    boolean_filter = json.loads('{"bool":{"must":[{"term":{"lang":"en"}},{"term":{"sentiment":"negative"}}]}}')
    newJsonQuery['query']['filtered']['filter'] = boolean_filter
    total_negative = count(newJsonQuery, docType)

    boolean_filter = json.loads('{"bool":{"must":[{"term":{"lang":"en"}},{"term":{"sentiment":"neutral"}}]}}')
    newJsonQuery['query']['filtered']['filter'] = boolean_filter
    total_neutral = count(newJsonQuery, docType)

    mean_sentiment = "neutral"
    #Calculate the mean:
    if total_positive>total_negative and total_positive>total_neutral:
        mean_sentiment = "positive"
    elif total_negative>total_positive and total_negative>total_neutral:
        mean_sentiment = "negative"
    else:
        mean_sentiment = "neutral"

    regions = getRegions()

    result = '{"results":{"total_tweets": %i, "mean_sentiment":\"%s\", "total_positive": %i, "total_neutral": %i, "total_negative": %i,%s}}}' % (total,mean_sentiment,total_positive,total_neutral,total_negative,regions) 

    return json.dumps(result, indent=4) 

#Get the document from couchdb by ID
def getDocument(db,id):
    doc = db.get(id)
    return doc

#Get the corresponding document from cultures couch database by state
#Disclaimer: If you have more than one document with the same state, this will return an array of docs
#If there is an empty result, return 'None'
def getCultures(state):
    server = couchdb.Server(settings.server)
    try:
        #Just use existing DB
        db = server[settings.cultures_database]
    except:
        print("Error while accessing couchdb data base!")
    for id in db:
        doc = getDocument(db,id)
        if doc["crs"]['properties']['state_id'] == state:
            return json.dumps(doc, indent=4)

#Get the tweets located within a multipolygon and a set of points
def getTweetsBySuburb(term,suburb,docType):

    server = couchdb.Server(settings.server)
    try:
        #Just use existing DB
        db = server[settings.cultures_database]
    except:
        print("Error while accessing couchdb data base!")
    for id in db:
        doc = getDocument(db,id)
        
        for feature in doc["features"]:
            if feature["properties"]["feature_code"] == suburb:
                multipolygon = feature["geometry"]["coordinates"]


    if multipolygon:
        jsonQuery = {
                  "query": {"filtered": {"query": {"match": {"text": {"query": term, "operator": "or"} } }, 
                    "filter": {
                        "or" : {
                          "filters" : [
                                {"geo_shape":{"place.bounding_box":{"relation": "within", "shape": {"type": "multipolygon", "coordinates": multipolygon } } } },
                                {"geo_polygon": {"coordinates.coordinates": {"points" : multipolygon[0][0] } } }
                            ],
                            "_cache" : True
                        }
                      }
                    }
                  },
                  "size" : 1500
                }
        matches = es.search(index=settings.es_index, doc_type=docType, body=jsonQuery)
        return json.dumps(matches, indent=4) 


# query = '{"query":{"filtered":{"query":{"match":{"text":{"query":"support","operator":"or"}}},"strategy":"query_first"}}}'
# query = '{"query":{"filtered":{"query":{"match":{"text":{"query":"love","operator":"or"}}},"filter":{"term":{"lang":"en"}}}},from:0,size:20}'
# query = '{"query":{"filtered":{"query":{"match":{"text":{"query":"love","operator":"or"}}},"filter":{"term":{"lang":"en"}}},from:1,size":50}}'
# # print(statisticsByTerm(query,'tweet'))
# # print(statisticsByTerm(query,'tweet'))
# print(customSearch(query,'tweet'))


# {"query":{"filtered":{"query":{"match":{"text":{"query":"love","operator":"or"}}},"filter":{"term":{"lang":"en"}}}}}
# print(getCultures('VIC'))
# print(getTweetsBySuburb('AFL','206041117','tweet'))
