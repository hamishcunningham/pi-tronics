#!/bin/bash

#INDIR=/media/hamish/75d760c8-f766-4ba0-ae9f-cc870d6d11b9/fishy-backup/fishpics
INDIR=/home/hamish/fishpics
OUTDIR=/home/hamish/aquaponics-video/greenhouse-footage
IN=/tmp/$$.in

domerge() {
  ffmpeg -f concat -i $IN -c copy $1
}
dospeedy() {
  ffmpeg -i $1 -r 25 -filter:v "setpts=(1/8)*PTS" $2
}

cd $INDIR

# cam 1
>$IN
for f in \
f1/2015-11-20/vid-19-04-50.mp4 f1/2015-11-21/vid-23-02-56.mp4 f1/2015-11-22/vid-22-10-39.mp4 f1/2015-11-27/vid-17-40-22.mp4
do
  echo "file '${INDIR}/${f}'" >>$IN
done
domerge $OUTDIR/cam1.mp4
dospeedy $OUTDIR/cam1.mp4 $OUTDIR/cam1-fast.mp4

# cam 2
>$IN
for f in \
f2/2015-11-20/vid-19-08-55.mp4 f2/2015-11-21/vid-23-12-29.mp4 f2/2015-11-22/vid-22-21-02.mp4 f2/2015-11-27/vid-17-45-42.mp4
do
  echo "file '${INDIR}/${f}'" >>$IN
done
domerge $OUTDIR/cam2.mp4
dospeedy $OUTDIR/cam2.mp4 $OUTDIR/cam2-fast.mp4

# cam 3
>$IN
for f in \
f3/2015-11-20/vid-19-12-50.mp4 f3/2015-11-21/vid-23-21-37.mp4 f3/2015-11-22/vid-22-29-14.mp4 f3/2015-11-27/vid-17-50-58.mp4
do
  echo "file '${INDIR}/${f}'" >>$IN
done
domerge $OUTDIR/cam3.mp4
dospeedy $OUTDIR/cam3.mp4 $OUTDIR/cam3-fast.mp4

# composite
echo "file '$OUTDIR/cam1-fast.mp4'" > $IN
echo "file '$OUTDIR/cam2-fast.mp4'" >>$IN
echo "file '$OUTDIR/cam3-fast.mp4'" >>$IN
ffmpeg -f concat -i $IN -c copy $OUTDIR/all-fast.mp4

rm $IN
