import time
import RPi.GPIO as GPIO

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

GPIO.setup(3,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(7,GPIO.OUT)

while True:
  GPIO.output(5,GPIO.LOW)
  GPIO.output(3,GPIO.HIGH)
  time.sleep(2)

  GPIO.output(5,GPIO.HIGH)
  time.sleep(2)

  GPIO.output(5,GPIO.LOW)
  GPIO.output(3,GPIO.LOW)
  GPIO.output(7,GPIO.HIGH)
  time.sleep(2)

  GPIO.output(7,GPIO.LOW)
  GPIO.output(5,GPIO.HIGH)
  time.sleep(2)
