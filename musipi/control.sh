#!/bin/bash
# control a music pi using mpc

# turn me off with the -c option
[ x"$1" == x-c ] && {
  echo killalling control.sh
  killall control.sh
  exit 0
}

# command paths
GPIO=/usr/local/bin/gpio
MPC=/usr/bin/mpc

# set up the button press indicator LED
$GPIO mode 7 out
$GPIO write 7 0

# default output volume
$MPC volume 80

# functions that get triggered by button presses
control-func-4() { $MPC toggle; }
control-func-3() { $MPC prev; }
control-func-2() { $MPC next; }
control-func-1() { $MPC volume -5; }
control-func-0() { $MPC volume +5; }

# for each button press sensor pin:
#   set up the pin
#   background a function to:
#     wait for input on that pin, then:
#     flash the button press indicator LED
#     trigger the appropriate control function
for pin in 0 1 2 3 4
do
  $GPIO mode $pin up
  eval \
   "wfi-func-${pin}() {
      while :; do
        $GPIO wfi ${pin} rising;
        ( $GPIO write 7 1; sleep 0.5; $GPIO write 7 0; )&
        control-func-${pin}
      done;
    }"
  wfi-func-${pin} &
done

# start playing (on repeat)
$MPC play
$MPC repeat
