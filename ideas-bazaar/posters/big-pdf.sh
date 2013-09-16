#!/usr/bin/env bash

pdfjoin --rotateoversize 'false' --outfile big.pdf url.pdf open-culture-tech-small.pdf schools.pdf pi-brush-code.pdf snowcam.pdf future-making.pdf your-project-here.pdf
shrinkpdf.sh big.pdf 256 big-small.pdf
mv big-small.pdf big.pdf
ls -lh big.pdf

#/usr/bin/pdfjam --fitpaper 'true' --rotateoversize 'true' --suffix joined --outfile big.pdf -- url.pdf - open-culture-tech-small.pdf - schools.pdf - pi-brush-code.pdf - snowcam.pdf - future-making.pdf - your-project-here.pdf -
