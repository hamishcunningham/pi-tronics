import smbus
from time import sleep

# Version 5

bus = smbus.SMBus(1)
device = 0xb

# http://www.raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2
# http://wiki.erazor-zone.de/wiki:linux:python:smbus:doc
# https://www.kernel.org/doc/Documentation/i2c/smbus-protocol

def readTest(status = 1, voltage = 1, configuration = 1, poweron = 1, shutdown = 1):

	# Get MoPi Status
	if status:
		byte = bus.read_byte_data(device, 0b00000000)
		print '   Status: {:08b}'.format(byte)
		statusDetail(byte)
		print ''

	# Get Voltage Level
	if voltage:
		word = bus.read_word_data(device, 0b00000001)
		print '  Voltage: {:08b} {:08b}'.format((word & 0xFF00) >> 8, word & 0xff)
		print '  Voltage: %i mV' % word
		print ''

	# Get MoPi Configuration
	if configuration:
		data = bus.read_i2c_block_data(device, 0b00000010)
		print '   B1 Max: {:08b} {:08b}'.format(data[1], data[0])
		print '   B1 Max: %i mV' % ((data[1] << 8) + data[0])
		print '   B1 Mid: {:08b} {:08b}'.format(data[3], data[2])
		print '   B1 Mid: %i mV' % ((data[3] << 8) + data[2])
		print '   B1 Min: {:08b} {:08b}'.format(data[5], data[4])
		print '   B1 Min: %i mV' % ((data[5] << 8) + data[4])
		print ''

		print '   B2 Max: {:08b} {:08b}'.format(data[7], data[6])
		print '   B2 Max: %i mV' % ((data[7] << 8) + data[6])
		print '   B2 Mid: {:08b} {:08b}'.format(data[9], data[8])
		print '   B2 Mid: %i mV' % ((data[9] << 8) + data[8])
		print '   B2 Min: {:08b} {:08b}'.format(data[11], data[10])
		print '   B2 Min: %i mV' % ((data[11] << 8) + data[10])
		print ''

	# Get Power On Delay
	if poweron:
		word = bus.read_word_data(device, 0b00000011)
		print ' On Delay: {:08b} {:08b}'.format((word & 0xFF00) >> 8, word & 0xff)
		print ' On Delay: %i seconds' % word
		print ''

	# Get Shutdown Delay
	if shutdown:
		word = bus.read_word_data(device, 0b00000100)
		print 'Off Delay: {:08b} {:08b}'.format((word & 0xFF00) >> 8, word & 0xff)
		print 'Off Delay: %i seconds' % word
		print ''

def statusDetail(byte):
	if (byte >> 7):
		print '           Shutdown delay has been set'
	if (byte & 0b1000000) >> 6:
		print '           Power on delay has been set'
	if (byte & 0b100000) >> 5:
		print '           UPS mode'
	if (byte & 0b10000) >> 4:
		print '           Forced shutdown (button pressed)'
	if (byte & 0b1000) >> 3:
		print '           Battery critical'
	if (byte & 0b100) >> 2:
		print '           Battery low'
	if (byte & 0b10) >> 1:
		print '           Battery #2 active'
	if byte & 1:
		print '           Battery #1 active'

def writeTest(poweron = -1, shutdown = -1, battery = []):

	# Set MoPi Configuration
	if len(battery) == 6:
		print '  Writing battery configuration'
		data = [
			battery[0] & 0xff, battery[0] >> 8, \
			battery[1] & 0xff, battery[1] >> 8, \
			battery[2] & 0xff, battery[2] >> 8, \
			battery[3] & 0xff, battery[3] >> 8, \
			battery[4] & 0xff, battery[4] >> 8, \
			battery[5] & 0xff, battery[5] >> 8, \
			]
		bus.write_i2c_block_data(device, 0b00000010, data)

	# Set Power On Delay
	if poweron >= 0:
		print '  Writing power on delay: %i' % poweron
		bus.write_word_data(device, 0b00000011, poweron)

	# Set Shutdown Delay
	if shutdown >= -1:
		print '  Writing shutdown delay: %i' % shutdown
		bus.write_word_data(device, 0b00000100, shutdown)

	print ''


#############################
#### Program starts here ####
#############################

print 'Initial read tests...\n'
readTest()

print 'Write test #1 (delays)...'
writeTest(poweron = 10, shutdown = 360)

print 'Sleeping 2 seconds...\n'
sleep(2)

print 'Read back test...\n'
readTest(status = 1, voltage = 0, configuration = 0, poweron = 1, shutdown = 1)

print 'Write test #2 (all)...'
#writeTest(poweron = 0, shutdown = 0, battery=[18000, 10000, 7000, 19000, 11000, 8000])
writeTest(poweron = 0, shutdown = 0, battery=[11300, 9800, 8000, 11500, 10000, 8200])

print 'Read back test...\n'
readTest(status = 1, voltage = 0, configuration = 1, poweron = 1, shutdown = 1)
