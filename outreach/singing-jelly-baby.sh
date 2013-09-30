#!/bin/bash

gpio mode 8 up

while :
do
  if [ `gpio read 8` = 0 ]
  then
    echo "time to sing!" 
    aplay police_s.wav &
  fi

  echo "time to sleep..."
  sleep 2
done
