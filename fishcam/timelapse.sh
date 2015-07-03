#!/bin/bash
#
# timelapse.sh

# standard locals
alias cd='builtin cd'
P="$0"
USAGE="`basename ${P}` [-h(elp)] [-d(ebug)] [-n(no xyz)] [-i [1|2|3|...]"
DBG=:
OPTIONSTRING=hdni:

# specific locals
ABC=0
USEXYZ="1"
SLEEP=10
PICSDIR=/home/pi/pics

# message & exit if exit num present
usage() { echo -e Usage: $USAGE; [ ! -z "$1" ] && exit $1; }

# process options
while getopts $OPTIONSTRING OPTION
do
  case $OPTION in
    h)	usage 0 ;;
    d)	DBG=echo ;;
    n)	USEXYZ="" ;;
    i)	ABC="${OPTARG}" ;;
    *)	usage 1 ;;
  esac
done 
shift `expr $OPTIND - 1`

# take pics
picsloop() {
  while :
  do
    NOW=`date '+%Y-%m-%d--%T'|sed 's,:,-,g'`
    raspistill -t 1500 -o ${NOW}.jpg
    sleep $SLEEP
  done
}
[ -d $PICSDIR ] || mkdir -p $PICSDIR
cd $PICSDIR
picsloop
