#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# this many mm per bucket tip
CALIBRATION = 0.2794
# which GPIO pin the gauge is connected to
PIN = 17
# file to log rainfall data in
LOGFILE = "log.csv"

GPIO.setmode(GPIO.BCM)  
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# variable to keep track of how much rain
rain = 0

# the call back function for each bucket tip
def cb(channel):
	global rain
	rain = rain + CALIBRATION

# register the call back for pin interrupts
GPIO.add_event_detect(PIN, GPIO.FALLING, callback=cb, bouncetime=300)

# open the log file
file = open(LOGFILE, "a")

# display and log results
while True:
	line = "%i, %f" % (time.time(), rain)
	print(line)
	file.write(line + "\n")
	file.flush()
	rain = 0
	time.sleep(5)

# close the log file and exit nicely
file.close()
GPIO.cleanup()
