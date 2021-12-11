# pin kuning (pwm) di pin 3 raspi
# pin orange (5v) di pin 4 raspi
# pin coklat (gnd) di pin 6 raspi

import RPi.GPIO as GPIO
import sys
import time
import ultra # ultra.py
GPIO.setwarnings(False)

def bukaServo():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3,GPIO.OUT)
    q=GPIO.PWM(3,50)
    q.start(2.5) #0 derajat

    #q=GPIO.PWM(3,50)
    print('Selamat Datang')
    q.ChangeDutyCycle(6.3) #90 derajat
    time.sleep(1)

def tutupServo():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3,GPIO.OUT)
    q=GPIO.PWM(3,50)
    time.sleep(4)
    q.start(2.5) #0 derajat
    q.ChangeDutyCycle(2.5) #0 derajat
    time.sleep(1)

GPIO.cleanup()