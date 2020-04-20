# coding: utf-8
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)

try:
    while True:
        print(GPIO.input(16))
        if GPIO.input(16):
         print('Ambiente bom')
         time.sleep(0.2)
        if GPIO.input(16)!=1:
         print('Gás detectado')

except KeyboardInterrupt:
    GPIO.cleanup()
