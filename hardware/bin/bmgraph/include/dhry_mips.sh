#!/bin/bash

T=`cat $LOGFILE | grep "VAX"`
VALUES=`echo $T | sed -e 's/[A-Za-z= ]*\([0-9\.]*\)/\1 /g'`
UNITS="MIPS"
LABEL="Dhrystone ($UNITS)"
TITLE="Integer Math"