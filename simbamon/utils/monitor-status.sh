#!/usr/bin/env bash
# monitor-status -- loop reading status

do_stat() {
  sudo mopicli -e | pr -t3 -w100
}

clear
while :; do
  do_stat
  echo
  sleep 3
done
