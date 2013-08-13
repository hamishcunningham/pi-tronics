#!/bin/bash

T=`cat $LOGFILE | grep "MWIPS"`
VALUES=`echo $T | sed -e 's/MWIPS[ ]*\([0-9\.]*\)[ ]*\([0-9\.]*\)/\1 /g'`
UNITS="MFLOPS"
LABEL="Whetstone ($UNITS)"
TITLE="Floating Point Math"