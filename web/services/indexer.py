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

#Specific Web services
# def tweetsByTerm(jsonQuery, docType):
#     matches = es.search(index=settings.es_index, doc_type=docType, body=jsonQuery)
#     return json.dumps(matches, indent=4) 
def statisticsByTerm(term, suburbCode, docType):

    query = 'text:' + term
    query += " AND (sentiment_analysis.sentiment:positive OR sentiment_analysis.sentiment:negative OR sentiment_analysis.sentiment:neutral)"
    multipolygon = getMultipolygon(suburbCode)

    # print(multipolygon)

    jsonQuery = {
                   "query":{
                      "filtered":{
                         "filter":{
                            "or":{
                               "filters" : [
                                                {"geo_shape":{"place.bounding_box":{"relation": "within", "shape": {"type": "multipolygon", "coordinates": multipolygon } } } },
                                                {"geo_polygon": {"coordinates.coordinates": {"points" : multipolygon[0][0] } } }
                                            ],
                               "_cache":True
                            }
                         },
                         "query": {
                                    "query_string": {
                                      "query": query,
                                      "analyze_wildcard": True
                                    }
                        }
                      }
                   },
                   "aggs": {
                    "2": {
                      "terms": {
                        "field": "sentiment_analysis.sentiment",
                        "size": 3,
                        "order": {
                          "_count": "desc"
                        }
                      }
                    }
                  },
                   "size":0
                }

    matches = es.search(index=settings.es_index, doc_type=docType, body=jsonQuery)

    total = 0
    total_positive = 0
    total_neutral = 0
    total_negative = 0

    buckets = matches["aggregations"]["2"]["buckets"]

    for res in buckets:
        if res["key"] == "positive":
            total_positive = res["doc_count"]
            total += total_positive
        elif res["key"] == "neutral":
            total_neutral = res["doc_count"]
            total += total_neutral
        elif res["key"] == "negative":
            total_negative = res["doc_count"]
            total += total_negative

    mean_sentiment = "neutral"
    #Calculate the mean:
    if total_positive>total_negative and total_positive>total_neutral:
        mean_sentiment = "Positive"
    elif total_negative>total_positive and total_negative>total_neutral:
        mean_sentiment = "Negative"
    else:
        mean_sentiment = "Neutral"

    result = '{"results":{"total_tweets": %i, "mean_sentiment":\"%s\", "total_positive": %i, "total_neutral": %i, "total_negative": %i}}' % (total,mean_sentiment,total_positive,total_neutral,total_negative) 

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

#Get the corresponding document from suburbs couch database 
def getSuburbs(country):
    server = couchdb.Server(settings.server)
    try:
        #Just use existing DB
        db = server[settings.suburbs_database]
    except:
        print("Error while accessing suburbs couchdb data base!")
    for id in db:
        doc = getDocument(db,id)
        if doc["country_code"] == int(country):
            return json.dumps(doc, indent=4)

#Get the corresponding document from suburbs couch database 
def getLanguages(country):
    server = couchdb.Server(settings.server)
    try:
        #Just use existing DB
        db = server[settings.languages_database]
    except:
        print("Error while accessing languages couchdb data base!")
    for id in db:
        doc = getDocument(db,id)
        if doc["country_code"] == int(country):
            return json.dumps(doc, indent=4)

#Get the Multipolygon from cultures database
def getMultipolygon(suburbCode):
    server = couchdb.Server(settings.server)
    try:
        #Just use existing DB
        db = server[settings.cultures_database]
    except:
        print("Error while accessing cultures couchdb data base!")
    for id in db:
        doc = getDocument(db,id)
        
        for feature in doc["features"]:
            if feature["properties"]["feature_code"] == suburbCode:
                multipolygon = feature["geometry"]["coordinates"]
    return multipolygon

#Get the tweets located within a multipolygon and a set of points
def getTweetsBySuburb(term,suburbCode,fromP,sizeP,docType):

    query = 'text:' + term
    query += " AND (sentiment_analysis.sentiment:positive OR sentiment_analysis.sentiment:negative OR sentiment_analysis.sentiment:neutral)"
    multipolygon = getMultipolygon(suburbCode)

    if multipolygon:
        jsonQuery = {
                       "from":fromP,
                       "size":sizeP,
                       "query":{
                          "filtered":{
                             "filter":{
                                "or":{
                                   "_cache":True,
                                   "filters":[
                                                    {"geo_shape":{"place.bounding_box":{"relation": "within", "shape": {"type": "multipolygon", "coordinates": multipolygon } } } },
                                                    {"geo_polygon": {"coordinates.coordinates": {"points" : multipolygon[0][0] } } }
                                                ]
                                }
                             },
                             "query":{
                                "query_string": {
                                    "query": query
                                }
                             }
                          }
                       }
                    }

        matches = es.search(index=settings.es_index, doc_type=docType, body=jsonQuery)
        return json.dumps(matches, indent=4) 



# def getCustomAgg(docType,jsonQueryP):
# # "text:LOVE AND (sentiment_analysis.sentiment:positive OR sentiment_analysis.sentiment=negative OR sentiment_analysis.sentiment=neutral) AND -user.lang:en"

#     jsonQ = json.loads(jsonQueryP)
#     multipolygon = getMultipolygon(jsonQ["suburb"])

#     jsonQuery = {
#                    "size":0,
#                    "query":{"query_string":{"query":jsonQ["query"], 
#                             "analyze_wildcard":True } 
#                             }, 
#                    "aggs":{
#                       "2":{
#                          "terms":{
#                             "field":jsonQ["agg1"]["field"],
#                             "size":jsonQ["agg1"]["size"],
#                             "order":{
#                                "_count":jsonQ["agg1"]["order"]
#                             }
#                          },
#                          "aggs":{
#                             "3":{
#                                "terms":{
#                                   "field":jsonQ["agg2"]["field"],
#                                   "size":jsonQ["agg2"]["size"],
#                                   "order":{
#                                      "_count":jsonQ["agg2"]["order"]
#                                   } } } } } 
#                         },
#                     "filter": {
#                         "or" : {
#                           "filters" : [
#                                 {"geo_shape":{"place.bounding_box":{"relation": "within", "shape": {"type": "multipolygon", "coordinates": multipolygon } } } },
#                                 {"geo_polygon": {"coordinates.coordinates": {"points" : multipolygon[0][0] } } }
#                             ],
#                             "_cache" : True
#                         }
#                       }
#                 }
#     matches = es.search(index=settings.es_index, doc_type=docType, body=jsonQuery)
#     return json.dumps(matches, indent=4)

def getTopListBySuburb(docType,term,suburbCode,field,size): #Goooooood!

    multipolygon = getMultipolygon(suburbCode)
    query = "text:" + term
    query += " AND (sentiment_analysis.sentiment:positive OR sentiment_analysis.sentiment:negative OR sentiment_analysis.sentiment:neutral)"

    jsonQuery = {
                   "query":{
                      "filtered":{
                         "filter":{
                            "or":{
                               "filters" : [
                                                {"geo_shape":{"place.bounding_box":{"relation": "within", "shape": {"type": "multipolygon", "coordinates": multipolygon } } } },
                                                {"geo_polygon": {"coordinates.coordinates": {"points" : multipolygon[0][0] } } }
                                            ],
                               "_cache":True
                            }
                         },
                         "query": {
                                    "query_string": {
                                      "query": query,
                                      "analyze_wildcard": True
                                    }
                        }
                      }
                   },
                   "aggs": {"2": {"terms": {"field": field, "size": size, "order": {"_count": "desc"} } } },
                   "size":0
                }

    matches = es.search(index=settings.es_index, doc_type=docType, body=jsonQuery)
    return json.dumps(matches, indent=4)


################################################################################################# MUST BE REVISED!!!!


def getLanguagesFromTweetsBySuburb(tweetsBySuburb):

    totals = {}

    if tweetsBySuburb:
        for hits in tweetsBySuburb["hits"]["hits"]:
            lang = hits["_source"]["user"]["lang"]
            lang = lang.lower()

            if lang == 'select language...':
                lang = 'und'

            totals[lang] = totals.get(lang, 0) + 1
        return totals
    else:
        return None

def getCulturesBySuburb(countryOfBirthBySuburb,suburbCode):
    if countryOfBirthBySuburb:
        for crs in countryOfBirthBySuburb["features"]:
            suburb = crs["properties"]["feature_code"]
            if suburb == suburbCode:
                return crs["properties"]["country_of_birth"]
    else:
        return None


def mergeTweetsLanguages(languagesOfTweets,languagesOfCountries,cultures):

    counts = {}
    mergedList = list()

    for cob in cultures:
        languages = getListLanguages(languagesOfCountries["country_of_birth"],cob["id"])
        cob["languages"] = languages
        cob["count"] = 0
        mergedList.append(cob)

    for lan in languagesOfTweets:

        countryIndex = isInMergedList(mergedList,lan)

        if countryIndex:
            counts[countryIndex] = counts.get(countryIndex, 0) + languagesOfTweets[lan]
        else:
            counts["BE"] = counts.get("BE", 0) + languagesOfTweets[lan]

    mergedCountedList = list()

    for cob in mergedList:

        id = cob["id"]

        try:
            n = counts[id]
        except KeyError:
            n = 0

        cob["count"] = n
        mergedCountedList.append(cob)

    return mergedCountedList



def isInMergedList(mergedList,language):

    for cob in mergedList:
        for lan in cob["languages"]:
            if lan == language:
                return cob["id"]
    return False


def getListLanguages(languagesOfCountries,id):
    for cob in languagesOfCountries:
        if cob["id"] == id:
            return cob["languages"]

def getCountLanguages(languagesOfTweets,id):
    for lan in languagesOfTweets:
        if lan == id:
            return int(languagesOfTweets[lan])


def getTweetsByCountryOfBirth(term,stateCode,suburbCode):
    tweetsBySuburb = json.loads(getTweetsBySuburb(term,suburbCode,0,10000,"tweet"))
    languagesOfTweets = getLanguagesFromTweetsBySuburb(tweetsBySuburb)

    countryOfBirthBySuburb = json.loads(getCultures(stateCode))
    cultures = getCulturesBySuburb(countryOfBirthBySuburb,suburbCode)

    languagesOfCountries = json.loads(getLanguages(1)) #1: Australia

    tweetsByCountryOfBirth = mergeTweetsLanguages(languagesOfTweets,languagesOfCountries,cultures)
    
    return json.dumps(tweetsByCountryOfBirth, indent=4)


# query = '{"query":{"filtered":{"query":{"match":{"text":{"query":"support","operator":"or"}}},"strategy":"query_first"}}}'
# query = '{"query":{"filtered":{"query":{"match":{"text":{"query":"love","operator":"or"}}},"filter":{"term":{"lang":"en"}}}},from:0,size:20}'
# query = '{"query":{"filtered":{"query":{"match":{"text":{"query":"love","operator":"or"}}},"filter":{"term":{"lang":"en"}}},from:1,size":50}}'
# print(statisticsByTerm('AFL','206041117','tweet'))
# # print(statisticsByTerm(query,'tweet'))
# print(customSearch(query,'tweet'))
#

# print(getTweetsBySuburb('AFL','206041122','tweet'))

# test = {
#    "query":"text:AFL AND (sentiment_analysis.sentiment:positive OR sentiment_analysis.sentiment=negative OR sentiment_analysis.sentiment=neutral) AND -user.lang:en",
#    "agg1":{
#       "field":"user.lang",
#       "size":1,
#       "order":"desc"
#    },
#    "agg2":{
#       "field":"sentiment_analysis.sentiment",
#       "size":1,
#       "order":"desc"
#    }
# }
# # print(test[query])
# print(getCustomAgg('tweet',test))

# print(getLanguages ('1'))

print(getTweetsByCountryOfBirth('AFL','VIC','206041122'))
# print(getTweetsBySuburb('a','206041122','tweet'))

# {"query":{"filtered":{"query":{"match":{"text":{"query":"love","operator":"or"}}},"filter":{"term":{"lang":"en"}}}}}
# print(getCultures('VIC'))
# print(getTweetsBySuburb('AFL','206041117','tweet'))
