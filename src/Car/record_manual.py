import time
from datetime import datetime
import shutil
import imageio
import ocam
import threading
## Add Sibling directory to PATH
import sys, os
sys.path.append(os.path.abspath("../Comms"))
# Import Car class from Car.py
from Car import Car



########### CONFIG ######################
# Port for Arduino
port = "/dev/ttyACM0"
# Local temporary directory for storing dataset
directory = '/home/odroid/training_data_tmp'
# Record rate
record_rate = 9 #fps
########### END CONFIG ##################


print( ">> Autonomous Prime - Collect Training Data " )

# Connect to Camera
# locate camera 
devpath = ocam.FindCamera('oCam')
if(devpath is None):
    sys.exit()
cam = ocam.oCams(devpath, verbose=0)

# set format to 1280*720. Must be set before starting the camera
cam.Set((b'Greyscale 8-bit (Y800)', 1280, 720, 60))
# Open camera    
print(">> Opening camera")
cam.Start()
# Clear camera buffer. First few frames are usually corrupt
for i in range(0,10):
    cam.GetFrame()
print(">> Camera Open")


# Connect to car
car = Car()
car.connect(port=port)
print(">> Waiting to hear from vehicle on ",port," ...")
while(not car.connected):
   time.sleep(0.05)
print(">> Car is connected!")
time.sleep(0.3)

# Wait for controller to be turned on or in range
if car.channels_in["throttle"][0] < 930:
    print(">> Please connect transmitter")
while car.channels_in["throttle"][0] < 930:
    time.sleep(0.05)


# Tag this recording with extra info
print( ">> Please type information and press enter (simply press enter to stick to defaults or leave blank) ")
recorders = input('<< Who is capturing the data? ') or ""
location =  input('<< Where are you recording? ') or ""
batch_size = int(input('<< What batch size do you want? (Default: 128) ') or 128)
obstacles = input('<< Obstacles (low, med, high): ') or ""
pedestrians = input('<< Pedestrians (low, med, high): ') or ""
tags = input('<< Tags (separated by commas): ') or ""
notes = input('<< Any Notes: ') or ""


print('>> Writing metadata...') 
# Create Folder for this Run based on current timestamp
run_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
if not os.path.exists(directory + "/" + run_name):
    os.makedirs(directory + "/" + run_name)# name describing this run
metadata = open(directory+ "/" + run_name + "/metadata.txt", 'w') 
# Write meta data to folder
metadata.write(recorders + "~")
metadata.write(location + "~")
metadata.write(str(batch_size) + "~")
metadata.write(obstacles + "~")
metadata.write(pedestrians + "~")
metadata.write(tags + "~")
metadata.write(notes + "~")
metadata.write(run_name + "~")
metadata.close()


# State variables
frame_count = 0
batch_num = 0
last_entry = 0

# Wait for user to switch out of failsafe mode
if car.mode == "failsafe":
    print(">> Waiting for user to switch out of failsafe mode...")
while car.mode == "failsafe":
    time.sleep(0.05)
	

# Start recording
print(">> Recording")
try:
    # Record while we are connected and not failsafed or until ctrl-c
    while car.connected and car.mode != "failsafe":

        # Check to see if we should create a new batch
        if frame_count % batch_size == 0:
            if (frame_count > 0) :
                data.close()
                batch_num += 1
                frame_count = 0

            batch_dir = directory + "/" + run_name + "/" + str(batch_num)
            if not os.path.exists(batch_dir):
                os.makedirs(batch_dir)

            # Open data file and add header
            data = open(batch_dir + "/data.csv", 'w')
            data.write("timestamp,img_file,steering,throttle,aux1,aux2,mode\n")


        # Record data at certain frequency
        if time.time() - last_entry > 1.0/record_rate:
            # Timestamp entry            
            timestamp = time.time()
            
            # Get RC Controller channels
            channels = car.channels_in;
            mode = car.mode;
            
            # grab image
            image = cam.GetFrame()

            # Save image
            img_file = "{}/{}/{}.png".format(run_name,str(batch_num),str(frame_count)) 
            imageio.imwrite(directory + "/" + img_file,image,compression=1)
           
            # Save entry
            entry = "{}, {}, {}, {}, {}, {}, {}\n".format(str(timestamp),
                                                        str(img_file),
                                                        str(channels["steering"][0]),
                                                        str(channels["throttle"][0]),
                                                        str(channels["aux1"][0]),
                                                        str(channels["aux2"][0]),
                                                        str(mode))
            data.write(entry)

            # print debug
            fps = round(1.0/(timestamp - last_entry),2)
            print("Batch: {}, Frame: {} -- fps: {} -- mode: {}, str: {}, thr: {}, aux1: {}, aux2: {}".format(batch_num,frame_count,fps,mode,channels["steering"][0], channels["throttle"][0],channels["aux1"][0],channels["aux2"][0]))

            # update state
            frame_count += 1
            last_entry = timestamp


    
    # Check to see if we ended gracefully
    if not car.connected:
        print(">> ERROR: Car disconnected. Stopped recording") 
    if car.mode == "failsafe":
        print(">> ERROR: Car went into failsafe mode. Stopped recording") 
        

finally:
    print (">> Done!")
    # close data file
    data.close()
    # close camera
    cam.Close()
    # Close connection to car
    car.close()


    

