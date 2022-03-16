import math
import time
import sched
import numpy as np
import mecanum_py_by_wheel_encodeSpeed as drive
from simple_pid import PID

def main(): 
    # pid.output_limits = (10, 100)
    # prevRead = 0
    # while True:
    #     read = drive.fl.encoder.readSpeed()
    #     if read == prevRead:
    #         read -= 1
    #     control = pid(read)
    #     print("   " + str(read) + "   " + str(control))
    #     drive.fl.move(control)
    #     prevRead = read
    #     time.sleep(0.1)
    count = 0
    power = 50
    while True:
      drive.fl.move(power)
      drive.fr.move(power)
      drive.rl.move(power)
      drive.rr.move(power)
  
if __name__ == '__main__':
    try:
      main()
    except KeyboardInterrupt:
      drive.stop_car() #stop movement
      drive.destroy()  #clean up GPIO
      print("\nStopped and cleanup done")   