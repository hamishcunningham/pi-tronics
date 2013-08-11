#!/usr/bin/env bash
# monitor-log.sh -- grep simbamon syslog entries

while :
do
  clear
  grep simbamon /var/log/syslog |tail -20
  sleep 2
done
