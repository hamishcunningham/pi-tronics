#!/usr/bin/env bash
# monitor-log.sh -- grep simbamon syslog entries

tail -n 2000 -f /var/log/syslog | grep simbamon

#while :
#do
#  clear
#  grep simbamon /var/log/syslog |tail -20
#  sleep 2
#done
