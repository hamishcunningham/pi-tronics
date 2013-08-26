#!/usr/bin/env bash
# monitor-log.sh -- grep pi-cam syslog entries

while :
do
  clear
  grep pi-cam /var/log/syslog |tail -20
  sleep 2
done
