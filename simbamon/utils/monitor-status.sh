#!/usr/bin/env bash
# monitor-status -- loop reading status

#!/usr/bin/env bash
#
# template.sh

# standard locals
alias cd='builtin cd'
P="$0"
USAGE="`basename ${P}` [-h(elp)] [-d(ebug)] [-s(leep) secs]"
DBG=:
OPTIONSTRING=hds:

# specific locals
SLEEP=3

# message & exit if exit num present
usage() { echo -e Usage: $USAGE; [ ! -z "$1" ] && exit $1; }

# process options
while getopts $OPTIONSTRING OPTION
do
  case $OPTION in
    h)  usage 0 ;;
    d)  DBG=echo ;;
    s)  SLEEP="${OPTARG}" ;;
    *)  usage 1 ;;
  esac
done 
shift `expr $OPTIND - 1`

# functions
do_date() {
  date "+%Y-%m-%d-%T" |tr '[A-Z]' '[a-z]' |sed 's,:,,g'
}
do_stat() {
  sudo mopicli -e | pr -t3 -w100
}

# main loop
NOW=`do_date`
clear
while :; do
  echo "MoPi status at `do_date`:"
  do_stat
  echo
  sleep $SLEEP
done |tee mopi-status-log-${NOW}.txt
