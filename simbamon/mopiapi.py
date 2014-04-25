import smbus

# version 0.1
# for mopi firmware v3.02

class mopiapi():
	device = 0xb

	def __init__(self, i2cbus = 1):
		self.bus = smbus.SMBus(i2cbus)

	def getStatus(self):
		return self.bus.read_byte_data(self.device, 0b00000000)

	def getVoltage(self):
		return self.bus.read_word_data(self.device, 0b00000001)

	# returns an array of 6 integers: max1, mid1, min1, max2, mid2, min2 (mV)
	def readConfig(self):
		data = self.bus.read_i2c_block_data(self.device, 0b00000010)
		data2 = []
		data2.append((data[1] << 8) + data[0])
		data2.append((data[3] << 8) + data[2])
		data2.append((data[5] << 8) + data[4])
		data2.append((data[7] << 8) + data[6])
		data2.append((data[9] << 8) + data[8])
		data2.append((data[11] << 8) + data[10])
		return data2

	# takes an array of 6 integers: max1, mid1, min1, max2, mid2, min2 (mV)
	def writeConfig(self, battery):
		data = [
			battery[0] & 0xff, battery[0] >> 8, \
			battery[1] & 0xff, battery[1] >> 8, \
			battery[2] & 0xff, battery[2] >> 8, \
			battery[3] & 0xff, battery[3] >> 8, \
			battery[4] & 0xff, battery[4] >> 8, \
			battery[5] & 0xff, battery[5] >> 8, \
			]
		self.bus.write_i2c_block_data(self.device, 0b00000010, data)

	def setPowerOnDelay(self, poweron):
		self.bus.write_word_data(self.device, 0b00000011, poweron)

	def setShutdownDelay(self, shutdown):
		self.bus.write_word_data(self.device, 0b00000100, shutdown)

	def getPowerOnDelay(self):
		return self.bus.read_word_data(self.device, 0b00000011)

	def getShutdownDelay(self):
		return self.bus.read_word_data(self.device, 0b00000100)

def statusDetail(byte):
	out = ""
	if (byte >> 7):
		out += 'Shutdown delay has been set\n'
	if (byte & 0b1000000) >> 6:
		out += 'Power on delay has been set\n'
	if (byte & 0b100000) >> 5:
		out += 'UPS mode\n'
	if (byte & 0b10000) >> 4:
		out += 'Forced shutdown (button pressed)\n'
	if (byte & 0b1000) >> 3:
		out += 'Battery critical\n'
	if (byte & 0b100) >> 2:
		out += 'Battery low\n'
	if (byte & 0b10) >> 1:
		out += 'Battery #2 active\n'
	if byte & 1:
		out += 'Battery #1 active\n'
	if out == "":
		out = "An error has occured"
	else:
		out = out[:-1]
	return out
