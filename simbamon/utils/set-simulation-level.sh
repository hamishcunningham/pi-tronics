#!/usr/bin/env bash
# set-simulation-level.sh -- read and write battery level simulation values

while :
do
  echo -n 'level? '
  read LEVEL
  clear
  echo ${LEVEL} >/tmp/simbamon-simulation.txt
  echo -n 'level set to: '
  cat /tmp/simbamon-simulation.txt
  echo
done
