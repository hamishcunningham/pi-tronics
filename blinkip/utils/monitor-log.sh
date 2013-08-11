#!/usr/bin/env bash
# monitor-log.sh -- grep blinkip syslog entries

while :
do
  clear
  grep blinkip /var/log/syslog |tail -20
  sleep 2
done
