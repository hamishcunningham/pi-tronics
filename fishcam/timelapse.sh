#!/bin/bash
#
# timelapse.sh

# standard locals
alias cd='builtin cd'
P="$0"
USAGE="`basename ${P}` [-h(elp)] [-d(ebug)] [-r(sync)] [-s(sh)] [-f[123]] [-u(pdate)]"
DBG=:
OPTIONSTRING=hdf:sru

# specific locals
CAM=
SLEEP=60
PICSDIR=/home/pi/pics
SIN=
SYNC=
UPDATE=
NUCIP=10.0.0.5

# logical name
ME=
case `hostname` in fishcam1) ME=f1 ;; fishcam2) ME=f2 ;; fishcam3) ME=f3 ;; esac
echo logical name: $ME
 
# message & exit if exit num present
usage() { echo -e Usage: $USAGE; [ ! -z "$1" ] && exit $1; }

# process options
while getopts $OPTIONSTRING OPTION
do
  case $OPTION in
    h)	usage 0 ;;
    d)	DBG=echo ;;
    f)	CAM="f${OPTARG}" ;;
    s)  SIN=yes ;;
    r)  SYNC=yes ;;
    u)  UPDATE=yes ;;
    *)	usage 1 ;;
  esac
done 
shift `expr $OPTIND - 1`

# take pics
picsloop() {
  # top level dir
  [ -d $PICSDIR ] || mkdir -p $PICSDIR
  cd $PICSDIR

  # subdir for each day
  TODAYDIR=`date '+%Y-%m-%d'`
  [ -d $TODAYDIR ] || mkdir -p $TODAYDIR

  # TODO make sure nuc copy of this dir is up to date
  echo rsync -av ${TODAYDIR}/ $NCUIP:$PICSDIR
  cd $TODAYDIR
pwd
exit

  # TODO
  # send text if can't ping NUCIP

  # loop forever taking pics
  while :
  do
    NOW=`date '+%T'|sed 's,:,-,g'`
    raspistill -t 1000 -o ${NOW}.jpg
    exiv2 -et ${NOW}.jpg        # extract thumbnail

    # TODO
    # sync to pi@hc-nuc after each pic, thumbnail first
    scp ${NOW}-thumb.jpg ${NUCIP}:fishpics/XXX/${TODAYDIR}

    sleep $SLEEP
  done

  # TODO
  # hamish-nuc serve thumbs page
}

# update and reboot the cameras
updatecams() {
  for cam in f1 f2 f3
  do
    CAM=$cam
    eval echo "\$$CAM" >/tmp/$$; IP=`cat /tmp/$$`; rm /tmp/$$
    ssh -i .ssh/pitronics_id_dsa pi@${IP} \
      'bash -c "hostname && cd pi-tronics && git pull && sudo reboot"'
  done
}

# create a vid
makevid() {
  # from http://www.raspberrypi-spy.co.uk/2013/05/creating-timelapse-videos-with-the-raspberry-pi-camera/
  avconv \
    -r 10 -i timelapse_%04d.jpg \
    -r 10 -vcodec libx264 -crf 20 -g 15 \
    -vf crop=2592:1458,scale=1280:720 \
  timelapse.mp4
  return 0

  # alternatives:

  # from http://www.instructables.com/id/Simple-timelapse-camera-using-Raspberry-Pi-and-a-c/?ALLSTEPS
  mencoder -nosound -ovc lavc -lavcopts \
    vcodec=mpeg4:aspect=16/9:vbitrate=8000000 -vf scale=1920:1080 \
    -o timelapse.avi -mf type=jpeg:fps=24 mf://@list.txt

  # from https://www.raspberrypi.org/learning/timelapse-setup/worksheet.md
  mencoder -nosound -ovc lavc -lavcopts \
    vcodec=mpeg4:aspect=16/9:vbitrate=8000000 \
    -vf scale=1920:1080 -o timelapse.avi -mf type=jpeg:fps=24 mf://@stills.txt

  # from http://blog.davidsingleton.org/raspberry-pi-timelapse-controller/
  # (also discusses exposure times and flicker at sunset)
  ffmpeg -r 18 -q:v 2 -start_number XXXX -i /tmp/timelapse/IMG_%d.JPG \
    output.mp4

  # from http://computers.tutsplus.com/tutorials/creating-time-lapse-photography-with-a-raspberry-pi--cms-20794
  mencoder -nosound -ovc lavc -lavcopts \
    vcodec=mpeg4:aspect=16/9:vbitrate=8000000 -vf scale=1920:1080 \
    -o timelapse.avi -mf type=jpeg:fps=24 mf://@stills.txt
}

# do summut
cd
if [ x$SIN = xyes -a x"$CAM" != x ]             # ssh into the cam
then
  eval echo "\$$CAM" >/tmp/$$; IP=`cat /tmp/$$`; rm /tmp/$$
  ssh -i .ssh/pitronics_id_dsa pi@${IP}
elif [ x$SYNC = xyes -a x"$CAM" != x ]          # rsync back to nuc
then
  eval echo "\$$CAM" >/tmp/$$; IP=`cat /tmp/$$`; rm /tmp/$$
  rsync -av -e "ssh -i .ssh/pitronics_id_dsa" pi@${IP}:pics/ fishpics/${CAM}-pics
elif [ x$UPDATE = xyes ]                        # update and reboor
then
  updatecams
else                                            # the default: take pics
  picsloop
fi
