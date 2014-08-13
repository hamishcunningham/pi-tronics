#!/usr/bin/env python
# mopilog.py. Log the voltage and status of the MoPi battery power add-on to
#   a csv file for later analysis.  (http://pi.gate.ac.uk/mopi)

import mopiapi
import csv
from time import sleep, gmtime, strftime, time


# file to log results to
outputfile = 'mopilog.csv'

# logging interval (seconds)
interval = 5

# enable console display
display = 0


# connect to the mopi!
mymopi = mopiapi.mopiapi()

# open the output file for logging
with open(outputfile, 'ab') as logfile:
	# let's have a csv file
	logwriter = csv.writer(logfile, quoting=csv.QUOTE_NONNUMERIC)
	# headers for the csv
	logwriter.writerow(['Date & Time', 'Current Voltage (mV)', 'Status Word', 'Voltage #1 (mV)', 'Voltage #2 (mV)'])

	# loop & log
	while True:
		a = time() # timer for sleeping
		n = strftime('%Y-%m-%d %H:%M:%S', gmtime()) # date & time
		v = mymopi.getVoltage() # current voltage
		s = mymopi.getStatus() # current MoPi status
		v1 = mymopi.getVoltage(1) # voltage of source #1
		v2 = mymopi.getVoltage(2) # voltage of source #2
		logwriter.writerow([n, v, s, v1, v2])
		if display == 1:
			print "%s\n\tCurrent Voltage: %s mV" % (n, v)
			print "\tStatus Word: %i" % s
			print "\tVoltage #1: %i mV" % v1
			print "\tVoltage #2: %i mV" % v2
		# sleep until it is time to log again
		sleep(interval - (time() - a))
