import time
import numpy as np
import Matrices.frame as fr
from board import SCL,SDA
import busio
from adafruit_pca9685 import PCA9685
import RPi.GPIO as GPIO #control through GPIO pins

# adafruit forces GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BCM)
#I2C for PCS9685 and Gyro
# create i2c bus interface to access PCA9685, for example
i2c = busio.I2C(SCL, SDA)    #busio.I2C(board.SCL, board.SDA) create i2c bus
pca = PCA9685(i2c, address = 0x41)           #adafruit_pca9685.PCA9685(i2c)   instance PCA9685 on bus
pca.frequency = 1000 #set pwm clock in Hz (debug 60 was 1000)
# usage: pwm_channel = pca.channels[0] instance example
#        pwm_channel.duty_cycle = speed (0 .. 100)  speed example

PWMOEN = 4 #pin 7 #PCA9685 OEn pin
pwmOEn = GPIO.setup(PWMOEN, GPIO.OUT)  # enable PCA outputs

R1 = pca.channels[0]

#equivalent of Arduino map()
def valmap(value, istart, istop, ostart, ostop): 
  return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

#for 0 to 100, % speed as integer, to use for PWM 
#full range 0xFFFF, but PCS9685 ignores last Hex digit as only 12 bit resolution)
def getPWMPer(value): 
  return int(valmap(value, 0, 100, 0, 0xFFFF))

while True:
    for i in range(100):
        R1.duty_cycle = getPWMPer(i)
        time.sleep(0.01)
        print(i)
    for i in range(100):
        R1.duty_cycle = getPWMPer(100-i)
        time.sleep(0.01)
        print(i)