Indexer Module
===================

- - - - 

This module is related to the Elasticsearch idexing process. Prior to the index creation, it is necessary to permorm two main configurations:

1. Configure Mappings
2. Create Index
3. Configure Coucdb-river

- - - -

## 1. Configure Mappings

>"Mapping is the process of defining how a document should be mapped to the Search Engine, including its searchable characteristics such as which fields are searchable and if/how they are tokenized. In Elasticsearch, an index may store documents of different mapping types". 

Elasticsearch allows one to associate multiple mapping definitions for each mapping type. This process can be omitted as ES takes care of it automatically by detecting mapping types during the indexing process. However, we may want to map certain fields to satisfy our needs depending on how we are going to analyse data in later stages.

The file json/twitter_index_config.json contains the basic mapping configurations for a typical tweet obtained from the Twitter API streaming services. In order to save storage, certain fields won't be indexed and some of them will be mapped with special mapping types such as geo_point and geo_polygon for location coordinates and some non-analysed fields in order to prevent text tokenization will be considered as well (i.e. Languages like en-US, en-AU shouldn't be tokenized).

Further information and references: [Mapping in ES](http://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html)

## 2. Create Index

Once we have defined the mapping types, we are ready to create the ES index. This process can be done by executing:

```sh
curl -XPOST "localhost:9200/$INDEX_NAME" -d @json/twitter_index_config.json
```
Where $INDEX_NAME should be he name of the index you want to create. The response should be:

```sh
{"ok":true,"acknowledged":true}
```

Further information: [Create Index ES](http://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html)

## 3. Configure Couchdb-river

One way to insert data into Elasticsearch is to use a service that fetches the data from an external source (one shot or periodically) and puts the data into the cluster. This sort of services are called Rivers and for this project's sake, we'll be interested in a couchdb-river.

### Installation

* Install River plugin (if it is not already done):
```sh
$ /usr/share/elasticsearch/bin/plugin install elasticsearch/elasticsearch-river-couchdb/2.5.0
```
Further information: [elasticsearch-couchdb-river](https://github.com/elastic/elasticsearch-river-couchdb/blob/master/README.md)

* Cofigure river:
```sh
$ curl -XPUT "localhost:9200/_river/$INDEX_NAME/_meta" -d @json/twitter_river_config.json
```
This call will create a river that uses the _changes stream to index all data within couchdb. Moreover, any "future" changes will automatically be indexed as well, making your search index and couchdb synchronized at all times. River configurations are defined on the  twitter_river_config.json file. The response should be:

```sh
{"ok":true,"_index":"_river","_type":" couchriver ","_id":"_
       meta","_version":1}
```

### Create and Configure: automatic option

Alternatively, a bash script which performs the steps mentioned above is provided. You may want to execute it instead of running each line by yourself. However, be aware that you must have installed the River pluging before executig this script.

```sh
$ ./configure_index.sh
```

### Response

If everithing was configured correctly, you may expect to see how the indexing process starts and documents are continously streamed from the couchdb database. It may take a while depending on the machine capabilities, cluster configuration and the amount of data to be indexed.

