import time
from pibrella import *

class Wheel(Output):

	type = 'Wheel'

	def __init__(self, pin):
		self.frequency = 100
		super(Wheel,self).__init__(pin)
		self.pwm(self.frequency,0)

	def forward(self, speed, move_time = 0):
		self.pwm(self.frequency,0)
		self.duty_cycle(speed)
		if move_time > 0:
			time.sleep( move_time )
			self.stop()
			super(Wheel,self).stop()

	def stop(self):
		self.duty_cycle(0)
		self.low()

class Motobrella:
	motor_left = output.e
	motor_right = output.f
	default_frequency = 100
	
	def __init__(self):
		self.mover = None

	def begin(self):
		self.motor_left.pwm(self.default_frequency,0)
		self.motor_right.pwm(self.default_frequency,0)

	def move(self, left_speed, right_speed, move_time = 0):
		self.stop()
		self.begin()
		time_start = time.time()
		def _move():
			if move_time > 0 and time.time() - time_start >= move_time:
				self.motor_left.duty_cycle(0)
				self.motor_right.duty_cycle(0)
				return False
			self.motor_left.frequency(left_speed*2.5)
			self.motor_left.duty_cycle(left_speed)

			self.motor_right.frequency(right_speed*2.5)
			self.motor_right.duty_cycle(right_speed)

		self.mover = AsyncWorker(_move)
		self.mover.start()
		return True

	def forward(self, speed, move_time = 0):
		self.move( speed, speed, move_time )

	def left(self, speed, move_time = 0, ratio = 4):
		self.move( speed/ratio, speed, move_time )

	def right(self, speed, move_time = 0, ratio = 4):
		self.move( speed, speed/ratio, move_time )

	def turn(self, speed, degrees):
		degrees*=2
		if degrees > 0:
			self.move( speed, 0, abs(degrees)/speed)
		else:
			self.move( 0, speed, abs(degrees)/speed)

	def stop(self):
		if self.mover != None:
			self.mover.stop()
		self.motor_left.duty_cycle(0)
		self.motor_right.duty_cycle(0)
		self.motor_left.stop()
		self.motor_right.stop()

move = Motobrella()
#forward = motobrella.forward
#left = motobrella.left
#right = motobrella.right
stop = move.stop
#turn = motobrella.turn

left_wheel = Wheel( output.e.pin )
right_wheel = Wheel( output.f.pin )

wheel = Pins()
wheel._add( left = left_wheel )
wheel._add( right = right_wheel )

FAST = 100
MEDIUM = 50
SLOW = 20
