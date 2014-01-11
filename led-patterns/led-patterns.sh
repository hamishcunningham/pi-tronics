#!/usr/bin/env bash
#
# led-patterns.sh

# standard locals
alias cd='builtin cd'
P="$0"
USAGE="`basename ${P}` [-h(elp)] [-d(ebug)] [-o(ff)]"
DBG=:
OPTIONSTRING=hdo

# specific locals
TURNOFF=0
STOPFILE=${HOME}/.stop-led-patterns
G_RED=0
G_YELLOW=2
G_GREEN=3

# message & exit if exit num present
usage() { echo -e Usage: $USAGE; [ ! -z "$1" ] && exit $1; }

# process options
while getopts $OPTIONSTRING OPTION
do
  case $OPTION in
    h)	usage 0 ;;
    d)	DBG=echo ;;
    o)  TURNOFF=1 ;;
    *)	usage 1 ;;
  esac
done 
shift `expr $OPTIND - 1`

# stop requested?
[ ${TURNOFF} == 1 ] && { >${STOPFILE}; exit 0; }

# led switching functions
on-off() {
  if [ x$2 == xoff ]
  then
    gpio write $1 0
  else
    gpio write $1 1
  fi
}
red()     { on-off $G_RED    $1; }
yellow()  { on-off $G_YELLOW $1; }
green()   { on-off $G_GREEN  $1; }
all-on()  { red; yellow; green;  }
all-off() { red off; yellow off; green off;  }

# simulate gpio if not available
if [ x`which gpio` == x ]
then
  gpio() { echo $*; }
fi

# mail loop
while :
do
  [ -f ${STOPFILE} ] && { rm ${STOPFILE}; exit 0; }
  all-on
  sleep 1
  all-off
  sleep 1
done
