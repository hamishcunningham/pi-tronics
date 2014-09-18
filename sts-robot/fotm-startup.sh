#!/usr/bin/env bash
#service simbamond restart -d
service simbamond stop
cd /home/pi/robot/
while [ 1 ]; do
  python fotm.py;
  if [ -f /home/pi/stop-robot.txt ]
  then
    break
  fi
  sleep 1;
done
