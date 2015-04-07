#!/bin/bash

log_file="/Users/diogonal/Documents/CRONTABS/log_replication.dat"

#Replicate victoria:
curl -X POST http://diogonal:dgl0588@localhost:5984/_replicate  -d '{"source":"http://node3:sentiment3@115.146.86.97:5984/victoria", "target":"http://diogonal:dgl0588@localhost:5984/victoria"}' -H "Content-Type: application/json"
#Replicate tasmania:
curl -X POST http://diogonal:dgl0588@localhost:5984/_replicate  -d '{"source":"http://node3:sentiment3@115.146.86.97:5984/tasmania", "target":"http://diogonal:dgl0588@localhost:5984/tasmania"}' -H "Content-Type: application/json"
curl -X POST http://diogonal:dgl0588@localhost:5984/_replicate  -d '{"source":"http://node1:sentiment1@115.146.87.52:5984/tasmania", "target":"http://diogonal:dgl0588@localhost:5984/tasmania"}' -H "Content-Type: application/json"
#Replicate nsw:
curl -X POST http://diogonal:dgl0588@localhost:5984/_replicate  -d '{"source":"http://node3:sentiment3@115.146.86.97:5984/nsw", "target":"http://diogonal:dgl0588@localhost:5984/nsw"}' -H "Content-Type: application/json"
#Replicate westernau:
curl -X POST http://diogonal:dgl0588@localhost:5984/_replicate  -d '{"source":"http://node3:sentiment3@115.146.86.97:5984/westernau1", "target":"http://diogonal:dgl0588@localhost:5984/westernau"}' -H "Content-Type: application/json"
curl -X POST http://diogonal:dgl0588@localhost:5984/_replicate  -d '{"source":"http://node4:sentiment4@115.146.86.45:5984/westernau2", "target":"http://diogonal:dgl0588@localhost:5984/westernau"}' -H "Content-Type: application/json"
#Replicate southau:
curl -X POST http://diogonal:dgl0588@localhost:5984/_replicate  -d '{"source":"http://node4:sentiment4@115.146.86.45:5984/southau", "target":"http://diogonal:dgl0588@localhost:5984/southau"}' -H "Content-Type: application/json"
#Replicate queensland:
curl -X POST http://diogonal:dgl0588@localhost:5984/_replicate  -d '{"source":"http://node4:sentiment4@115.146.86.45:5984/queensland", "target":"http://diogonal:dgl0588@localhost:5984/queensland"}' -H "Content-Type: application/json"
#Replicate northernt:
curl -X POST http://diogonal:dgl0588@localhost:5984/_replicate  -d '{"source":"http://node4:sentiment4@115.146.86.45:5984/northernt", "target":"http://diogonal:dgl0588@localhost:5984/northernt"}' -H "Content-Type: application/json"
curl -X POST http://diogonal:dgl0588@localhost:5984/_replicate  -d '{"source":"http://node2:sentiment2@115.146.87.46:5984/northernt", "target":"http://diogonal:dgl0588@localhost:5984/northernt"}' -H "Content-Type: application/json"

/Users/diogonal/Documents/CRONTABS/reset_results.sh
current_date=$(date '+%d/%m/%Y %H:%M:%S');
echo "Replicated at: " $current_date >> "$log_file"