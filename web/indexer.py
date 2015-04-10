import elasticsearch
import json

es = elasticsearch.Elasticsearch()  # use default of localhost, port 9200
es_index = 'twitterall_2'

#Perform a search in a index based on a particular text
def simpleSearch(query):
    matches = es.search(index=es_index, q=query)
    #hits = matches['hits']['hits']
    return json.dumps(matches, indent=4) 

#Perform a search in a index based on a custom json query
def customSearch(jsonQuery, docType):
    matches = es.search(index=es_index, doc_type=docType, body=jsonQuery)
    return json.dumps(matches, indent=4) 

#Count the number of ocurrences in a index based on a json query
def count(jsonQuery, docType):
    num = es.count(index=es_index, doc_type=docType, body=jsonQuery)
    counter = num['count']
    return int(counter)

#TODO: this must be dynamic!!!!
def getRegions():
    return '"regions":{"NSW":{"name":"NewSouthWales","sentiment":"positive","positive":123,"neutral":15,"negative":65},"NT":{"name":"NorthernTerritory","sentiment":"positive","positive":456,"neutral":156,"negative":46},"QLD":{"name":"Queensland","sentiment":"negative","positive":25,"neutral":133,"negative":250},"SA":{"name":"SouthAustralia","sentiment":"negative","positive":12,"neutral":45,"negative":90},"TAS":{"name":"Tasmania","sentiment":"neutral","positive":123,"neutral":247,"negative":39},"VIC":{"name":"Victoria","sentiment":"positive","positive":421,"neutral":9,"negative":117},"WA":{"name":"WesternAustralia","sentiment":"negative","positive":50,"neutral":34,"negative":129}'

#Specific Web services
# def tweetsByTerm(jsonQuery, docType):
#     matches = es.search(index=es_index, doc_type=docType, body=jsonQuery)
#     return json.dumps(matches, indent=4) 

def statisticsByTerm(jsonQuery, docType):
    # matches = es.search(index=es_index, doc_type=docType, body=jsonQuery)
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

    # print("Total: ", total)
    # print("Mean: ", mean_sentiment)
    # print("Positive: ", total_positive)
    # print("Negative: ", total_negative)
    # print("Neutral: ", total_neutral)

    result = '{"results":{"total_tweets": %i, "mean_sentiment":\"%s\", "total_positive": %i, "total_neutral": %i, "total_negative": %i,%s}}}' % (total,mean_sentiment,total_positive,total_neutral,total_negative,regions) 

    return json.dumps(result, indent=4) 



# query = '{"query":{"filtered":{"query":{"match":{"text":{"query":"support","operator":"or"}}},"strategy":"query_first"}}}'
# query = '{"query": {"filtered": {"query": {"match": {"text": {"query": "shit","operator": "or"}}},"filter": {"term": {"lang": "en"}}}}}'
# # print(statisticsByTerm(query,'tweet'))
# statisticsByTerm(query,'tweet')