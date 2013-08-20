#!/bin/bash

T=`cat "$LOGFILE" | grep "\[" | grep "/sec" | sed -e 's/.*ytes//'`
VALUES=`echo $T | sed -e 's/\([0-9\.]*\) \([A-Za-z]*\)\/sec/\1/g'`
UNITS=`echo $T | sed -e 's/\([0-9\.]*\) \([A-Za-z]*\).*\/sec/\2\/sec/'`
UNITS=`echo $UNITS | sed -e 's/\//\\\\\//'`
LABEL="Bandwidth ($UNITS)"
TITLE="Networking"
