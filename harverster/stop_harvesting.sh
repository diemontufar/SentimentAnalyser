#!/bin/bash

for pid in $(ps -ef | grep "generic_harvester.py" | awk '{print $2}'); do kill -15 $pid; done