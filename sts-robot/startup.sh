#!/usr/bin/env bash
#service simbamond restart -d
service simbamond stop
cd /home/pi/robot/
while [ 1 ]; do python robot.py; done
