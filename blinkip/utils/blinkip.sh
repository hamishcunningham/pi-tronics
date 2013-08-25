#!/bin/bash
# blinkip.sh -- blink our IP address

LED=/sys/class/leds/led0/brightness
MYIP=`ifconfig |grep -v 127.0.0.1 |grep 'addr:' | \
  sed -e 's,.*addr:,,' -e 's, .*,,' |sed 's,\., ,g'`
#LOG=echo
LOG=:
NAME=$0

if [ -z "$MYIP" ]
then
  echo $0: failed to find my IP address, giving up
  exit 1
fi

bright() { echo 1 >$LED; }
dark()   { echo 0 >$LED; }
pause() { dark; sleep 2.5; }
shortpause() { dark; sleep 1; }
rapid()  {
  i=0
  while [ $i -lt 15 ]
  do
    bright; sleep 0.05; dark; sleep 0.05
    i=`expr $i + 1`
  done
}
showdigit() {
  d=$1
  [ $d = 0 ] && d=10
  for((b=0; b<$d; b++))
  do
    $LOG $NAME: showing digit $d
    bright; sleep 0.3; dark; sleep 0.4
  done
}
blink() {
  # blink rapidly to start with
  $LOG $NAME: preparing to blink $MYIP
  rapid; rapid

  # cycle through each address block
  for block in $1 $2 $3 $4
  do
    $LOG $NAME: doing block $block

    numdigits=${#block}
    for ((i=0; i < $numdigits; i++))
    do
      pause
      showdigit ${block:$i:1}
    done

    shortpause; rapid
    shift
  done

  $LOG $NAME: done $MYIP
}
blink $MYIP
