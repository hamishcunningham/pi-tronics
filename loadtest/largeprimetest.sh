#!/bin/bash
g++ -march=armv6 -mfloat-abi=hard -mfpu=vfp -O3 largeprime.cpp -o largeprime
while true;
do
	time ./largeprime
done
