#!/usr/bin/env bash
# testing cleanup stuff

# cleanup function to run on termination, and a trap to trigger it
clean-up() {
  # kill any child processes (the list includes the ps process, so we discard
  # the "no such process" message)
  CHILDREN=`ps -T -o pid --no-headers --ppid $$`
  echo killing $CHILDREN
  [ ! -z "$CHILDREN" ] && kill -9 $CHILDREN 2>/dev/null
}
trap clean-up EXIT

sleep 100 &
echo sleep PID = $!

# uncomment demonstrate that it works on normal exit
sleep 1;exit 0

# demonstrate that it works on Cntrl&C
while :
do
  :
  sleep 1
done
