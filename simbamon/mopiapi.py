import smbus

VERSION=0.2
# for mopi firmware v3.03
FIRMMAJ=3
FIRMMINR=3

class mopiapi():
	device = 0xb

	def __init__(self, i2cbus = 1):
		self.bus = smbus.SMBus(i2cbus)
		[maj, minr] = self.getFirmwareVersion()
		if maj != FIRMMAJ or minr != FIRMMINR:
			raise Exception("Version mis-match between API and MoPi. Got %i.%02i, expected %i.%02i." % (maj, minr, FIRMMAJ, FIRMMINR))

	def getStatus(self):
		return self.bus.read_word_data(self.device, 0b00000000)

	def getVoltage(self, input=0):
		if input == 1:
			return self.bus.read_word_data(self.device, 0b00000101) # 5
		elif input == 2:
			return self.bus.read_word_data(self.device, 0b00000110) # 6
		else:
			return self.bus.read_word_data(self.device, 0b00000001)

	# returns an array of 3 integers: max, mid, min (mV)
	def readConfig(self, input=0):
		if input == 1:
			data = self.bus.read_i2c_block_data(self.device, 0b00000111) # 7
		elif input == 2:
			data = self.bus.read_i2c_block_data(self.device, 0b00001000) # 8
		else:
			data = self.bus.read_i2c_block_data(self.device, 0b00000010)
		data2 = []
		data2.append((data[0] << 8) + data[1])
		data2.append((data[2] << 8) + data[3])
		data2.append((data[4] << 8) + data[5])
		return data2

	# takes an array of 3 integers: max, mid, min (mV)
	def writeConfig(self, battery, input=0):
		data = [
			battery[0] >> 8, battery[0] & 0xff, \
			battery[1] >> 8, battery[1] & 0xff, \
			battery[2] >> 8, battery[2] & 0xff, \
			]
		if input == 1:
			self.bus.write_i2c_block_data(self.device, 0b00000111, data) # 7
		elif input == 2:
			self.bus.write_i2c_block_data(self.device, 0b00001000, data) # 8
		else:
			self.bus.write_i2c_block_data(self.device, 0b00000010, data)

	def setPowerOnDelay(self, poweron):
		self.bus.write_word_data(self.device, 0b00000011, poweron)

	def setShutdownDelay(self, shutdown):
		self.bus.write_word_data(self.device, 0b00000100, shutdown)

	def getPowerOnDelay(self):
		return self.bus.read_word_data(self.device, 0b00000011)

	def getShutdownDelay(self):
		return self.bus.read_word_data(self.device, 0b00000100)

	def getFirmwareVersion(self):
		word = self.bus.read_word_data(self.device, 0b00001001) # 9
		return [word >> 8, word & 0xff]

	def getSerialNumber(self):
		return self.bus.read_word_data(self.device, 0b00001010) # 10

def getApiVersion():
	return VERSION

def statusDetail(byte):
	out = ""
	if (byte & 0b100000000000) >> 10:
		out += 'Shutdown delay in progress\n'
	if (byte & 0b10000000000) >> 10:
		out += 'Shutdown delay set\n'
	if (byte & 0b1000000000) >> 9:
		out += 'Power on delay in progress\n'
	if (byte & 0b100000000) >> 8:
		out += 'Power on delay set\n'
	if (byte & 0b10000000) >> 7:
		out += 'Forced shutdown\n'
#	if (byte & 0b1000000) >> 6:
#		out += 'Unused!\n'
	if (byte & 0b100000) >> 5:
		out += 'Battery critical (flashing red led)\n'
	if (byte & 0b10000) >> 4:
		out += 'Battery low (red led)\n'
	if (byte & 0b1000) >> 3:
		out += 'Battery good (green led)\n'
	if (byte & 0b100) >> 2:
		out += 'Battery full (blue led)\n'
	if (byte & 0b10) >> 1:
		out += 'Battery #2 active\n'
	if byte & 1:
		out += 'Battery #1 active\n'
	if out == "":
		out = "An error has occured"
	else:
		out = out[:-1]
	return out
