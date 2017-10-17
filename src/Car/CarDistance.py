## add sibling directory to path
import sys, os
sys.path.append(os.path.abspath("../Comms"))
# import car class from car.py
from Car import Car
import time

if __name__ == '__main__':
     try:
          car = Car()
          car.connect(port="/dev/ttyACM0")
          print("Waiting to hear from vehicle...")
          
          #wait to hear from vehicle
          while(not car.connected):
               time.sleep(0.05)
          print('connected')
          
          car.control(throttle=1500, steering=1500, aux1=3000, aux2=4000)
          time.sleep(3)
          print("Find 20% marker")
          
          '''
          for i in range(1500,1300,-1):
               car.control(throttle=i, steering=1500, aux1=3000, aux2=4000)
               time.sleep(0.2)
               #print("throttle: "+str(i))
               mode = car.mode
               print("Throttle {} mode: {}".format(i,mode)) 
               #print("Throttle {} {}".format(i,j))
          '''
          print("Distance Test")

          
          # start of range 1445 - 1440 (1440 is safeish)
          '''
          for i in range(0,500,1):
               car.control(throttle=1500, steering=1500-i, aux1=3000, aux2=4000)
               time.sleep(0.04)
               print("i value: {}  mode: {}".format((1500-i),car.mode))

          print("Traversed Distance")

          print(car.errors)
          '''
          #1220 & 1720 are max steering
          
          
          #acceleration
          car.control(throttle=1445)
          time.sleep(1.0)
          #turn
          car.control(throttle=1445, steering=1360, aux1=3000, aux2=4000)
          time.sleep(0.5)
          #straight
          
          #car.control(throttle=1445, steering=1500, aux1=3000, aux2=4000)
          #time.sleep(0.2)
          
          #turn
          car.control(throttle=1445, steering=1640, aux1=3000, aux2=4000)
          time.sleep(0.5)
          #coast
         # car.control(throttle=1500, steering=1500, aux1=3000, aux2=4000)
         # time.sleep(1.0)
          #brake
          car.control(throttle=2000, steering=1500, aux1=3000, aux2=4000)
          time.sleep(0.2)
          car.control(throttle=1500, steering=1500, aux1=3000, aux2=4000)          
          
          print("Traversed Distance")


     finally:
          car.close() 
