#!/bin/bash

DATABASE='cultures' 

curl -H 'Content-Type: application/json' -X POST http://localhost:5984/"$DATABASE" -d @cities/melbourne.json
curl -H 'Content-Type: application/json' -X POST http://localhost:5984/"$DATABASE" -d @cities/sydney.json
curl -H 'Content-Type: application/json' -X POST http://localhost:5984/"$DATABASE" -d @cities/hobart.json
curl -H 'Content-Type: application/json' -X POST http://localhost:5984/"$DATABASE" -d @cities/adelaide.json
curl -H 'Content-Type: application/json' -X POST http://localhost:5984/"$DATABASE" -d @cities/darwin.json
curl -H 'Content-Type: application/json' -X POST http://localhost:5984/"$DATABASE" -d @cities/perth.json
curl -H 'Content-Type: application/json' -X POST http://localhost:5984/"$DATABASE" -d @cities/brisbane.json