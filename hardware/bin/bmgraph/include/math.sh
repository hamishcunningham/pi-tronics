#!/bin/bash

function mean {
    SUM=0
    for v in $@
    do
        SUM=`echo $SUM + $v | bc -l`
    done
    echo `echo $SUM / $# | bc -l`
}

function min {
    MIN=9999
    for v in $@
    do
        r=`echo $v \< $MIN | bc -l`
        if [ $r == 1 ]
        then
            MIN=$v
        fi
    done
    echo $MIN
}

function max {
    MAX=0
    for v in $@
    do
        r=`echo $v \> $MAX | bc -l`
        if [ $r == 1 ]
        then
            MAX=$v
        fi
    done
    echo $MAX
}

function multiply {
    RET=1
    for v in $@
    do
        RET=`echo $RET \* $v | bc -l`
    done
    echo $RET
}

function minus {
    RET=$1
    shift
    for v in $@
    do
        RET=`echo $RET - $v | bc -l`
    done
    echo $RET
}

function divide {
    RET=$1
    shift
    for v in $@
    do
        RET=`echo $RET / $v | bc -l`
    done
    echo $RET
}

function add {
    RET=$1
    shift
    for v in $@
    do
        RET=`echo $RET + $v | bc -l`
    done
    echo $RET
}
