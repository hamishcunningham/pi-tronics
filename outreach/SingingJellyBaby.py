# SingingJellyBaby.py

import time
import RPi.GPIO as GPIO
import os

GPIO.cleanup()
GPIO.semode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN)

while True:
  if GPIO.input(3) == False:
    os.system('mpg321 la.mp3 &')
  time.sleep(1)
