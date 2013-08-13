#!/bin/bash

T=`cat $LOGFILE | grep "cached reads"`
VALUES=`echo $T | sed -e 's/[^=]*= \([0-9\.]*\) \([A-Za-z]*\)\/sec/\1 /g'`
UNITS=`echo $T | sed -e 's/[^=]*= \([0-9\.]*\) \([A-Za-z]*\).*\/sec/\2\/sec/'`
UNITS=`echo $UNITS | sed -e 's/\//\\\\\//'`
LABEL="Cached reads ($UNITS)"
TITLE="Disk Cache"