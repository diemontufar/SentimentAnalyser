#!/bin/bash

DATABASE='suburbs' 

curl -H 'Content-Type: application/json' -X POST http://localhost:5984/"$DATABASE" -d @suburbs.json