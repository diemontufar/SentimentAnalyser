import indexer_settings as settings #custom settings
import elasticsearch #elasticsearch library
import couchdb #couchdb library
import json
import datetime

es = elasticsearch.Elasticsearch()  # use default of localhost, port 9200

# Method:           genericSearch
# Description:      Execute a generic query againt the index based on a json query
# Parameters:       jsonQuery must be a valid elasticsearch query.
# Further info:     http://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-queries.html
# Output:           matches (JSON)
def genericSearch(jsonQuery):
    matches = es.search(index=settings.es_index, doc_type=settings.es_docType, body=jsonQuery)
    return json.dumps(matches, indent=4) 

# Method:           count
# Description:      Count the number of ocurrences in a index based on a json query
# Parameters:       jsonQuery must be a valid elasticsearch query.
# Further info:     http://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-queries.html
# Output:           counter (Integer)
def count(jsonQuery):
    num = es.count(index=settings.es_index, doc_type=settings.es_docType, body=jsonQuery)
    counter = num['count']
    return int(counter)

# Method:           getDocument
# Description:      Obtain a document from couchdb by ID   
# Parameters:       couchdb database connection and document id
# Output:           doc (JSON)
def getDocument(db,id):
    doc = db.get(id)
    return doc

# Method:           getCulturesByState
# Description:      Obtain the list of cultures by state from couchdb database            
# Parameters:       stateCode (String) as defined on the database i.e. 'VIC'
# Output:           doc (JSON)
def getCulturesByState(stateCode):
    server = couchdb.Server(settings.server)
    try:
        #Just use existing DB
        db = server[settings.cultures_database]
    except:
        print("Error while accessing couchdb data base!")
    for id in db:
        doc = getDocument(db,id)
        if doc["crs"]['properties']['state_id'] == stateCode:
            return json.dumps(doc, indent=4)

# Method:           getSuburbsList
# Description:      Obtain the list of suburbs by country from couchdb database                    
# Parameters:       countryCode (String) as defined on the database i.e. '1' (corresponds to Australia)
# Output:           doc (JSON)
def getSuburbsList(countryCode):
    server = couchdb.Server(settings.server)
    try:
        #Just use existing DB
        db = server[settings.suburbs_database]
    except:
        print("Error while accessing suburbs couchdb data base!")
    for id in db:
        doc = getDocument(db,id)
        if doc["country_code"] == int(countryCode):
            return json.dumps(doc, indent=4)

# Method:           getLanguages
# Description:      Obtain the list of suburbs by country from couchdb database
# Parameters:       countryCode (String) as defined on the database i.e. '1' (corresponds to Australia)
# Output:           doc (JSON)
def getLanguages(countryCode):
    server = couchdb.Server(settings.server)
    try:
        #Just use existing DB
        db = server[settings.languages_database]
    except:
        print("Error while accessing languages couchdb data base!")
    for id in db:
        doc = getDocument(db,id)
        if doc["country_code"] == int(countryCode):
            return json.dumps(doc, indent=4)

# Method:           getMultipolygon
# Description:      Obtain multipolygon defined on GeoJson document on couchdb database        
# Parameters:       suburbCode (String) as defined on the database i.e. '206041122' (corresponds to melbourne)
# Output:           multipolygon (Geojson Feature)
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


def getFormattedRange(startTimestamp,endTimestamp):

    strStart = datetime.datetime.fromtimestamp(int(startTimestamp)/1000).strftime('%Y-%m-%d')
    strEnd = datetime.datetime.fromtimestamp(int(endTimestamp)/1000).strftime('%Y-%m-%d')

    if strStart == strEnd:
        return strStart
    else:
        return "[" + strStart + " TO " + strEnd + "]"

# Method:           
# Description:      
#                                 
# Parameters:       
# Output:           
def statisticsByTerm(term, suburbCode, startTimestamp, endTimestamp):

    dateRange = getFormattedRange(startTimestamp,endTimestamp)
    str_date_len = len(dateRange)

    query = 'text:' + term
    query += " AND (sentiment_analysis.sentiment:positive OR sentiment_analysis.sentiment:negative OR sentiment_analysis.sentiment:neutral)"
    query +=  " AND created_at:" + dateRange

    multipolygon = getMultipolygon(suburbCode)

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

    matches = es.search(index=settings.es_index, doc_type=settings.es_docType, body=jsonQuery)

    print(jsonQuery)

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

# Method:           
# Description:      
#                                 
# Parameters:       
# Output:           
def getTopListBySuburb(term,suburbCode,field,size, startTimestamp, endTimestamp): 

    dateRange = getFormattedRange(startTimestamp,endTimestamp)
    str_date_len = len(dateRange)

    multipolygon = getMultipolygon(suburbCode)
    query = "text:" + term
    query += " AND (sentiment_analysis.sentiment:positive OR sentiment_analysis.sentiment:negative OR sentiment_analysis.sentiment:neutral)"
    query +=  " AND created_at:" + dateRange

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

    matches = es.search(index=settings.es_index, doc_type=settings.es_docType, body=jsonQuery)
    return json.dumps(matches, indent=4)


# Method:           
# Description:      
#                   
#                   
# Parameters:       
# Output:           
#Get the tweets located within a multipolygon and a set of points
def getTweetsBySuburb(term,suburbCode,fromP,sizeP, startTimestamp, endTimestamp):

    dateRange = getFormattedRange(startTimestamp,endTimestamp)
    str_date_len = len(dateRange)

    multipolygon = getMultipolygon(suburbCode)
    query = 'text:' + term
    query += " AND (sentiment_analysis.sentiment:positive OR sentiment_analysis.sentiment:negative OR sentiment_analysis.sentiment:neutral)"
    query +=  " AND created_at:" + dateRange
    

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

        matches = es.search(index=settings.es_index, doc_type=settings.es_docType, body=jsonQuery)
        return json.dumps(matches, indent=4) 


def getCityBoundingBox(stateCode):

    if stateCode == 'VIC':
        coordinates = {"bottom_right" : [145.764740,-38.260720], "top_left" : [144.394492,-37.459846] }
    elif stateCode == 'NSW':
        coordinates = {"bottom_right" : [151.342636,-34.169249], "top_left" : [150.502229,-33.424598] }
    elif stateCode == 'TAS':
        coordinates = {"bottom_right" : [147.341501,-42.891561], "top_left" : [147.315681,-42.873221] }
    elif stateCode == 'WA':
        coordinates = {"bottom_right" : [116.413915,-32.482907], "top_left" : [115.448767,-31.454860] }
    elif stateCode == 'SA':
        coordinates = {"bottom_right" : [139.043564,-35.464059 ], "top_left" : [138.360346,-34.507872] }
    elif stateCode == 'NT':
        coordinates = {"bottom_right" : [131.200600,-12.859710], "top_left" : [130.815152,-12.330012] }
    elif stateCode == 'QLD':
        coordinates = {"bottom_right" : [153.552920,-28.037280], "top_left" : [152.452799,-26.777500] }

        140.9923,-39.2060,150.1329,-35.8547

    return coordinates

# Method:           
# Description:      
#                   
#                   
# Parameters:       
# Output:   
def getSentimentTotalsByCity(term, stateCode, startTimestamp, endTimestamp):

    dateRange = getFormattedRange(startTimestamp,endTimestamp)
    str_date_len = len(dateRange)

    coordinates = getCityBoundingBox(stateCode)
    query = 'text:' + term
    query += " AND (sentiment_analysis.sentiment:positive OR sentiment_analysis.sentiment:negative OR sentiment_analysis.sentiment:neutral)"
    query +=  " AND created_at:" + dateRange

    if coordinates:
        jsonQuery = {
                       "query":{
                          "filtered":{
                             "filter": {
                                        "geo_bounding_box": {
                                          "coordinates.coordinates": coordinates
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
                       "aggs": {"2": {"terms": {"field": "sentiment_analysis.sentiment", "size": 0, "order": {"_count": "desc"} } } },
                       "size":0
                    }
        # print(jsonQuery)

        matches = es.search(index=settings.es_index, doc_type=settings.es_docType, body=jsonQuery)
        return json.dumps(matches, indent=4) 


def getDataFromResponse(response):

    responseJson = json.loads(response)
    bucks = {}

    if responseJson is not None:

        total = responseJson["hits"]["total"]
        buckets = responseJson["aggregations"]["2"]["buckets"]

        for buck in buckets:

             bucks[buck["key"]] = buck["doc_count"] 

        return {"total" : total, "buckets" : bucks}



def getAllSentimentTotalsByCity(term, startTimestamp, endTimestamp):

    statesList = ['VIC','NSW','TAS','WA','SA','NT','QLD']

    positive = 0
    negative = 0
    neutral = 0

    sentimentTotalsByCityList = {}

    for state in statesList:
        response = getSentimentTotalsByCity(term, state, startTimestamp, endTimestamp)
        sentimentTotals = getDataFromResponse(response)

        try:
            positive = sentimentTotals["buckets"]["positive"]
        except KeyError:
            positive = 0

        try:
            negative = sentimentTotals["buckets"]["negative"]
        except KeyError:
            negative = 0

        try:
            neutral = sentimentTotals["buckets"]["neutral"]
        except KeyError:
            neutral = 0

        sentimentTotalsByCityList[state] = {"total" : sentimentTotals["total"], "positive": positive, "negative" : negative, "neutral": neutral }

        positive = 0
        negative = 0
        neutral = 0

    return json.dumps(sentimentTotalsByCityList, indent=4) 

# def getCustomAgg(jsonQueryP):
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
#     matches = es.search(index=settings.es_index, doc_type=settings.es_docType, body=jsonQuery)
#     return json.dumps(matches, indent=4)





################################################################################################# MUST BE REVISED!!!!

# Method:           
# Description:      
#                                 
# Parameters:       
# Output:           
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

# Method:           
# Description:      
#                                 
# Parameters:       
# Output:           
def getCulturesBySuburb(countryOfBirthBySuburb,suburbCode):
    if countryOfBirthBySuburb:
        for crs in countryOfBirthBySuburb["features"]:
            suburb = crs["properties"]["feature_code"]
            if suburb == suburbCode:
                return crs["properties"]["country_of_birth"]
    else:
        return None

# Method:           
# Description:      
#                                 
# Parameters:       
# Output:           
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


# Method:           
# Description:      
#                                 
# Parameters:       
# Output:           
def isInMergedList(mergedList,language):

    for cob in mergedList:
        for lan in cob["languages"]:
            if lan == language:
                return cob["id"]
    return False

# Method:           
# Description:      
#                                 
# Parameters:       
# Output:           
def getListLanguages(languagesOfCountries,id):
    for cob in languagesOfCountries:
        if cob["id"] == id:
            return cob["languages"]

def getCountLanguages(languagesOfTweets,id):
    for lan in languagesOfTweets:
        if lan == id:
            return int(languagesOfTweets[lan])

# Method:           
# Description:      
#                                 
# Parameters:       
# Output:           
def getTweetsByCountryOfBirth(term,stateCode,suburbCode,startTimestamp, endTimestamp):
    tweetsBySuburb = json.loads(getTweetsBySuburb(term,suburbCode,0,10000, startTimestamp, endTimestamp))
    languagesOfTweets = getLanguagesFromTweetsBySuburb(tweetsBySuburb)

    countryOfBirthBySuburb = json.loads(getCulturesByState(stateCode))
    cultures = getCulturesBySuburb(countryOfBirthBySuburb,suburbCode)

    languagesOfCountries = json.loads(getLanguages(1)) #1: Australia

    tweetsByCountryOfBirth = mergeTweetsLanguages(languagesOfTweets,languagesOfCountries,cultures)
    
    return json.dumps(tweetsByCountryOfBirth, indent=4)


# query = '{"query":{"filtered":{"query":{"match":{"text":{"query":"support","operator":"or"}}},"strategy":"query_first"}}}'
# query = '{"query":{"filtered":{"query":{"match":{"text":{"query":"love","operator":"or"}}},"filter":{"term":{"lang":"en"}}}},from:0,size:20}'
# query = '{"query":{"filtered":{"query":{"match":{"text":{"query":"love","operator":"or"}}},"filter":{"term":{"lang":"en"}}},from:1,size":50}}'
# print(statisticsByTerm('AFL','206041117'))
# # print(statisticsByTerm(query,'tweet'))
# print(customSearch(query,'tweet'))
#

# statisticsByTerm("love", "206041117", "1428069500339", "1430578700339")
# print(getSentimentTotalsByCity('AFL','VIC', "1428069500339", "1430578700339"))
print(getAllSentimentTotalsByCity('AFL', "1428069500339", "1430578700339"))
# AFL/206041117/1428069500339/1430578700339"
# print(getTweetsBySuburb('a','206041122',"1427202000000", "1427202000000"))

#1427893200000 - 1430402400000
# 1428069500339/1430578700339"

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

# print(getTweetsByCountryOfBirth('AFL','VIC','206041122'))
# print(getTweetsBySuburb('a','206041122','tweet'))

# {"query":{"filtered":{"query":{"match":{"text":{"query":"love","operator":"or"}}},"filter":{"term":{"lang":"en"}}}}}
# print(getCultures('VIC'))
# print(getTweetsBySuburb('AFL','206041117','tweet'))
