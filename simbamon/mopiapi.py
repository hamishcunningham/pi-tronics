#!/usr/bin/env python
# mopiapi. Python interface to the MoPi battery power add-on board for the
#   Raspberry Pi. (http://pi.gate.ac.uk/mopi)

import smbus
import errno
import RPi.GPIO
import time

# Version of the API
APIVERSION=0.3

# For at least mopi firmware vX.YY...
FIRMMAJ=3
FIRMMINR=5

# Package version
VERSION="3.6+2"

# Number of times to retry a failed I2C read/write to the MoPi
MAXTRIES=3

class mopiapi():
	device = 0xb
	maj = 0
	minr = 0

	def __init__(self, i2cbus = -1):
		if i2cbus == -1:
			i2cbus = guessI2C()
		self.bus = smbus.SMBus(i2cbus)
		[self.maj, self.minr] = self.getFirmwareVersion()
		if self.maj != FIRMMAJ or self.minr < FIRMMINR:
			raise OSError(errno.EUNATCH, "Expected at least MoPi firmware version %i.%02i, got %i.%02i instead." % (FIRMMAJ, FIRMMINR, self.maj, self.minr))

	def getStatus(self):
		word = self.readWord(0b00000000)
		if self.maj == 3 and self.minr > 9:
			# bit changed at v3.10
			word = word ^ (1 << 6)
		return word

	def getVoltage(self, input=0):
		if input == 1:
			return self.readWord(0b00000101) # 5
		elif input == 2:
			return self.readWord(0b00000110) # 6
		else:
			return self.readWord(0b00000001)

	# returns an array of 5 integers: power source type, max, good, low, crit (mV)
	def readConfig(self, input=0):
		# try reading the config
		tries = 0
		error = 0
		while tries < MAXTRIES:
			error = 0
			try:
				if input == 1:
					data = self.bus.read_i2c_block_data(self.device, 0b00000111) # 7
				elif input == 2:
					data = self.bus.read_i2c_block_data(self.device, 0b00001000) # 8
				else:
					data = self.bus.read_i2c_block_data(self.device, 0b00000010) # 2
				break
			except IOError as e:
				error = e
				time.sleep(0.33)
			tries += 1
		# unsucessfully read
		if error != 0:
			if e.errno == errno.EIO:
				e.strerror = "I2C bus input/output error on read config"
			raise e
		if tries == MAXTRIES or (self.maj == 3 and self.minr > 9 and data[0] == 255):
			raise IOError(errno.ECOMM, "Communications protocol error on read config")
		# behaivour changed at v3.10 to 5x0 so that 255 could serve as error detection
		if self.maj == 3 and self.minr > 9 and cmp(data[:5], [0, 0, 0, 0, 0]) == 0:
			data = [255, 255, 255, 255, 255]
		if data[0] != 255:
			# it's a cV reading that we need to convert back to mV
			# (with 255's it's indicating a differing config)
			for i in range(1,5):
				data[i] *= 100
		return data[:5]

	# takes an array of 5 integers: power source type, max, good, low, crit (mV)
	def writeConfig(self, battery, input=0):
		if len(battery) != 5:
			raise IOError(errno.EINVAL, "Invalid parameter, wrong number of arguments")
		if battery[0] < 1 or battery[0] > 3:
			raise IOError(errno.EINVAL, "Invalid parameter, type outside range")

		data = [battery[0]]
		for i in range(1,5):
			battery[i] /= 100
			data.append(battery[i])
			battery[i] *= 100 # for the read back we need to compare to the rounded value
			if data[i] < 0 or data[i] > 255:
				raise IOError(errno.EINVAL, "Invalid parameter, voltage outside range")

		# check if config to be written matches existing config
		if cmp(battery, self.readConfig(input)) == 0:
			return

		# try writing the config
		tries = 0
		error = 0
		while tries < MAXTRIES:
			error = 0
			try:
				if input == 1:
					self.bus.write_i2c_block_data(self.device, 0b00000111, data) # 7
				elif input == 2:
					self.bus.write_i2c_block_data(self.device, 0b00001000, data) # 8
				else:
					self.bus.write_i2c_block_data(self.device, 0b00000010, data) # 2
			except IOError as e:
				error = e
				time.sleep(0.33)
			# read back test
			time.sleep(0.02) # slight delay to allow write to take effect
			if cmp(battery, self.readConfig(input)) == 0:
				break
			tries += 1
		# unsucessfully written
		if error != 0:
			if e.errno == errno.EIO:
				e.strerror = "I2C bus input/output error on send config"
			raise e
		if tries == MAXTRIES:
			raise IOError(errno.ECOMM, "Communications protocol error on send config")

	def setPowerOnDelay(self, poweron):
		self.writeWord(0b00000011, poweron)

	def setShutdownDelay(self, shutdown):
		self.writeWord(0b00000100, shutdown)

	def getPowerOnDelay(self):
		return self.readWord(0b00000011)

	def getShutdownDelay(self):
		return self.readWord(0b00000100)

	def getFirmwareVersion(self):
		word = self.readWord(0b00001001) # 9
		return [word >> 8, word & 0xff]

	def getSerialNumber(self):
		return self.readWord(0b00001010) # 10

	def baseReadWord(self, register):
		tries = 0
		data = 0xFFFF
		error = 0
		while data == 0xFFFF and tries < MAXTRIES:
			error = 0
			try:
				data = self.bus.read_word_data(self.device, register)
			except IOError as e:
				error = e
				time.sleep(0.33)
			tries += 1
		# unsucessfully read
		if error != 0:
			if e.errno == errno.EIO:
				e.strerror = "I2C bus input/output error on read word"
			raise e
		if data == 0xFFFF:
			raise IOError(errno.ECOMM, "Communications protocol error on read word")
		return data

	def readWord(self, register):
		return self.baseReadWord(register)

	def advancedReadWord(self, register):
		data = self.baseReadWord(register)

		# try and re-read the config in the case of a high bit to
		# counter possible i2c clock drift
		# see https://github.com/raspberrypi/linux/issues/254
		# use if you're having consistent problems reading words
		if data & 32768 == 32768 or data & 128 == 128:
			data2 = self.baseReadWord(register)
			if data != data2:
				data3 = self.baseReadWord(register)
				if data2 == data3:
					return data2
				else:
					raise IOError(errno.ECOMM, "Communications protocol error on read word, bit 15 or 7")
		return data

	def writeWord(self, register, data):
		if data < 0 or data > 0xFFFF:
			raise IOError(errno.EINVAL, "Invalid parameter, value outside range")

		# check if word is already set
		if self.readWord(register) == data:
			return

		# try writing
		tries = 0
		error = 0
		while tries < MAXTRIES:
			error = 0
			try:
				self.bus.write_word_data(self.device, register, data)
			except IOError as e:
				error = e
				time.sleep(0.33)
			# read back test
			time.sleep(0.02) # slight delay to allow write to take effect
			if self.readWord(register) == data:
				break
			tries += 1
		# unsucessfully written
		if error != 0:
			if e.errno == errno.EIO:
				e.strerror = "I2C bus input/output error on write word"
			raise e
		if tries == MAXTRIES:
			raise IOError(errno.ECOMM, "Communications protocol error on write word")
			

def getApiVersion():
	return APIVERSION


class status():
	byte = 0

	def __init__(self, status):
		self.byte = status

	def getByte(self):
		return self.byte

	# get the bit, starting from 0 LSB
	def getBit(self, bitnum):
		return (self.byte & (1 << bitnum)) >> bitnum
	
	
	def SourceOneActive(self):
		return self.getBit(0)
	def SourceTwoActive(self):
		return self.getBit(1)

	def LEDBlue(self):
		return self.getBit(2)
	def LEDGreen(self):
		return self.getBit(3)
	def LEDRed(self):
		return self.getBit(4)
	def LEDFlashing(self):
		return self.getBit(5)

	# Output: 1 for NiMH, 0 for Alkaline
	def JumperState(self):
		return not self.getBit(6)
	
	def ForcedShutdown(self):
		return self.getBit(7)

	def PowerOnDelaySet(self):
		return self.getBit(8)
	def PowerOnDelayActive(self):
		return self.getBit(9)
	def ShutdownDelaySet(self):
		return self.getBit(10)
	def ShutdownDelayActive(self):
		return self.getBit(11)

	def CheckSourceOne(self):
		return self.getBit(12)
	def CheckSourceTwo(self):
		return self.getBit(13)

	def UserConfiguration(self):
		return self.getBit(14)


	def StatusDetail(self):
		out = ""

		if self.SourceOneActive():
			out += 'Source #1 active\n'
		if self.SourceTwoActive():
			out += 'Source #2 active\n'

		if self.LEDBlue():
			out += 'Source full (blue led)\n'
		if self.LEDGreen():
			out += 'Source good (green led)\n'
		if self.LEDRed():
			out += 'Source low (red led)\n'
		if self.LEDFlashing():
			out += 'Source critical (flashing red led)\n'

		if not self.UserConfiguration():
			if self.JumperState():
				out += 'NiMH battery profile\n'
			else:
				out += 'Alkaline battery profile\n'

		if self.ForcedShutdown():
			out += 'Forced shutdown\n'

		if self.PowerOnDelaySet():
			out += 'Power on delay set\n'
		if self.PowerOnDelayActive():
			out += 'Power on delay in progress\n'
		if self.ShutdownDelaySet():
			out += 'Shutdown delay set\n'
		if self.ShutdownDelayActive():
			out += 'Shutdown delay in progress\n'

		if self.CheckSourceOne():
			out += 'Source #1 good\n'
		else:
			out += 'Source #1 low/not present\n'
		if self.CheckSourceTwo():
			out += 'Source #2 good\n'
		else:
			out += 'Source #2 low/not present\n'

		if self.UserConfiguration():
			out += 'User configured\n'

		if out == "":
			# Source #1 or #2 should always be active...
			raise IOError(errno.EINVAL, "Invalid status")
		else:
			out = out[:-1]
		return out

def guessI2C():
	# Rev2 of RPi switched the i2c address, so return the right one for the board we have 
	if RPi.GPIO.RPI_REVISION == 1:
		return 0
	else:
		return 1
