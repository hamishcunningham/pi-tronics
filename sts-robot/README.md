Robot Demo
==========


Code seeds from Phil Howard at Pimoroni -- @Gadgetoid -- thanks Phil!

---

cd; ln -s pi-tronics/sts-robot robot

sudo apt-get install python-pip
sudo pip install pibrella

edit /etc/rc.local and add /home/pi/robot/fotm-startup.sh &

----



Requires RPi.GPIO and Pibrella libraries

Includes alpha of Motobrella library

Ensure the files included in this demo are in /home/pi/robot/

Make sure startup.sh is executable.

Add /home/pi/robot/startup.sh to /etc/rc.local
