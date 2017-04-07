from Car import Car
import time

if __name__ == '__main__':
    try:
        car = Car()

        #connect
        car.connect(port="COM8")
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

        # Send control commands(currently designed to echo)
        print("Controlling vehicle")
        for i in range(0,1000,10):
            car.control(throttle=1000 + i,steering=2000+i, aux1=3000+i,aux2=4000+i)
            time.sleep(0.04)
            print(car.connected,car.channels_in)
            channels = car.channels_in
            throttle = channels["steering"]

        # print pending errors
        print("Showing errors")
        print(car.errors)

    finally:
        #close connection
        car.close()
