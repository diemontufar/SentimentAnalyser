#!/bin/bash

log_file="log_backup.dat"
current_date=$(date '+%d-%m-%Y-%H-%M-%S');

database="australia"
from_directory="/mnt/couchdb/$database"
to_directory="/mnt/backups"
directory="$to_directory/backup_$current_date"

mkdir "$directory"

echo "Proceeding to copy from: $from_directory to $directory"
cp from_directory directory