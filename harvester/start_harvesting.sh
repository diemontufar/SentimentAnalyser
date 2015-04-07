#!/bin/bash

initial_cuadrant="$1"
final_cuadrant="$2"

if [ $# -lt 2 ]
  then
    	for((i=1;i<=14;i++)); do nohup python generic_harvester.py ${i} 2>1 & done
  else if [ $# -eq 2 ]
  	then
  		for((i=$initial_cuadrant;i<=$final_cuadrant;i++)); do nohup python generic_harvester.py ${i} 2>1 & done
  	fi
fi