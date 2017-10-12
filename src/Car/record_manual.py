# Collect training from a manual driver
import sys, os
sys.path.append(os.path.abspath("../Comms"))
# Import Car class from Car.py
from Car import Car
import ocam
import time
from datetime import datetime
import shutil


# TODO
# Use Ocam - figure out format
# Mount network drive
# Record all channels and timestamp
# Create save_entry function


print( " Autonomous Prime - Collect Training Data " )
print( " Please type information and press enter (simply press enter to stick to defaults or leave blank) ")

directory = raw_input('Mapped Network Drive: (Default: \\h01.ece.iastate.edu/ecpeprime/training_data) ') or "//h01.ece.iastate.edu/ecpeprime/training_data"
recorders = raw_input('Who is capturing the data? ') or ""
location =  raw_input('Where are you recording? ') or ""
batch_size = int(raw_input('What batch size do you want? (Default: 64) ') or 64)
obstacles = raw_input('Obstacles (low, med, high): ') or ""
pedestrians = raw_input('Pedestrians (low, med, high): ') or ""
tags = raw_input('Tags (separated by commas): ') or ""
notes = raw_input('Any Notes: ') or ""


# folders contain batch_size photos, framerate is number of photos per folder
run_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
if not os.path.exists(directory + "/" + run_name):
    os.makedirs(directory + "/" + run_name)# name describing this run
metadata = open(directory+ "/" + run_name + "/metadata.txt", 'w')

metadata.write(" Recorded by: " + recorders + "~")
metadata.write(" Location: " + location + "~")
metadata.write(" Batch Size: " + str(batch_size) + "~")
metadata.write(" Obstacles: " + obstacles + "~")
metadata.write(" Pedestrians: " + pedestrians + "~")
metadata.write(" Tags: " + tags + "~")
metadata.write(" Notes: " + notes + "~")
metadata.write(" Date: " + run_name + "~")

# Connect to car
car = Car()
car.connect(port="/dev/ttyACM0")
print("Waiting to hear from vehicle...")
while(not car.connected):
    time.sleep(0.05)
print("Car is connected!")


# locate camera
devpath = ocam.FindCamera('oCam')
cam = ocam.oCams(devpath, verbose=0)
# set format to 1280*720. Must be set before starting the camera
cam.Set(fmtlist[1])
# Open camera
cam.Start()
# Clear Camera buffer
for i in range(0,10):
    cam.GetFrame()
print("Camera is open")

# State Variables
count = 0
batch_num = 0;

try:
    while True:
        if count % batch_size == 0:
            if (count > 0) :
                data.close()
                batch_num += 1
                count = 0
            if not os.path.exists(directory + "/" + run_name + "/" + str(batch_num)):
                os.makedirs(directory + "/" + run_name + "/" + str(batch_num))# name describing this run
            data = open(directory + "/" + run_name + "/" + str(batch_num) + "/data.txt", 'w')

        # Capture Frame
        image = cam.GetFrame()
        # Read RC input from user
        channels = car.channels_in;
        steering_command = channels["steering"]
        # Save entry
        cv2.imwrite(directory+ "/" + run_name + "/" + str(batch_num) + "/%d.jpg" %count, image)
        data.write(str(steering_command) + " " + str(count) + ".jpg\n")

        count += 1

        time.sleep(.2)


finally:
    data.close()
    metadata.close()
    if (count < batch_size - 1):
        shutil.rmtree(directory + "/" + run_name + "/" + str(batch_num))

    print ("Done!")
    cam.Stop()
    car.close()
