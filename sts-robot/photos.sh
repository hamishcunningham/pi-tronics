#!/bin/bash
while true;
do
	raspistill -w 800 -h 600 -o test.jpg -n -t 1 -vf -hf
done
