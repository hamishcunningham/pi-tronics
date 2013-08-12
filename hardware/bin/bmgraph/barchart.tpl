clear
reset
unset key
set boxwidth 1
set style histogram errorbars linewidth 1 gap 1.5
set style data histogram
set style fill solid 0.3
set autoscale y
set xrange [-0.5:%xmax%]
set boxwidth 1.3
set xtics rotate out
set bmargin 5.5
unset ytics
set y2tics rotate out offset -1
set y2label '%label%' offset -2.5
set terminal svg font "Bitstream Vera Sans, 12" linewidth 1 size %height%,%width%
set output 'graph.svg'

plot '%data%' using 2:3:4:xticlabels(1)
