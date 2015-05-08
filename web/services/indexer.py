#########################################################################################################
#
# Author:       Diego Montufar
# Date:         Apr/2015
# Name:         indexer.py
# Description:  This module builds queries based on the user-defined parameters taken from the URL's requesting call.
#               There is a direct connection to elasticsearch and couchdb as defined on the settings file.
#               Almost every query/response takes the form of a json structure, so called 'dictionary' in python, which is either returned
#               or taken as parameter by some methods of this class.
#               Error handling is not considered strictly in this module as any problem during requests comming from the client request,
#               must be handled by the client's code side. However, PUT and DELETE operations are not allowed as we are only
#               calling GET and POST calls for performing simple or more complex searches.
#
# Execution:    This module can be executed independently as well, by calling any of the implemented methods as follows: python indexer.py
# Dependencies: tweet_classifier, couchdb,elasticsearch
#
#########################################################################################################

import indexer_settings as settings #custom settings
import elasticsearch #elasticsearch library
import couchdb #couchdb library
import json
import datetime
import tweet_classifier.classifier as classifier #Sentiment Analysis tool

es = elasticsearch.Elasticsearch()  # use default of localhost, port 9200

# Method:           getSentimentAnalysis
# Description:      Perform sentiment analysis using the tweet_classifier python tools
# Parameters:       jsonQuery must be a valid elasticsearch query.
# Further info:     http://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-queries.html
# Output:           matches (JSON)
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
# Description:      Sentiment statistics by term and by suburb within a date range
# Parameters:       term (String)
#                   suburbCode (String)
#                   startTimestamp (String)
#                   endTimestamp (String)
# Output:           json object containing sentiment results
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
                         "query": { "query_string": {"query": query, "analyze_wildcard": True } }
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

# Method:           getTopListBySuburb
# Description:      List the top N list count of a particular field within a date range by suburb
# Parameters:       term        (String)  -> Text you want to search for. i.e. AFL or Tony Abbott or *
#                   suburbCode  (String)  -> Suburb code. i.e. 206041122
#                   field       (String)  -> Twitter field to aggreagate i.e. user.screen_name
#                   size        (Int)     -> N i.e 5 for a Top five list 
#                   startTimestamp   (Int)     -> Timestamp start date. i.e 1428069500339
#                   endTimestamp     (Int)     -> Timestamp end date i.e 1430578700339
# Output:           a json object containing the matched results
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

# Method:           getTopListByCity
# Description:      Generic query for searching aggregated field within a bounding box
# Parameters:       stateCode   (String)  -> State code. i.e. VIC, TAS
#                   field       (String)  -> Twitter field to aggreagate i.e. user.screen_name
#                   size        (Int)     -> N i.e 5 for a Top five list 
#                   startTimestamp   (Int)     -> Timestamp start date. i.e 1428069500339
#                   endTimestamp     (Int)     -> Timestamp end date i.e 1430578700339
# Output:           a json object containing the matched results
def getTopListByCity(stateCode,field,size, startTimestamp, endTimestamp): 

    dateRange = getFormattedRange(startTimestamp,endTimestamp)
    str_date_len = len(dateRange)

    coordinates = getCityBoundingBox(stateCode)
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

# Method:           getTweetsBySuburb
# Description:      Get all the tweets within a multipolygon defined on the geo json cultures database
# Parameters:       term            (String)  -> Text you want to search for. i.e. AFL or Tony Abbott or *
#                   suburbCode      (String)  -> Suburb code. i.e. 206041122
#                   fromP           (Int)     -> Pagination support. i.e. 0 if you want all the results, or 15 if you want to skip the first 15 results
#                   sizeP            (Int)     -> Pagination support. i.e 50 if you want up to 50 resutls by taking account of startP parameter
#                   startTimestamp   (Int)     -> Timestamp start date. i.e 1428069500339
#                   endTimestamp     (Int)     -> Timestamp end date i.e 1430578700339
# Output:    a json object containing the matched results
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

# Method:           getCityBoundingBox
# Description:      Get the corresponding bounding box around a particular city             
# Parameters:       stateCode       (String) -> State code. i.e. VIC, TAS
# Output:           bounding box coordinates
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


# Method:           getAggTotalsByCity
# Description:      Generic method for getting aggregations based on a query with results falling within a bounding box
# Parameters:       term        (String)  -> Text you want to search for. i.e. AFL or Tony Abbott or *
#                   field       (String)  -> Twitter field to aggreagate i.e. user.screen_name
#                   startTimestamp   (Int)     -> Timestamp start date. i.e 1428069500339
#                   endTimestamp     (Int)     -> Timestamp end date i.e 1430578700339
# Output:           a json object containing the matched results
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

# Method:           getBucketsFromResponse
# Description:      Helper method for retreiving results from bukets array comming from an elasticsearch response
#                                 
# Parameters:       response (Json Object) -> elasticsearch styled response
# Output:           a json object containing the matched results
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


# Method:           getAllSentimentTotalsByCity
# Description:      Build a query response with sentiment total statistics by term within a date range.
#                   This method does multiple calls to the getAggTotalsByCity method and builds the response
#                   based on the results obtained for each city.
# Parameters:       term        (String)  -> Text you want to search for. i.e. AFL or Tony Abbott or *
#                   startTimestamp   (Int)     -> Timestamp start date. i.e 1428069500339
#                   endTimestamp     (Int)     -> Timestamp end date i.e 1430578700339
# Output:           a json object containing the matched results
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


# Method:           getAllLanguagesTotalsByCity
# Description:      Get the count of languages found on the tweets by terms within a date range
# Parameters:       term              (String)  -> Text you want to search for. i.e. AFL or Tony Abbott or *
#                   startTimestamp    (String)  -> the code of the state: i.e: VIC, TAS, etc
#                   endTimestamp      (Int)     -> Timestamp start date. i.e 1428069500339
#                   endDate           (Int)     -> Timestamp end date i.e 1430578700339
# Output:           a json object containing the matched results
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

# Method:           findCountryName
# Description:      Helper method for finding the name of a language by its code. i.e. en-gb corresponds to United Kigndom
# Parameters:       jsonLanguagesOfCountries (Json object) -> large object containing all data (by state) comming from the 
#                                                             cultures database corresponding to a particular state/city
#                   lang (String)                          -> The language ou are looking for
# Output:           the name of the language you are looking for
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


# Method:            getAllTopListsByCity
# Description:       Get the top N list by city within a date range
# Parameters:        field       (String)  -> Twitter field to aggreagate i.e. user.screen_name
#                    size        (Int)     -> N i.e 5 for a Top five list 
#                    startDate   (Int)     -> Timestamp start date. i.e 1428069500339
#                    endDate     (Int)     -> Timestamp end date i.e 1430578700339
# Output:            a json object containing the matched results
def getAllTopListsByCity(field,size,startTimestamp, endTimestamp):

  statesList = ['VIC','NSW','TAS','WA','SA','NT','QLD']

  topListsByCity = {}

  for state in statesList:
    response = getTopListByCity(state,field,size, startTimestamp, endTimestamp)
    topLists = getBucketsFromResponse(response)

    topListsByCity[state] = topLists

  return topListsByCity


# Method:            getCulturesBySuburb
# Description:       Helper method for getting data related to a particular suburb like goejson and description fields. 
# Parameters:        countryOfBirthBySuburb (Json object) -> A large object containing all countries of birth per suburb
#                    suburbCode (String)                  -> a particular suburb you want to retrieve
# Output:            a json object containing all data related to the suburb you were looking for
def getCulturesBySuburb(countryOfBirthBySuburb,suburbCode):

    if countryOfBirthBySuburb:
        for crs in countryOfBirthBySuburb["features"]:
            suburb = crs["properties"]["feature_code"]
            if suburb == suburbCode:
                return crs["properties"]["country_of_birth"]
    else:
        return None

# Method:           mergeTweetsLanguages
# Description:      Merge languages defined on the languages database and the ones found on the cultures database.
#                   This method allow us to build a relationship between tweets and census data as well.
# Parameters:       languagesOfTweets,languagesOfCountries,cultures
# Output:           mergedCountedList (Json object containing a table of tweets and languages by suburb)
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


# Method:           isInMergedList
# Description:      Helper method. Check whether there is a language on the mergedList or not  
def isInMergedList(mergedList,language):

    for cob in mergedList:
        for lan in cob["languages"]:
            if lan == language:
                return cob["id"]
    return False

# Method:           getListLanguages
# Description:      Helper method. Get a list of languages found on the languagesOfCountries json object
def getListLanguages(languagesOfCountries,id):
    for cob in languagesOfCountries:
        if cob["id"] == id:
            return cob["languages"]


# Method:           getCountLanguages
# Description:      Helper method. Get a count of languages found on the languagesOfTweets json object    
def getCountLanguages(languagesOfTweets,id):
    for lan in languagesOfTweets:
        if lan == id:
            return int(languagesOfTweets[lan])

# Method:           getSuburbCodesFromGeoJson
# Description:      Helper method. Get suburb codes defined on the geojsonSuburbsStr json bsed string object.
def getSuburbCodesFromGeoJson(geojsonSuburbsStr):

  geojsonSuburbs = json.loads(geojsonSuburbsStr)
  suburbList = {}

  for feature in geojsonSuburbs["features"]:
    code = feature["properties"]["feature_code"]
    name = feature["properties"]["feature_name"]

    suburbList[code] = name

  return suburbList

# Method:           getTweetsByCountryOfBirth
# Description:      Get the count of tweets grouped by language as defined on the languages database
# Parameters:       term        (String)  -> Text you want to search for. i.e. AFL or Tony Abbott or *
#                   stateCode   (String)  -> the code of the state: i.e: VIC, TAS, etc
#                   suburbCode  (String)  -> Suburb code. i.e. 206041122
#                   startTimestamp   (Int)     -> Timestamp start date. i.e 1428069500339
#                   endTimestamp     (Int)     -> Timestamp end date i.e 1430578700339
# Output:           a json object containing the matched results
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


# Method:           getAllSentimentByCity
# Description:       Get the total sentiment by City, by term within a date range.
# Disclaimer:        This search takes a long time. Must be reviewed.
# Parameters:        term        (String)  -> Text you want to search for. i.e. AFL or Tony Abbott or *
#                   stateCode   (String)  -> the code of the state: i.e: VIC, TAS, etc
#                   startTimestamp   (Int)     -> Timestamp start date. i.e 1428069500339
#                   endTimestamp     (Int)     -> Timestamp end date i.e 1430578700339
# Output:            a json object containing the matched results
def getAllSentimentByCity(term,stateCode, startTimestamp, endTimestamp):

  geojsonSuburbsStr = json.dumps(getCulturesByState(stateCode), indent=4)

  suburbList = getSuburbCodesFromGeoJson(geojsonSuburbsStr)

  response = {}

  for suburb in suburbList:
    stats = statisticsByTerm(term, suburb, startTimestamp, endTimestamp)

    response[suburb] = stats
    response[suburb]["suburb_name"] = suburbList[suburb]

  return response
