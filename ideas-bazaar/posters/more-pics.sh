#!/usr/bin/env bash

y=100
x=100

for f in basics.jpg blinkip.jpg chasing-pine-martens.jpg feed-me-seymour.jpg legocases.jpg mopi.jpg notipi.jpg pigs-and-pi.jpg schools.jpg sensing-and-responding.jpg snowcam.jpg stay-dry-cheaply.jpg
do
sed -e 's,__X__,'${x}',g' -e 's,__F__,'${f}',g' -e 's,__Y__,'${y}',g' << EOF
<image
  y="__Y__"
  x="__X__"
  id="image__X__"
  xlink:href="file:///home/hamish/export/__F__"
  height="200"
  width="200" />
EOF
  x=`expr $x + 100`
  y=`expr $y + 100`
done
