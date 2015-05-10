#!/bin/bash

#########################################################################################################
#
# Author: 		Diego Montufar
# Date: 		Apr/2015
# Name: 		start_harvesting.sh
# Description: 	Executes multiple instances of the harvester_classifier.py program
#
# Execution:   	./start_harvesting.sh 
# By range:		./start_harvesting.sh 4 7
#
#########################################################################################################


initial_cuadrant="$1"
final_cuadrant="$2"

if [ $# -lt 2 ]
  then
    	for((i=1;i<=14;i++)); do nohup python harvester_classifier.py ${i} 2>1 & done
  else if [ $# -eq 2 ]
  	then
  		for((i=$initial_cuadrant;i<=$final_cuadrant;i++)); do nohup python harvester_classifier.py ${i} 2>1 & done
  	fi
fi