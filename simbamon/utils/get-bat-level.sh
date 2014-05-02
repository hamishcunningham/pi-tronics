#!/bin/bash
# get-bat-level.sh

# source the config
. /etc/default/simbamond

# current level; -1 means unset
BAT_LEVEL=-1

CLI=../mopicli

STATUS=`sudo ${CLI} -s`
echo 'status is ${STATUS}'

for i in {1..10}
do
  echo -en "${i} is "
  echo "obase=2;${i}" |bc
done

if [ $(( 2 & 130 )) -eq 2 ]; then echo hello; fi




exit 0

# which status bit stores level
BAT_LEVEL_BIT=

# helper to check the level
get-bat-level() {
  #BAT_LEVEL=`echo "ibase=2;${BAT_LEVEL_BASE2}" |bc`
  STATUS=`${CLI} -sv`
  case ${STATUS} in
    *Forced*shutdown*)  echo 1 ;;
    *Battery*critical*) echo 3 ;;
    *Battery*low*)      echo 4 ;;
    *)                  echo 7 ;;
}

# get the level
get-bat-level
