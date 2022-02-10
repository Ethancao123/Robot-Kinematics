import time #used to set delay time to control moving distance

#set up PC9685 osoyoo/AdaFruit
from board import SCL,SDA
import busio
from adafruit_pca9685 import PCA9685

#set up Raspberry Pi GPIO
import RPi.GPIO as GPIO #control through GPIO pins


# adafruit forces GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BCM)
#I2C for PCS9685 and Gyro
# create i2c bus interface to access PCA9685, for example
i2c = busio.I2C(SCL, SDA)    #busio.I2C(board.SCL, board.SDA) create i2c bus
pca = PCA9685(i2c)           #adafruit_pca9685.PCA9685(i2c)   instance PCA9685 on bus
pca.frequency = 1000 #set pwm clock in Hz (debug 60 was 1000)
# usage: pwm_channel = pca.channels[0] instance example
#        pwm_channel.duty_cycle = speed (0 .. 100)  speed example


#motors
# front controller, PCA channel
ENAFR = 0
IN1FR = 1
IN2FR = 2

IN3FL = 5
IN4FL = 6
ENBFL = 4
# rear controller, PCA channel
ENARR = 8
IN1RR = 9
IN2RR = 10

IN3RL = 13
IN4RL = 14
ENBRL = 12

#Encoders, GPIO.board pin
S1FR = 17 #pin 11
S2FR = 27 #pin 13 

S1FL = 20 #pin CHANGED
S2FL = 21 #pin CHANGED

S1RR = 12  #pin CHANGED
S2RR = 16 #pin CHANGED

S1RL = 5  #pin 29
S2RL = 6  #pin 31
perRev = 155 # estimate A type motors

#PCA9685
PWMOEN = 4 #pin 7 #PCA9685 OEn pin
pwmOEn = GPIO.setup(PWMOEN, GPIO.OUT)  # enable PCA outputs

#encoder class 
class Encoder:
  def __init__(self, name, S1, S2, side):
    self.name = name #for debug
    self.s1  = S1 #pin
    GPIO.setup(S1, GPIO.IN) #instance
    self.s2  = S2 #pin
    GPIO.setup(S2, GPIO.IN)  
    self.aState = 0 #value (aState)
    self.bState = 0
    self.aLastState = 0 # remember last value (aLastState)
#    self.bLastState = 0 # not needed?
    self.counter = 0
    self.lastCounter = 0
#    self.aturn = 0 # for diagnostic
#    self.bturn = 0 #for diagnostic
    self.speed = 0
    self.time = time.perf_counter_ns()
    self.lastTime = self.time
    self.side = side
        
  def read(self):
    self.aState  = GPIO.input(self.s1)
    self.bState  = GPIO.input(self.s2)
    self.time = time.perf_counter_ns()
    return self.aState, self.bState
    
  def read_turn(self):
    return self.aturn, self.bturn  # for diagnostic (whole method)
    
  def name(self):
    return self.name # for diagnostic (whole method)
    
  def readEncoder(self):
    #Reads the "current" state of the encoders
    aState, bState = self.read() 
    #If the previous and the current state are different,  a Pulse has occured
    if aState != self.aLastState  :
      #self.aturn +=1; #for diagnostic
      #If the outputB state is different to the outputA state, rotating clockwise
      if bState!= aState :
        self.counter += 1
      else : #rotating counter clockwise
        self.counter -= 1
       
#   if bState != self.bLastState  :
#      self.bturn +=1; #for diagnostic
     
#    if aState != self.aLastState or bState != self.bLastState:
#      print(self.name +" position: " + str(self.counter) + " a: " + str(self.aturn) + " b: " + str(self.bturn) ) #for diagnostic
     
    self.aLastState = aState #remember last state of a
#   self.bLastState = bState #remember last state of b (for diagnostic)

  def readEncoderTest(self):
    self.readEncoder()
    print(self.name +" position: " + str(self.counter)  ) #for diagnostic
    
    
#set up call back functions, ignore 2nd parameter 
  def callback_encoder(self,channel):
    print("click  " + self.name)
    self.readEncoder()

  def callback_encoder2(self,channel):
    print("click2  " + self.name)
    self.readEncoder()
    
  def readSpeed(self):
    #correct for side of car left goes - otherwise
    if self.time != 0 and self.time != self.lastTime: #store speed in clicks/nS
      self.speed = self.side * (self.counter - self.lastCounter)/(self.time - self.lastTime)
    else:
      self.speed = 0

    # lastTime and lastCounter were set at last call to this function
    self.lastTime = self.time #time was set at each/last call to .read
    self.lastCounter = self.counter #counter was set at each/last call to .readEncoder

    print(self.name +" position: " + str(self.counter) + " @: " + str(self.time) + \
       " speed rev/sec: " + str(self.speed*1E9/perRev) ) #for diagnostic
    # print counts revs /second    
    
  def resetSpeed(self):
    self.speed = 0  
    self.counter = 0
    self.lastCounter = 0
    #may need initialize since stop so 1st speed valid
    self.time = 0
    self.lastTime = 0
    
#end of Encoder class 

#Set up Encoder instances with connections, GPIO.board (swheel), 
# side = -1 if speed reported negative
sfl = Encoder("sfl", S1FL, S2FL,-1)
sfr = Encoder("sfr", S1FR, S2FR, 1)
srl = Encoder("srl", S1RL, S2RL, -1)
srr = Encoder("srr", S1RR, S2RR, 1)

GPIO.add_event_detect(sfl.s1, GPIO.BOTH,callback = sfl.callback_encoder)
GPIO.add_event_detect(sfr.s1, GPIO.BOTH,callback = sfr.callback_encoder)
GPIO.add_event_detect(srl.s1, GPIO.BOTH,callback = srl.callback_encoder)
GPIO.add_event_detect(srr.s1, GPIO.BOTH,callback = srr.callback_encoder)
GPIO.add_event_detect(sfl.s2, GPIO.BOTH,callback = sfl.callback_encoder2)
GPIO.add_event_detect(sfr.s2, GPIO.BOTH,callback = sfr.callback_encoder2)
GPIO.add_event_detect(srl.s2, GPIO.BOTH,callback = srl.callback_encoder2)
GPIO.add_event_detect(srr.s2, GPIO.BOTH,callback = srr.callback_encoder2)



def destroy():
    pwmOEn=1 #disable outputs of PCA9685
    GPIO.cleanup()
    
def main(): 
    while(True):
        time.sleep(1)
  
if __name__ == '__main__':
    try:
      main()
    except KeyboardInterrupt:
      stop_car() #stop movement
      destroy()  #clean up GPIO
      print("\nStopped and cleanup done")    