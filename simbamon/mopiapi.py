#!/usr/bin/env python
# mopiapi. Python interface to the MoPi battery power add-on board for the
#   Raspberry Pi. (http://pi.gate.ac.uk/mopi)

import smbus
import errno
import re

# Version of the API
APIVERSION=0.3

# For at least mopi firmware vX.YY...
FIRMMAJ=3
FIRMMINR=5

# Package version
VERSION=3.2+1

# Number of times to retry a failed I2C read/write to the MoPi
RETRIES=3

class mopiapi():
	device = 0xb

	def __init__(self, i2cbus = -1):
		if i2cbus == -1:
			i2cbus = guessI2C()
		self.bus = smbus.SMBus(i2cbus)
		[maj, minr] = self.getFirmwareVersion()
		if maj != FIRMMAJ or minr < FIRMMINR:
			raise OSError(errno.EUNATCH, "Expected at least MoPi firmware version %i.%02i, got %i.%02i instead." % (FIRMMAJ, FIRMMINR, maj, minr))

	def getStatus(self):
		return self.readWord(0b00000000)

	def getVoltage(self, input=0):
		if input == 1:
			return self.readWord(0b00000101) # 5
		elif input == 2:
			return self.readWord(0b00000110) # 6
		else:
			return self.readWord(0b00000001)

	# returns an array of 5 integers: power source type, max, good, low, crit (mV)
	def readConfig(self, input=0):
		if input == 1:
			data = self.bus.read_i2c_block_data(self.device, 0b00000111) # 7
		elif input == 2:
			data = self.bus.read_i2c_block_data(self.device, 0b00001000) # 8
		else:
			data = self.bus.read_i2c_block_data(self.device, 0b00000010)
		if data[0] != 255:
			for i in range(1,5):
				data[i] *= 100
		return data[:5]

	# takes an array of 5 integers: power source type, max, good, low, crit (mV)
	def writeConfig(self, battery, input=0):
		if len(battery) != 5:
			raise IOError(errno.EINVAL, "Invalid parameter")
		if battery[0] < 1 or battery[0] > 2:
			raise IOError(errno.EINVAL, "Invalid parameter")

		data = [battery[0]]
		for i in range(1,5):
			battery[i] /= 100
			data.append(battery[i])
			battery[i] *= 100 # for the read back we need to compare to the rounded value
			if data[i] < 0 or data[i] > 255:
				raise IOError(errno.EINVAL, "Invalid parameter")

		# check if config to be written matches existing config
		tries = 0
		while cmp(battery, self.readConfig(input)) != 0 and tries < RETRIES:
			if input == 1:
				self.bus.write_i2c_block_data(self.device, 0b00000111, data) # 7
			elif input == 2:
				self.bus.write_i2c_block_data(self.device, 0b00001000, data) # 8
			else:
				self.bus.write_i2c_block_data(self.device, 0b00000010, data)
			tries += 1
		# unsucessfully written
		if tries - 1 == RETRIES:
			raise IOError(errno.ECOMM, "Communication error on send")
			return False
		return True

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

	def readWord(self, register):
		tries = 0
		data = 0xFFFF
		while data == 0xFFFF and tries < RETRIES:
			data = self.bus.read_word_data(self.device, register)
			tries += 1
		if data == 0xFFFF:
			raise IOError(errno.EIO, "")
		data = data & 32767 # fix for leading bit
		return data

	def writeWord(self, register, data):
		if data < 0 or data > 0xFFFF:
			raise IOError(errno.EINVAL, "Invalid parameter")

		tries = 0
		while self.readWord(register) != data and tries < RETRIES:
			self.bus.write_word_data(self.device, register, data)
			tries += 1
		# unsucessfully written
		if tries - 1 == RETRIES:
			raise IOError(errno.ECOMM, "Communication error on send")
			return False
		return True
			

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
			out += 'Battery #1 active\n'
		if self.SourceTwoActive():
			out += 'Battery #2 active\n'

		if self.LEDBlue():
			out += 'Battery full (blue led)\n'
		if self.LEDGreen():
			out += 'Battery good (green led)\n'
		if self.LEDRed():
			out += 'Battery low (red led)\n'
		if self.LEDFlashing():
			out += 'Battery critical (flashing red led)\n'

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
			out += 'Battery #1 good\n'
		else:
			out += 'Battery #1 low/not present\n'
		if self.CheckSourceTwo():
			out += 'Battery #2 good\n'
		else:
			out += 'Battery #2 low/not present\n'

		if self.UserConfiguration():
			out += 'User configured\n'

		if out == "":
			# Battery #1 or #2 should always be active...
			raise IOError(errno.EINVAL, "Invalid status")
		else:
			out = out[:-1]
		return out

def guessI2C():
	# try to auto-detect appropriate bus, boards 2 and 3 are Model B Rev 1.0
	if (int(re.search('Revision\t: ([0-9a-e]*)', open('/proc/cpuinfo').read(1000)).group(1), 16) & 0xFFFF) < 4:
		return 0
	else:
		return 1
