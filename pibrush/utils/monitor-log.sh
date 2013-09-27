#!/usr/bin/env bash
# monitor-log.sh -- grep pibrush syslog entries

while :
do
  clear
  grep pibrush /var/log/syslog |tail -20
  sleep 2
done
