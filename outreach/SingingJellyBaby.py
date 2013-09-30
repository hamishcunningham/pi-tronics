# SingingJellyBaby.py

import time
import RPi.GPIO as GPIO
import os

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN)

while True:
  if GPIO.input(3) == False:
    print("time to sing!")
    # os.system('mpg321 la.mp3 &')
    os.system('aplay police_s.wav &')

  print("time to sleep...")
  time.sleep(2)
