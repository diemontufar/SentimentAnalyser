#!/bin/bash

DATABASE='languages' 

curl -H 'Content-Type: application/json' -X POST http://localhost:5984/"$DATABASE" -d @languages.json