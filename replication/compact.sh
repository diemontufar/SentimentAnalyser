#!/bin/bash

log_file="/Users/diogonal/Documents/CRONTABS/log_compaction.dat"

#Compact victoria:
curl -H "Content-Type: application/json" -X POST http://node3:sentiment3@115.146.86.97:5984/victoria/_compact
#Compact tasmania:
curl -H "Content-Type: application/json" -X POST http://node3:sentiment3@115.146.86.97:5984/tasmania/_compact
curl -H "Content-Type: application/json" -X POST http://node1:sentiment1@115.146.87.52:5984/tasmania/_compact
#Compact nsw:
curl -H "Content-Type: application/json" -X POST http://node3:sentiment3@115.146.86.97:5984/nsw/_compact
#Compact westernau:
curl -H "Content-Type: application/json" -X POST http://node3:sentiment3@115.146.86.97:5984/westernau1/_compact
curl -H "Content-Type: application/json" -X POST http://node4:sentiment4@115.146.86.45:5984/westernau2/_compact
#Compact southau:
curl -H "Content-Type: application/json" -X POST http://node4:sentiment4@115.146.86.45:5984/southau/_compact
#Compact queensland:
curl -H "Content-Type: application/json" -X POST http://node4:sentiment4@115.146.86.45:5984/queensland/_compact
#COmpact northernt:
curl -H "Content-Type: application/json" -X POST http://node4:sentiment4@115.146.86.45:5984/northernt/_compact
curl -H "Content-Type: application/json" -X POST http://node2:sentiment2@115.146.87.46:5984/northernt/_compact

current_date=$(date '+%d/%m/%Y %H:%M:%S');
echo "Compacted at: " $current_date >> "$log_file"