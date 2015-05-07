#########################################################################################################
#
# Author: Diego Montufar
# Date: Apr/2015
# Name: indexer.py
# Description: 
#              
#
# Execution:   python indexer.py
#
#########################################################################################################

import indexer_settings as settings #custom settings
import elasticsearch #elasticsearch library
import couchdb #couchdb library
import json
import datetime
import tweet_classifier.classifier as classifier

es = elasticsearch.Elasticsearch()  # use default of localhost, port 9200


def getSentimentAnalysis(text):
  return classifier.doSentimentAnalysis(text)

# Method:           genericSearch
# Description:      Execute a generic query againt the index based on a json query
# Parameters:       jsonQuery must be a valid elasticsearch query.
# Further info:     http://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-queries.html
# Output:           matches (JSON)
def genericSearch(jsonQuery):
    matches = es.search(index=settings.es_index, doc_type=settings.es_docType, body=jsonQuery)
    return matches

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
            return doc

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
            return doc

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
            return doc

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


# Method:           getFormattedRange
# Description:      Parse start and end dates in timestamp format into a Lucene syntax for date ranges
# Parameters:       startTimestamp (String),endTimestamp (String) i.e. 1428069500339, 1430578700339
# Output:           range (String) i.e. [2015-01-01 TO 2015-02-01]
def getFormattedRange(startTimestamp,endTimestamp):

    #Format YY-mm-dd
    strStart = datetime.datetime.fromtimestamp(int(startTimestamp)/1000).strftime('%Y-%m-%d')
    strEnd = datetime.datetime.fromtimestamp(int(endTimestamp)/1000).strftime('%Y-%m-%d')

    if strStart == strEnd:
        return strStart #return a single date
    else:
        return "[" + strStart + " TO " + strEnd + "]" #return range

# Method:           statisticsByTerm
# Description:      
#                                 
# Parameters:       term (String)
#                   suburbCode (String)
#                   startTimestamp (String)
#                   endTimestamp (String)
# Output:           
def statisticsByTerm(term, suburbCode, startTimestamp, endTimestamp):

    dateRange = getFormattedRange(startTimestamp,endTimestamp)
    str_date_len = len(dateRange)

    if term == '*':
      query =  "created_at:" + dateRange
    else:
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

    return json.loads(result)

# Method:           
# Description:      
#                                 
# Parameters:       
# Output:           
def getTopListBySuburb(term,suburbCode,field,size, startTimestamp, endTimestamp): 

    dateRange = getFormattedRange(startTimestamp,endTimestamp)
    str_date_len = len(dateRange)

    multipolygon = getMultipolygon(suburbCode)

    if term == '*':
      query =  "created_at:" + dateRange
    else:
      query = 'text:' + term
      # query += " AND (sentiment_analysis.sentiment:positive OR sentiment_analysis.sentiment:negative OR sentiment_analysis.sentiment:neutral)"
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
    return matches

# Method:           
# Description:      
#                                 
# Parameters:       
# Output:           
def getTopListByCity(cityCode,field,size, startTimestamp, endTimestamp): 

    dateRange = getFormattedRange(startTimestamp,endTimestamp)
    str_date_len = len(dateRange)

    coordinates = getCityBoundingBox(cityCode)
    query =  "created_at:" + dateRange

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
                   "aggs": {"2": {"terms": {"field": field, "size": size, "order": {"_count": "desc"} } } },
                   "size":0
                }

    matches = es.search(index=settings.es_index, doc_type=settings.es_docType, body=jsonQuery)
    return matches

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

    if term == '*':
      query =  "created_at:" + dateRange
    else:
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
        return matches

# Method:           
# Description:      
#                                 
# Parameters:       
# Output:           
def getCityBoundingBox(stateCode):

    coordinates = None

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

    return coordinates


# Method:           
# Description:      
#                                 
# Parameters:       
# Output:           
def getAggTotalsByCity(term, field, stateCode, startTimestamp, endTimestamp):

    dateRange = getFormattedRange(startTimestamp,endTimestamp)
    str_date_len = len(dateRange)

    coordinates = getCityBoundingBox(stateCode)

    if term == '*':
      query =  "created_at:" + dateRange
    else:
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
                       "aggs": {"2": {"terms": {"field": field, "size": 0, "order": {"_count": "desc"} } } },
                       "size":0
                    }
        # print(jsonQuery)

        matches = es.search(index=settings.es_index, doc_type=settings.es_docType, body=jsonQuery)
        return matches

# Method:           
# Description:      
#                                 
# Parameters:       
# Output:           
def getBucketsFromResponse(response):

    responseJson = response
    bucks = {}
    total = 0

    if responseJson is not None:

        buckets = responseJson["aggregations"]["2"]["buckets"]

        for buck in buckets:

             bucks[buck["key"]] = buck["doc_count"] 
             total += buck["doc_count"] 

        return {"total" : total, "buckets" : bucks}


# Method:           
# Description:      
#                                 
# Parameters:       
# Output:           
def getAllSentimentTotalsByCity(term, startTimestamp, endTimestamp):

    statesList = ['VIC','NSW','TAS','WA','SA','NT','QLD']

    positive = 0
    negative = 0
    neutral = 0

    sentimentTotalsByCityList = {}

    for state in statesList:
        response = getAggTotalsByCity(term, "sentiment_analysis.sentiment" ,state, startTimestamp, endTimestamp)
        sentimentTotals = getBucketsFromResponse(response)

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

    return sentimentTotalsByCityList


# Method:           
# Description:      
#                                 
# Parameters:       
# Output:           
def getAllLanguagesTotalsByCity(term, stateCode, startTimestamp, endTimestamp):

    response = getAggTotalsByCity(term, "user.lang" ,stateCode, startTimestamp, endTimestamp)
    languageTotals = getBucketsFromResponse(response)
    languagesOfCountries = json.dumps(getLanguages(1), indent=4) #1: Australia
    jsonLanguagesOfCountries = json.loads(languagesOfCountries)

    cleanedLanguageTotals = {}
    languageList = {}
    total = languageTotals["total"]
    mergedList = list()


    for language in languageTotals["buckets"]:

      lang = language.lower()

      if lang == 'select language...':
        lang = 'und'

      country_name = findCountryName(jsonLanguagesOfCountries,lang)

      languageList[country_name] = languageList.get(country_name, 0) + languageTotals["buckets"][language]

    cleanedLanguageTotals["total"] = total
    cleanedLanguageTotals["buckets"] = languageList

    # print(json.dumps(cleanedLanguageTotals, indent=4))

    return cleanedLanguageTotals

# Method:           
# Description:      
#                                 
# Parameters:       
# Output:           
def findCountryName(jsonLanguagesOfCountries,lang):

  country_name = ''

  for cob in jsonLanguagesOfCountries["country_of_birth"]:
    languages = cob["languages"]
    for lan in languages:
      if lan == lang:
        return cob["name"]
    
  if country_name == '':
    return 'Born elsewhere(e)'

  return country_name


def getAllTopListsByCity(field,size,startTimestamp, endTimestamp):

  statesList = ['VIC','NSW','TAS','WA','SA','NT','QLD']

  topListsByCity = {}

  for state in statesList:
    response = getTopListByCity(state,field,size, startTimestamp, endTimestamp)
    topLists = getBucketsFromResponse(response)

    topListsByCity[state] = topLists

  return topListsByCity


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
    total = 0

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
        total += n
        mergedCountedList.append(cob)

    # print(total)

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

    languagesOfTweets = {}

    tweetsBySuburb = getTopListBySuburb(term,suburbCode,"user.lang",0, startTimestamp, endTimestamp)

    for buck in tweetsBySuburb["aggregations"]["2"]["buckets"]:
      lang = buck["key"]
      lang = lang.lower()

      if lang == 'select language...':
        lang = 'und'

      languagesOfTweets[lang] = buck["doc_count"]

    countryOfBirthBySuburb = getCulturesByState(stateCode)

    cultures = getCulturesBySuburb(countryOfBirthBySuburb,suburbCode)

    languagesOfCountries = json.dumps(getLanguages(1), indent=4) #1: Australia

    tweetsByCountryOfBirth = mergeTweetsLanguages(languagesOfTweets,json.loads(languagesOfCountries),cultures)

    res = {}
    res["buckets"] = tweetsByCountryOfBirth
    
    return res

# Method:           
# Description:      
#                                 
# Parameters:       
# Output:           
def getSuburbCodesFromGeoJson(geojsonSuburbsStr):

  geojsonSuburbs = json.loads(geojsonSuburbsStr)
  suburbList = {}

  for feature in geojsonSuburbs["features"]:
    code = feature["properties"]["feature_code"]
    name = feature["properties"]["feature_name"]

    suburbList[code] = name

  return suburbList


# Method:           
# Description:      
#                                 
# Parameters:       
# Output:           
def getAllSentimentByCity(term,stateCode, startTimestamp, endTimestamp):

  geojsonSuburbsStr = json.dumps(getCulturesByState(stateCode), indent=4)

  suburbList = getSuburbCodesFromGeoJson(geojsonSuburbsStr)

  response = {}

  for suburb in suburbList:
    stats = statisticsByTerm(term, suburb, startTimestamp, endTimestamp)

    response[suburb] = stats
    response[suburb]["suburb_name"] = suburbList[suburb]

  return response


#--------------------------------------
  # tweetsBySuburb = getTweetsBySuburb(term,suburbCode,fromP,sizeP, startTimestamp, endTimestamp)


# query = '{"query":{"filtered":{"query":{"match":{"text":{"query":"support","operator":"or"}}},"strategy":"query_first"}}}'
# query = '{"query":{"filtered":{"query":{"match":{"text":{"query":"love","operator":"or"}}},"filter":{"term":{"lang":"en"}}}},from:0,size:20}'
# query = '{"query":{"filtered":{"query":{"match":{"text":{"query":"love","operator":"or"}}},"filter":{"term":{"lang":"en"}}},from:1,size":50}}'
# print(statisticsByTerm('AFL','206041117'))
# # print(statisticsByTerm(query,'tweet'))
# print(customSearch(query,'tweet'))
#

# print(json.dumps(getTopListByCity('VIC',"entities.hashtags.text",5, "1428069500339", "1430578700339"), indent=4))

# print(json.dumps(getAllTopListsByCity("entities.hashtags.text",5,"1428303745213","1430809345213"), indent=4))


# print(json.dumps(getAllSentimentByCity("*", "SA", "1428303745213","1430809345213"), indent=4))

# getTweetsByLanguageByCity("*","VIC", "1420030800000","1430402400000") #Jan to May

# print(json.dumps(getSentimentAnalysis("I'm happy to be here"),indent=4))

# statisticsByTerm("love", "206041117", "1428069500339", "1430578700339")
# print(getSentimentTotalsByCity('AFL','VIC', "1428069500339", "1430578700339"))
# print(getAllSentimentTotalsByCity('AFL', "1428069500339", "1430578700339"))
# print(getCulturesByState('WA'))
# AFL/206041117/1428069500339/1430578700339"
# print(getTweetsBySuburb('a','206041122',"1427202000000", "1427202000000"))

#1427893200000 - 1430402400000
# 1428069500339/1430578700339"

# jsonQuery = '{"query":{"query_string":{"query":"text:AFL","analyze_wildcard":true}}}'
# print(type(genericSearch(jsonQuery)))

# print(json.dumps(getAllSentimentTotalsByCity('AFL', "1428069500339", "1430578700339")))

# print(type(getTweetsByCountryOfBirth('a','VIC','206041122',"1428069500339", "1430578700339")))

# print(type(statisticsByTerm('AFL', '206041122', "1428069500339", "1430578700339")))

# print(type(getLanguages(1)))

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
