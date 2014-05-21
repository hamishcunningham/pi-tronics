#!/usr/bin/env bash
# monitor-status -- loop reading status

do_date() {
  date "+%Y-%m-%d-%T" |tr '[A-Z]' '[a-z]' |sed 's,:,,g'
}
do_stat() {
  sudo mopicli -e | pr -t3 -w100
}

NOW=`do_date`

clear
while :; do
  echo "MoPi status at `do_date`:"
  do_stat
  echo
  sleep 3
done |tee mopi-status-log-${NOW}.txt
