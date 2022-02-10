import time #used to set delay time to control moving distance

#set up PC9685 osoyoo/AdaFruit
from board import SCL,SDA
import busio
from adafruit_pca9685 import PCA9685

#set up Raspberry Pi GPIO
import RPi.GPIO as GPIO #control through GPIO pins

switch_pin = 26 #pin 37
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(switch_pin, GPIO.FALLING, callback = switch_callback)


def switch_callback(self):
    print("switch pressed")

while True:
    time.sleep(1)