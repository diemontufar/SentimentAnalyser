#!/bin/bash

INDEX_CONFIG_PATH="json/twitter_index_config.json"
RIVER_PATH="json/twitter_river_config.json"
INDEX_NAME="twitterall_2"

#Create Index
echo "Creating Index: $INDEX_NAME ..."
curl -XPOST "localhost:9200/$INDEX_NAME" -d "@$INDEX_CONFIG_PATH"

#Create River-CouchDB
echo "Creating River-CouchDB..."
curl -XPUT "localhost:9200/_river/$INDEX_NAME/_meta" -d "@$RIVER_PATH"