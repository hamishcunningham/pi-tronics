#!/bin/bash

# needs Raspberry_Pi_Benchmarks.zip from http://www.raspberrypi.org/phpBB3/viewtopic.php?t=44080&p=374054
# specifically dhry.h dhry_2.c cpuidh.h cpuidc.c whets.c dhry_1.c

# iperf, hdparm, lame, bzip2 should also be installed

# also need a audiodump.wav file for the practical benchmarks

# and then of course configure the settings below...

# compiler options
CFLAGS="-march=native"
#CFLAGS="-march=armv6"
#CFLAGS="-march=armv6 -mfloat-abi=hard -mfpu=vfp"

# hard disk to benchmark
DRIVE="/dev/sdi"

# remote host running iperf -s for network benchmarking
REMOTE="192.168.1.64"

# log file of results
LOGFILE="bm.log"

# program start!
date | tee -a "$LOGFILE"

echo "Checking for executables..." | tee -a "$LOGFILE"
for exe in iperf hdparm lame bzip2
do
    which $exe 2>>"$LOGFILE" 1>>"$LOGFILE"
    if [ $? -ne 0 ]
    then
        echo "$exe not found!" | tee -a "$LOGFILE"
        exit 1
    fi
done

echo "Checking for datafiles..." | tee -a "$LOGFILE"
for fil in audiodump.wav dhry.h dhry_2.c cpuidh.h cpuidc.c whets.c dhry_1.c
do
    if [ ! -e $fil ]
    then
        echo "$fil not found!" | tee -a "$LOGFILE"
        exit 1
    fi
done

echo "Compiling benchmarks..." | tee -a "$LOGFILE"
gcc dhry_1.c dhry_2.c cpuidc.c -lm -lrt -O3 $CFLAGS -o dhry 2>>"$LOGFILE" 1>>"$LOGFILE"
gcc  whets.c cpuidc.c -lm -lrt -O3 $CFLAGS -o whet 2>>"$LOGFILE" 1>>"$LOGFILE"

if [ ! -x dhry ] || [ ! -x whet ]
then
    echo "Failed compiling!" | tee -a "$LOGFILE"
    exit 1
fi

echo "Starting benchmarks..." | tee -a "$LOGFILE"
echo ""

for C in 1 2 3
do
    echo "Benchmark trial $C..." | tee -a "$LOGFILE"

    echo " IO Networking $C..." | tee -a "$LOGFILE"
    iperf -c "$REMOTE" 2>>"$LOGFILE" 1>>"$LOGFILE"
    echo " IO HD $C..." | tee -a "$LOGFILE"
    hdparm -tT "$DRIVE" 2>>"$LOGFILE" 1>>"$LOGFILE"

    echo " Theoretical Dhrystone $C..." | tee -a "$LOGFILE"
    echo "" | ./dhry 2>>"$LOGFILE" 1>>"$LOGFILE"
    echo " Theoretical Whetsone $C..." | tee -a "$LOGFILE"
    echo "" | ./whet 2>>"$LOGFILE" 1>>"$LOGFILE"

    echo " Practical bzip2 $C..." | tee -a "$LOGFILE"
    echo 1 > /proc/sys/vm/drop_caches
    bash -c "time bzip2 -fk audiodump.wav" 2>>"$LOGFILE" 1>>"$LOGFILE"
    echo " Practical lame $C..." | tee -a "$LOGFILE"
    echo 1 > /proc/sys/vm/drop_caches
    bash -c "time lame -S audiodump.wav" 2>>"$LOGFILE" 1>>"$LOGFILE"

done

echo "Benchmarks complete." | tee -a "$LOGFILE"
date | tee -a "$LOGFILE"
# all done!
