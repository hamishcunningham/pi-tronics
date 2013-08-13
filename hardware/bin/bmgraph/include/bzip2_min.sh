#!/bin/bash

T=`cat $LOGFILE | grep "real"`
VALUES2=`echo $T | sed -e 's/real \([0-9ms\.]*\)/\1 /g'`
IFS=' ' read -a VALUES2 <<< "$VALUES2"
VALUES=''
for C in $(seq 0 2 $[${#VALUES2[@]}-1])
do
    AT=${VALUES2[$C]}
    MIN=`echo $AT | sed -e 's/\([0-9]*\)m.*/\1/'`
    SEC=`echo $AT | sed -e 's/\([0-9]*\)m\([0-9\.]*\)s/\2/'`
    MIN=`add $MIN \`divide $SEC 60\``
    VALUES="$VALUES $MIN"
done

UNITS="minutes"
LABEL="Time ($UNITS)"
TITLE="Bzip2 Compression"