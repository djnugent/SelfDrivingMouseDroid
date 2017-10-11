from Car import Car
import time

#can use the sys and getopt libraries to support command line arguments
#allow for manual computer entry, or taking in a file 
if __name__ == '__main__':
    try:
        car = Car()

        #connect
        car.connect(port="COM5")

        print("Waiting to hear from vehicle...")

        #wait to hear from vehicle
        while(not car.connected):
            time.sleep(0.05)
        print('connected')

        #change modes
        print("Current mode is: {}".format(car.mode))
        print("Switching to auto mode...")
        car.set_mode('auto')
        while(car.mode != 'auto'):
            time.sleep(0.05)
        print("Car is in auto mode")
		
		#loop for user interaction if applicable, else loop for using a file
		# response = input("enter distance or 'q' to quit: ")
		
		#calculate the time it will take to reach the distance & when it will turn/be straight
		#send maneuver for angling to a 25 degree angle/10 degree angle
		
    finally:
    #close connection
    car.close()