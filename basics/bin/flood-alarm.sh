#!/usr/bin/env bash
# flood-alarm.sh

# standard locals
alias cd='builtin cd'
P="$0"
USAGE="`basename ${P}` [-h(elp)] [-w(et)] [-d(ry)]\n
\twet and dry are for testing; normally we are run without options\n
\tand loop forever waiting for state changes on GPIO 2..."
OPTIONSTRING=hwd

# specific locals
WET=0
DRY=0
STATUS=none
pdate() { date '+%b %d %Y %T'; }

# message & exit if exit num present
usage() { echo -e Usage: $USAGE; [ ! -z "$1" ] && exit $1; }

# process options
while getopts $OPTIONSTRING OPTION
do
  case $OPTION in
    h)	usage 0 ;;
    d)	DRY=1; WET=0 ;;
    w)	WET=1; DRY=0 ;;
    *)	usage 1 ;;
  esac
done 
shift `expr $OPTIND - 1`

# get started
echo
echo ========================================================================
echo Hello! no flooding today, we hope...
pdate
echo

# set up the gpio pins
gpio mode 0 out # pin 0 is the buzzer and red led
gpio mode 1 out # pin 1 is the green led
gpio mode 2 in  # pin 2 is the water sensing circuit

# helpers for processing state changes
statusDry() {
  if [ $STATUS == wet ]
  then
    echo Becoming dry at `pdate`...
  else
    echo Staying dry at `pdate`...
  fi
  STATUS=dry
  gpio write 0 0
  gpio write 1 1
}
statusWet() {
  if [ $STATUS == dry ]
  then
    echo Eek! Becoming wet! `pdate`
  else
    echo Bugger. Staying wet! `pdate`
  fi
  STATUS=wet
  gpio write 0 1
  gpio write 1 0
}

# helper to send notifications when wetness persists
notifyFlooding() {
  DATE_TIME=`date '+%b %d %Y %T'`

  # send an SMS over the net
  PW=`cat flood-alarm-data-secure-store/bulksms.txt`
  SMS_STATUS=`./hc-sendbulksms.sh -u hcunningham \
    -p "${PW}" -n 447712341234 -m "Flooding in the basement? $DATE_TIME"`
  echo "BulkSMS says: ${SMS_STATUS}"

  # we could also use our NotiPi code here to send an SMS over the phone...
}

# either do a state change (for debugging), or loop
if [ $DRY == 1 ]
then
  statusDry
elif [ $WET == 1 ]
then
  statusWet
else
  # after an alarm wait at least 30 mins before re-testing
  MIN_DELAY=30
  DELAY=${MIN_DELAY}
  while :
  do
    WET=`gpio read 2`
    if [ $WET == 0 ]
    then
      statusDry
      DELAY=${MIN_DELAY}
      sleep 1
    else
      # wait a little and test again, just to be sure
      sleep 3
      WET=`gpio read 2`
      [ $WET == 0 ] && echo 'Hmmm... false alarm!' && statusDry && continue
      
      # raise the alarm
      statusWet
      notifyFlooding
      echo Taking a break for ${DELAY} minutes...
      sleep ${DELAY}m

      # if it is still wet we want to sleep longer next time
      DELAY=`expr 2 \* ${DELAY}`
      if [ $DELAY -gt 1440 ] 
      then
        # max delay is 24 hours
        DELAY=1440
      fi
    fi
  done
fi
