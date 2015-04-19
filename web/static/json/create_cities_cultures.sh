#!/bin/bash
curl -H 'Content-Type: application/json' -X POST http://diogonal:dgl0588@localhost:5984/cultures -d @melbourne.json
curl -H 'Content-Type: application/json' -X POST http://diogonal:dgl0588@localhost:5984/cultures -d @sydney.json
curl -H 'Content-Type: application/json' -X POST http://diogonal:dgl0588@localhost:5984/cultures -d @hobart.json
curl -H 'Content-Type: application/json' -X POST http://diogonal:dgl0588@localhost:5984/cultures -d @adelaide.json
curl -H 'Content-Type: application/json' -X POST http://diogonal:dgl0588@localhost:5984/cultures -d @darwin.json
curl -H 'Content-Type: application/json' -X POST http://diogonal:dgl0588@localhost:5984/cultures -d @perth.json
curl -H 'Content-Type: application/json' -X POST http://diogonal:dgl0588@localhost:5984/cultures -d @brisbane.json