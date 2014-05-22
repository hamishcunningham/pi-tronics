#!/bin/bash

LOG_PATTERN='mopi-status-log-2014-05-22-*'
NORMAL_READING_PATTERN=4101

LOGS=`find . -name "${LOG_PATTERN}"`
ABNORMAL_LINES=`grep 'Status.word: ' $LOGS |grep -v ${NORMAL_READING_PATTERN}`
OIFS="$IFS"
IFS='
'
for l in ${ABNORMAL_LINES}
do
  IFS="$OIFS"
  set $l
  ABNORMAL_READINGS="$3 $ABNORMAL_READINGS"
done
IFS="$OIFS"

ABNORMAL_READINGS=`echo $ABNORMAL_READINGS |sed 's, ,\n,g' |sort |uniq`

for r in $ABNORMAL_READINGS
do
  echo Details for reading $r:
  echo 0123456789012345
  echo "obase=2;${r};" |bc |rev

  for f in $LOGS
  do
    set x `grep -n 'Status.word: '$r $f |sed 's,:, ,'`
    N=$2
    [ -z "$N" ] && continue
    START=`expr $N - 3`
    END=`expr $N + 3`
    echo
    sed -n "${START},${END}p" $f
  done
done
