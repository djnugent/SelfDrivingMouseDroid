#!/usr/bin/python3.5

import os, sys, getopt, math, time
sys.path.append(os.path.abspath("../Comms"))
from Car import Car
from Record import Record

hypotenuse = 2.829
degToServo = 5
#minThrottle = 1445
minThrottle = 1555

def main():
	#define record and car variables
	 car = Car()
	 car.connect(port="/dev/ttyACM0")
     print("Waiting to hear from vehicle...")
     while(not car.connected):
          time.sleep(0.05)
     print('connected')
	 record = Record()
	 #have a while loop so multiple runs can be executed
	 while(true):
	      print("Enter a negative double to go left\nor a positive double to go right\nelse type exit to quit\n")
		  divert = (input('<< '))
		  try:
               divert = float(divert)
          
          except ValueError:
               break
		  
		  executeManeuver(divert, car, record)

def executeManeuver(dist, car, record):
     try:
          # car = Car()
          # car.connect(port="/dev/ttyACM0")
          # print("Waiting to hear from vehicle...")
          # while(not car.connected):
               # time.sleep(0.05)
          # print('connected')

          abs_dist = math.fabs(dist)
          angle = math.degrees(math.asin(dist/hypotenuse))
          delta_servo = float(angle) * degToServo
          print("delta_servo {}".format(delta_servo))

          if dist < 0:
               #subtract
               delta_servo = (-1) * delta_servo

          first_turn = 1500 + delta_servo
          second_turn = 1500 + (-1) * delta_servo
          print("first turn: {}\nsecond turn: {}".format(first_turn, second_turn))
          
          record = Record()
          record.set_mode(1)

          car.control(throttle=1500, steering=1500)
          print("Beginning maneuver")
          time.sleep(3.0)
     
          #acceleration
          car.control(throttle=minThrottle, steering=1500)
          time.sleep(1.0)
          #turn
          #car.control(throttle=minThrottle, steering=first_turn)
          car.control(throttle=minThrottle, steering=int(first_turn))
          
          time.sleep(0.5)

          #turn
          car.control(throttle=minThrottle, steering=int(second_turn))
          time.sleep(0.5)
          
          #straight
          car.control(throttle=minThrottle, steering=1500)
          #start recording
          record.start_recording(car)
          time.sleep(0.5)
          
          #turn
          car.control(throttle=minThrottle, steering=int(second_turn))
          time.sleep(0.5)
          
          #turn
          car.control(throttle=minThrottle, steering=int(first_turn))
          time.sleep(0.5)
          #straight
          car.control(throttle=minThrottle, steering=1500)
          record.stop_recording()
          time.sleep(0.3)
          #stop recording
          #brake
          car.control(throttle=1000, steering=1500)
          time.sleep(0.2)
          car.control(throttle=1500) 

     finally:
          car.close()    

if __name__ == "__main__":
     main()