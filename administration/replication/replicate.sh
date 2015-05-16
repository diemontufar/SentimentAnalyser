#!/bin/bash

log_file="log_replication.dat"

echo "Reading config...." >&2
source ../configuration.sh

echo
echo "Replicating from: $node1_databases to master_databases ..."
curl -X POST http://"$master_coucdb_user":"$master_couchdb_pass"@"$master_ip":5984/_replicate  -d '{"source":"http://'"$node1_couchdb_user:$node1_couchdb_pass@$node1_ip:5984/$node1_databases"'", "target":"http://'"$master_coucdb_user:$master_couchdb_pass@$master_ip:5984/$master_databases"'" , "continuous":true}' -H "Content-Type: application/json"
echo "Replicating from: $node2_databases to master_databases ..."
curl -X POST http://"$master_coucdb_user":"$master_couchdb_pass"@"$master_ip":5984/_replicate  -d '{"source":"http://'"$node2_couchdb_user:$node2_couchdb_pass@$node2_ip:5984/$node2_databases"'", "target":"http://'"$master_coucdb_user:$master_couchdb_pass@$master_ip:5984/$master_databases"'" , "continuous":true}' -H "Content-Type: application/json"

for database3 in $(echo $node3_databases | tr "," "\n")
do
    echo "Replicating from: $database3 to master_databases ..."
    curl -X POST http://"$master_coucdb_user":"$master_couchdb_pass"@"$master_ip":5984/_replicate  -d '{"source":"http://'"$node3_couchdb_user:$node3_couchdb_pass@$node3_ip:5984/$database3"'", "target":"http://'"$master_coucdb_user:$master_couchdb_pass@$master_ip:5984/$master_databases"'" , "continuous":true}' -H "Content-Type: application/json"
done

for database4 in $(echo $node4_databases | tr "," "\n")
do
    echo "Replicating from: $database4 to master_databases ..."
    curl -X POST http://"$master_coucdb_user":"$master_couchdb_pass"@"$master_ip":5984/_replicate  -d '{"source":"http://'"$node4_couchdb_user:$node4_couchdb_pass@$node4_ip:5984/$database4"'", "target":"http://'"$master_coucdb_user:$master_couchdb_pass@$master_ip:5984/$master_databases"'" , "continuous":true}' -H "Content-Type: application/json"
done

./reset_results.sh
current_date=$(date '+%d/%m/%Y %H:%M:%S');
echo "Replicated at: " $current_date >> "$log_file"


