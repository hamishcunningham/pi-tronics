#!/bin/bash

[ -z "$1" ] && { echo usage: $0 status-word; exit 1; }

cat << EOF
Bit values:
s_supply1_active()         # bit  0
s_supply2_active()         # bit  1
s_bat_full()               # bit  2
s_bat_good()               # bit  3
s_bat_low()                # bit  4
s_bat_critical()           # bit  5
s_jumper_on()              # bit  6
s_forced_shutdown()        # bit  7
s_power_on_delay_set()     # bit  8
s_power_on_delay_running() # bit  9
s_shutdown_delay_set()     # bit 10
s_shutdown_delay_running() # bit 11
s_check_supply1()          # bit 12
s_check_supply2()          # bit 13
s_user_configured()        # bit 14
s_unused()                 # bit 15
EOF
echo

for w in $*
do
  echo Status word " "$w is:
  echo "  bit key:   0123456789012345"
  echo -n "  binary:    "; echo "obase=2;$w;" |bc |rev
  echo -n "  hex:       "; echo "0x`echo "obase=16;$w" |bc`"
  echo
done
