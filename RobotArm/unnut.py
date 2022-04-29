import time
import numpy as np
import Matrices.frame as fr
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
import RPi.GPIO as GPIO  # control through GPIO pins

# adafruit forces GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BCM)
# I2C for PCS9685 and Gyro
# create i2c bus interface to access PCA9685, for example
i2c = busio.I2C(SCL, SDA)    # busio.I2C(board.SCL, board.SDA) create i2c bus
pca = PCA9685(i2c, address=0x41)           # adafruit_pca9685.PCA9685(i2c)   instance PCA9685 on bus
pca.frequency = 50  # set pwm clock in Hz (debug 60 was 1000)
# usage: pwm_channel = pca.channels[0] instance example
#        pwm_channel.duty_cycle = speed (0 .. 100)  speed example

L1 = 100
L2 = 105

PWMOEN = 4  # pin 7 #PCA9685 OEn pin
pwmOEn = GPIO.setup(PWMOEN, GPIO.OUT)  # enable PCA outputs

R1 = pca.channels[0]
R2 = pca.channels[1]
R3 = pca.channels[2]
R4 = pca.channels[3]
R5 = pca.channels[4]
clawRange = [40.60]


# equivalent of Arduino map()
def valmap(value, istart, istop, ostart, ostop): 
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

# for 0 to 100, % speed as integer, to use for PWM 
# full range 0xFFFF, but PCS9685 ignores last Hex digit as only 12 bit resolution)
def getPWMPer(value): 
    if value < 0:
      value = 0
      print("Angle is below range")
    if value > 180:
      value = 180
      print("Angle is above range")
    return int(valmap(value, 0, 180, 2038, 12.5/100 * 0xFFFF))

def zeroArm():
    R1.duty_cycle = getPWMPer(90)
    R2.duty_cycle = getPWMPer(90)
    R3.duty_cycle = getPWMPer(90)
    R4.duty_cycle = getPWMPer(90)
    R5.duty_cycle = getPWMPer(90)

def moveTo(point):
    beta = np.deg2rad(point[3])
    alpha = (point[2]) # kept in degrees
    x = point[0]
    y = point[1]
    p2 = None
    if beta > 90:
      x2 = x + L1 * np.cos(beta)
      y2 = y + L1 * np.sin(beta)
      p2 = [x2, y2]
    else:
      x2 = x - L1 * np.cos(beta)
      y2 = y - L1 * np.sin(beta)
      p2 = [x2, y2]
    t2 = np.arctan2(p2[1], p2[0])
    t1 = (90 - t2) + beta
    R1.duty_cycle = getPWMPer(alpha)
    R2.duty_cycle = getPWMPer(np.rad2deg(t1))
    R3.duty_cycle = getPWMPer(np.rad2deg(t2))

    if point[4]:
      R5.duty_cycle = getPWMPer(clawRange[0])
    else:
      R5.duty_cycle = getPWMPer(clawRange[1])

# points using coords [x,y,thetaBase, thetaClaw, grabbing] in mm and degrees:
initLoc = [[0], [0], [0], [0], False]
nutLoc = [[100], [100], [30], [90], False]
screwLoc = [[100], [0], [-30], [140], True]


# while True:
zeroArm()
time.sleep(1)
moveTo(initLoc)
