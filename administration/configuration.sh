#!/bin/bash

#masters
master_ip="115.146.86.249"
master_coucdb_user="master"
master_couchdb_pass="sentiment"
master_databases=australia

#harvesters
node1_ip="115.146.87.52"
node1_couchdb_user="node1"
node1_couchdb_pass="sentiment1"
node1_databases=tasmania

node2_ip="115.146.87.46"
node2_couchdb_user="node2"
node2_couchdb_pass="sentiment2"
node2_databases=northernt

node3_ip="115.146.86.97"
node3_couchdb_user="node3"
node3_couchdb_pass="sentiment3"
node3_databases=tasmania,nsw,victoria,westernau1

node4_ip="115.146.86.45"
node4_couchdb_user="node4"
node4_couchdb_pass="sentiment4"
node4_databases=queensland,northernt,westernau2,southau