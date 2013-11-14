#!/bin/bash
# get-bat-level.sh

# source the config
. /etc/default/simbamond

# current level; -1 means unset
BAT_LEVEL=-1

# helper to check the level
get-bat-level() {
  BAT_LEVEL_BASE2=`gpio read ${IO_A}``gpio read ${IO_B}``gpio read ${IO_C}`
  BAT_LEVEL=`echo "ibase=2;${BAT_LEVEL_BASE2}" |bc`
  echo ${BAT_LEVEL}
}

# get the level
get-bat-level
