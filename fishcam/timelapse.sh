#!/bin/bash
#
# timelapse.sh

# standard locals
alias cd='builtin cd'
P="$0"
USAGE="`basename ${P}` [-h(elp)] [-d(ebug)] [-f[123]]"
DBG=:
OPTIONSTRING=hdf:

# specific locals
CAM=
SLEEP=60
PICSDIR=/home/pi/pics

# message & exit if exit num present
usage() { echo -e Usage: $USAGE; [ ! -z "$1" ] && exit $1; }

# process options
while getopts $OPTIONSTRING OPTION
do
  case $OPTION in
    h)	usage 0 ;;
    d)	DBG=echo ;;
    f)	CAM="f${OPTARG}" ;;
    *)	usage 1 ;;
  esac
done 
shift `expr $OPTIND - 1`

# take pics
picsloop() {
  while :
  do
    NOW=`date '+%Y-%m-%d--%T'|sed 's,:,-,g'`
    raspistill -t 1500 -o ${NOW}.jpg
    sleep $SLEEP
  done
}
[ -d $PICSDIR ] || mkdir -p $PICSDIR

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
if [ x"$CAM" != x ]                             # ssh into the cam
then
  eval echo "\$$CAM" >/tmp/$$
  IP=`cat /tmp/$$`
  rm /tmp/$$
  echo $IP

  cd
  ssh -i .ssh/pitronics_id_dsa pi@${IP}
  exit 0
fi

# the default: take pics
cd $PICSDIR
picsloop
