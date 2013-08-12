#!/bin/bash

# script to compare benchmark results
# requires gnuplot and bc

# benchmark log files for comparison, one run of dobm.sh per log file
LOGFILES=(
    '../bm/bm.log'
)

# the different graph types to plot
GRAPHS=(
    'network_graph.sh'
    'disk_cache.sh'
    'disk_read.sh'
    'dhry_mips.sh'
    'whet_mflops.sh'
    'bzip2_min.sh'
    'lame_min.sh'
)

# graph dimensions
WIDTH=600
HEIGHT=300

# destination folder for graphs
OUTDIR='graphs'

# program start!
source include/math.sh
for GRAPH in ${GRAPHS[@]}
do
    GRAPHFILE=`echo $GRAPH | sed -e 's/\..*//'`
    echo -n "" > bm.dat
    for LOGFILE in ${LOGFILES[@]}
    do
        SLF=`echo $LOGFILE | sed -e 's/[^\/]*\///'`
        SLF=`echo $SLF | sed -e 's/\..*//'`

        source include/$GRAPH

        Me=`mean $VALUES`
        Mi=`min $VALUES`
        Ma=`max $VALUES`
        echo "$SLF $Me $Mi $Ma" >> bm.dat
    done

    XMAX=`minus ${#LOGFILES[@]} 0.5`
    cat barchart.tpl | sed -e "s/%xmax%/$XMAX/" | sed -e "s/%label%/$LABEL/" | sed -e "s/%data%/bm.dat/" | \
        sed -e "s/%width%/$WIDTH/" | sed -e "s/%height%/$HEIGHT/" > graph.gpl
    gnuplot graph.gpl
    sed "5 s/width=\"$HEIGHT\" height=\"$WIDTH\"/width=\"$WIDTH\" height=\"$HEIGHT\"/" graph.svg | \
        sed -e "s/0 0 $HEIGHT $WIDTH/-$WIDTH 0 $WIDTH $HEIGHT/" | sed -e 's/vas"/vas" transform="rotate(90 0 0)" /' > t.svg
    mv t.svg $OUTDIR/$GRAPHFILE.svg
    
done

rm graph.gpl graph.svg bm.dat
