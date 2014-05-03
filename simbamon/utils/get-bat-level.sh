#!/bin/bash
# get-bat-level.sh

P="$0"
INST_DIR=`dirname ${P}`

# current level; -1 means unset
BAT_LEVEL=-1

# mopi command-line interface
CLI=${INST_DIR}/../mopicli

# get the config and status decoding functions
source ${INST_DIR}/../simbamond.default

# read the status
STATUS=`sudo ${CLI} -s`
#VSTATUS="`sudo ${CLI} -sv |tr '\n' 'X' |sed 's,X,; ,g'`"
VSTATUS=`sudo ${CLI} -sv`
#echo "status is ${STATUS} ( `echo \"obase=2;${STATUS}\" |bc`; ${VSTATUS})"
echo "Status is ${STATUS} ( `echo \"obase=2;${STATUS}\" |bc` )"
echo $VSTATUS

# get the level
s_battery_full     $STATUS && echo battery_full
s_battery_good     $STATUS && echo battery_good
s_battery_low      $STATUS && echo battery_low
s_battery_critical $STATUS && echo battery_critical
