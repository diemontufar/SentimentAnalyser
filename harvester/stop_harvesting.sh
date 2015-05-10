#!/bin/bash

#########################################################################################################
#
# Author: 			Diego Montufar
# Date: 			Apr/2015
# Name: 			stop_harvesting.sh
# Description: 		Stops all the current running instances of the harvester_classifier.py program
#
# Execution:   		./stop_harvesting.sh 
#
#########################################################################################################

for pid in $(ps -ef | grep "harvester_classifier.py" | awk '{print $2}'); do kill -15 $pid; done