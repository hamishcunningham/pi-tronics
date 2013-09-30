#!/bin/bash

sudo amixer cset numid=3 1
gpio mode 8 up

while :
do
  if [ `gpio read 8` = 0 ]
  then
    echo "time to sing!" 
    aplay police.wav &
  fi

  echo "time to sleep..."
  sleep 1
done
