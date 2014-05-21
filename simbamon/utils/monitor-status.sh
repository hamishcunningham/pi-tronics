#!/usr/bin/env bash
# monitor-status -- loop reading status

do_stat() {
  sudo mopicli -e | pr -t3 -w100
}

NOW=`date "+%Y-%m-%d-%T" |tr '[A-Z]' '[a-z]' |sed 's,:,,g'`

clear
while :; do
  do_stat
  echo
  sleep 3
done |tee mopi-status-log-${NOW}.txt
