#!/bin/bash
#
# timelapse.sh

# When started on a cam with no options (typically via rc.local), this script
# updates the server with the latest pics then loops taking new pics every
# minute or so. The various options are for actions on the server. 

# TODO
# -p pause, with flashing LED

# standard locals
alias cd='builtin cd'
P="$0"
USAGE="`basename ${P}` [-h(elp)] [-d(ebug)] [-r(sync)] [-s(sh)] [-f[123]] \
[-u(pdate)] [-w(ebserve)] [-b(ackup)] [-S(top)] [-H(alt)] [-D(isk free)]\
[-m(ake vid) indir [outname]] [-C(lear cams)]"
DBG=:
OPTIONSTRING=hdf:sruwbSHmDC

# specific locals
CAM=
SLEEP=13
PICSDIR=/home/pi/pics
SIN=
SYNC=
UPDATE=
NUCIP=10.0.0.5
BACKUP=
WEBSERVE=
STOP=
HALT=
MAKEVID=
DF=
CLEAR=

# logical name
ME=
case `hostname` in fishcam1) ME=f1 ;; fishcam2) ME=f2 ;; fishcam3) ME=f3 ;; esac
 
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
    w)  WEBSERVE=yes ;;
    b)  BACKUP=yes ;;
    S)  STOP=yes ;;
    D)  DF=yes ;;
    C)  CLEAR=yes ;;
    H)  HALT=yes ;;
    m)  MAKEVID=yes ;;
    *)	usage 1 ;;
  esac
done 
shift `expr $OPTIND - 1`

# take pics
picsloop() {
  # not a camera?
  [ x$ME == x ] && { echo not a camera...; usage 2; }
  
  # initialise the LED pins
  /home/pi/wiringPi/gpio/gpio mode 0 out
  /home/pi/wiringPi/gpio/gpio mode 1 out
  redoff
  greenon

  # check server
  i=0
  while ! ping -c 1 $NUCIP
  do
    i=$((i + 1))
    echo "no server ping ($i)"
    greenoff
    redon
    sleep 5
  done
  redoff
  greenon

  # top level dir
  [ -d $PICSDIR ] || mkdir -p $PICSDIR
  cd $PICSDIR

  # subdir for each day
  TODAYDIR=`date '+%Y-%m-%d'`
  [ -d $TODAYDIR ] || mkdir -p $TODAYDIR

  # make sure nuc copy of this dir is up to date
  echo "rsync -av --size-only -e \"ssh -i /home/pi/.ssh/id_dsa\" \
    ${TODAYDIR} \"pi@${NUCIP}:fishpics/${ME}\""
  su pi -c "rsync -av --size-only -e \"ssh -i /home/pi/.ssh/id_dsa\" \
    ${TODAYDIR} \"pi@${NUCIP}:fishpics/${ME}\""

  # location for new pics; serve recent ones
  cd $TODAYDIR
  [ -f recent.html ] || >recent.html
  python -m SimpleHTTPServer &

  # loop forever taking pics
  while :
  do
    NOW=`date '+%T'|sed 's,:,-,g'`
    raspistill -t 1000 --thumb '320:240:70' -o ${NOW}.jpg
    exiv2 -et ${NOW}.jpg        # extract thumbnail
    mv ${NOW}-thumb.jpg .${NOW}-thumb.jpg

    # add to recent page
    head -2 recent.html >recent-tmp-$$
    echo "<p><a href='${NOW}.jpg'><img src='.${NOW}-thumb.jpg'/></a></p>" \
      >recent.html
    tac recent-tmp-$$ >>recent.html
    rm recent-tmp-$$

    # set LED red if can't ping NUCIP
    ping -c 1 $NUCIP || ( echo 'no server ping (loop 1)'; sleep 5; redon; \
      ping -c 1 $NUCIP || ( echo 'no server ping (loop 2)'; sleep 5; \
        ping -c 1 $NUCIP || ( echo 'no server ping (loop 3)'; sleep 5; \
          ping -c 1 $NUCIP || ( echo 'no server ping (loop 4)'; sleep 5; \
            ping -c 1 $NUCIP || ( greenoff; \
    )))))
    ping -c 1 $NUCIP && greenon && redoff

    # sync to pi@hc-nuc after each pic, thumbnail first
    echo "scp .${NOW}-thumb.jpg pi@${NUCIP}:fishpics/${ME}/${TODAYDIR}"
    su pi -c "scp .${NOW}-thumb.jpg pi@${NUCIP}:fishpics/${ME}/${TODAYDIR}"
    echo "scp ${NOW}.jpg pi@${NUCIP}:fishpics/${ME}/${TODAYDIR}"
    su pi -c "scp ${NOW}.jpg pi@${NUCIP}:fishpics/${ME}/${TODAYDIR}"

    # add to the index.html
    TMPF=tmp-`hostname`-$$
    echo "<p><a href='${NOW}.jpg'><img src='.${NOW}-thumb.jpg'/></a></p>" >$TMPF
    su pi -c "scp ${TMPF} pi@${NUCIP}:fishpics/${ME}/${TODAYDIR}"
    su pi -c "ssh pi@${NUCIP} 'cd fishpics/${ME}/${TODAYDIR} && \
      [ -f index.html ] || >index.html && \
      cat $TMPF index.html >$$ && mv $$ index.html && rm $TMPF'"
    rm $TMPF

    # wait for next scheduled pic
    sleep $SLEEP
  done
}

# serve the thumbnails
servehttp() {
  cd /home/hamish/fishpics
  echo '<ul>'   >index.html
  for d in `find . -type d`
  do
    echo '<li><a href='${d}'/>'${d}'/</a></li>'
  done          >>index.html
  echo '</ul>'  >>index.html
  python -m SimpleHTTPServer
}

# df on each cam
diskfree() {
  for cam in f1 f2 f3
  do
    CAM=$cam
    eval echo "\$$CAM" >/tmp/$$; IP=`cat /tmp/$$`; rm /tmp/$$
    AVAIL=`ssh -i .ssh/pitronics_id_dsa pi@${IP} \
      'set \`df -h |grep '/$'\`; echo $4'`
    echo "Disk usage on ${cam} (${AVAIL} available on /):"
    ssh -i .ssh/pitronics_id_dsa pi@${IP} 'bash -c "df -h"'
    echo
  done
}

# halt cameras
haltcams() {
  read -p "about to halt cams; are you sure? (y/N) " -n 1 -r; echo
  [[ $REPLY =~ ^[Yy]$ ]] || { echo "ok, giving up!"; return 1; }

  for cam in f1 f2 f3
  do
    CAM=$cam
    eval echo "\$$CAM" >/tmp/$$; IP=`cat /tmp/$$`; rm /tmp/$$
    ssh -i .ssh/pitronics_id_dsa pi@${IP} 'bash -c "sudo halt"'
  done
}

# clear cam disks
clearcams() {
  read -p "about to CLEAR cams; are you sure? (y/N) " -n 1 -r; echo
  [[ $REPLY =~ ^[Yy]$ ]] || { echo "ok, giving up!"; return 1; }
  for cam in f1 f2 f3
  do
    CAM=$cam
    eval echo "\$$CAM" >/tmp/$$; IP=`cat /tmp/$$`; rm /tmp/$$
    ssh -i .ssh/pitronics_id_dsa pi@${IP} \
      'bash -c "sudo rm -rf /home/pi/pics/*"'
  done
}

# stop taking pics
stopcams() {
  read -p "about to stop cams; are you sure? (y/N) " -n 1 -r; echo
  [[ $REPLY =~ ^[Yy]$ ]] || { echo "ok, giving up!"; return 1; }
  for cam in f1 f2 f3
  do
    CAM=$cam
    eval echo "\$$CAM" >/tmp/$$; IP=`cat /tmp/$$`; rm /tmp/$$
    ssh -i .ssh/pitronics_id_dsa pi@${IP} \
      'bash -c "sudo kill `pgrep timelapse.sh`"'
  done
}

# back up the server copy
makebackup() {
  rsync -av --size-only /home/pi/fishpics /home/hamish/Pictures
}

# update and reboot the cameras
updatecams() {
  read -p "about to update cams; are you sure? (y/N) " -n 1 -r; echo
  [[ $REPLY =~ ^[Yy]$ ]] || { echo "ok, giving up!"; return 1; }

  for cam in f1 f2 f3
  do
    CAM=$cam
    eval echo "\$$CAM" >/tmp/$$; IP=`cat /tmp/$$`; rm /tmp/$$
    ssh -i .ssh/pitronics_id_dsa pi@${IP} \
      'bash -c "hostname && cd pi-tronics && git pull && sudo reboot"'
  done
}

# LED control
greenon()  { /home/pi/wiringPi/gpio/gpio write 0 1; }
greenoff() { /home/pi/wiringPi/gpio/gpio write 0 0; }
redon()    { /home/pi/wiringPi/gpio/gpio write 1 1; }
redoff()   { /home/pi/wiringPi/gpio/gpio write 1 0; }

# create a vid
makevid() {
  # validate args and find inputs
  [ x$1 == x ] && { echo oops: wrong args to makevid: $1 $2; usage 3; }
  VIDFILE=
  [ x$2 == x ] && VIDFILE=vid.mp4
  [ -d $1 ] || { echo oops: $1 is not a directory; usage 4; }
  [ x${VIDFILE} == x ] && case "$2" in
    *.mp4) VIDFILE=$2 ;;
    *)     VIDFILE=$2.mp4 ;;
  esac
  cd $1
  echo creating video from `pwd` to ${VIDFILE} ...
  sleep 2

  # ffmpeg on all .jpg
  ffmpeg -pattern_type glob -i "*.jpg" $VIDFILE

  # all done
  return 0
}

# do summut
cd
if [ x$SIN              == xyes -a x"$CAM" != x ]       # ssh into the cam
then
  eval echo "\$$CAM" >/tmp/$$; IP=`cat /tmp/$$`; rm /tmp/$$
  ssh -i .ssh/pitronics_id_dsa pi@${IP}
elif [ x$SYNC           == xyes -a x"$CAM" != x ]       # rsync back to nuc
then
  eval echo "\$$CAM" >/tmp/$$; IP=`cat /tmp/$$`; rm /tmp/$$
  rsync -av --size-only -e "ssh -i .ssh/pitronics_id_dsa" \
    pi@${IP}:pics/ fishpics/${CAM}-pics
elif [ x$UPDATE         == xyes ]                       # update and reboot cams
then
  updatecams
elif [ x$BACKUP         == xyes ]                       # back up server copy
then
  makebackup
elif [ x$STOP           == xyes ]                       # stop taking pics
then
  stopcams
elif [ x$MAKEVID        == xyes ]                       # create a video
then
  makevid $*
elif [ x$DF             == xyes ]                       # df
then
  diskfree
elif [ x$CLEAR          == xyes ]                       # clear camera disks
then
  clearcams
elif [ x$HALT           == xyes ]                       # halt cameras
then
  haltcams
elif [ x$WEBSERVE       == xyes ]                       # web server
then
  servehttp
else                                                    # the default: take pics
  picsloop
fi


#########################################################################
# makevid NOTES:
#  
# from http://blog.davidsingleton.org/raspberry-pi-timelapse-controller/
# (also discusses exposure times and flicker at sunset)
# ffmpeg -r 18 -q:v 2 -start_number XXXX -i /tmp/timelapse/IMG_%d.JPG \
#   output.mp4
#
# from http://www.raspberrypi-spy.co.uk/2013/05/creating-timelapse-videos-with-the-raspberry-pi-camera/
# avconv \
#   -r 10 -i timelapse_%04d.jpg \
#   -r 10 -vcodec libx264 -crf 20 -g 15 \
#   -vf crop=2592:1458,scale=1280:720 \
# timelapse.mp4
#
# from http://www.instructables.com/id/Simple-timelapse-camera-using-Raspberry-Pi-and-a-c/?ALLSTEPS
# mencoder -nosound -ovc lavc -lavcopts \
#   vcodec=mpeg4:aspect=16/9:vbitrate=8000000 -vf scale=1920:1080 \
#   -o timelapse.avi -mf type=jpeg:fps=24 mf://@list.txt
#
# from https://www.raspberrypi.org/learning/timelapse-setup/worksheet.md
# mencoder -nosound -ovc lavc -lavcopts \
#   vcodec=mpeg4:aspect=16/9:vbitrate=8000000 \
#   -vf scale=1920:1080 -o timelapse.avi -mf type=jpeg:fps=24 mf://@stills.txt
#
# from http://computers.tutsplus.com/tutorials/creating-time-lapse-photography-with-a-raspberry-pi--cms-20794
# mencoder -nosound -ovc lavc -lavcopts \
#   vcodec=mpeg4:aspect=16/9:vbitrate=8000000 -vf scale=1920:1080 \
#   -o timelapse.avi -mf type=jpeg:fps=24 mf://@stills.txt
