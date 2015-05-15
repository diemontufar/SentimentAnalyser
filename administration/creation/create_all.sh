#!/bin/bash

echo 'Creating Databases...'
echo 'CREATE: cultures'
cultures/create_cities_couchdb.sh
echo
echo 'CREATE: suburbs'
suburbs/create_suburbs_couchdb.sh
echo
echo 'CREATE: languages'
languages/create_languages_couchdb.sh
echo
echo 'database creation finalized...'
