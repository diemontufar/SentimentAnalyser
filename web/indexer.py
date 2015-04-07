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

#Count the number of ocurrences in a index based on a particular text
def simpleCount(query):
    num = es.count(index=es_index, q=query)
    print("The query is: " + query)
    counter = num['count']
    return counter

#Count the number of ocurrences in a index based on a json query
def customCount(jsonQuery, docType):
    num = es.count(index=es_index, doc_type=docType, body=jsonQuery)
    counter = num['count']
    return counter


# query = '{"query":{"filtered":{"query":{"match":{"text":{"query":"support","operator":"or"}}},"strategy":"query_first"}}}'
# print(customSearch(query,'tweet'))