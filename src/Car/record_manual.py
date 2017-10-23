import time
import json
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


## Manual data recorder for collecting datasets
# Usage:
#   - Records while in manual mode
#   - Stops recording when in failsafe mode
#   - Creates a new batch: after collection of [batch_size] samples OR if you stop recording and start again
#   - stores files locally. Use `upload.py` to upload dataset to storage server


########### CONFIG ######################
# Port for Arduino
port = "/dev/ttyACM0"
# Local temporary directory for storing dataset
directory = '/home/odroid/training_data_tmp'
# Record rate
record_rate = 9 #fps
########### END CONFIG ##################


print( ">> Autonomous Prime - Collect Training Data ")

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
metadata = {}
print( ">> Please type information and press enter (simply press enter to stick to defaults or leave blank) ")
metadata["recorders"] = (input('<< Who is capturing the data? ') or "").lower()
metadata["location"] =  (input('<< Where are you recording? ') or "").lower()
batch_size = int(input('<< What batch size do you want? (Default: 128) ') or 128)
metadata["batch_size"] = batch_size
metadata["obstacles"] = (input('<< Obstacles (low, med, high): ') or "").lower()
metadata["pedestrians"] = (input('<< Pedestrians (low, med, high): ') or "").lower()
metadata["tags"] = (input('<< Tags (separated by commas): ') or "").lower()
metadata["notes"] = (input('<< Any Notes: ') or "").lower()


print('>> Writing metadata...') 
# Create Folder for this Run based on current timestamp
run_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
if not os.path.exists(directory + "/" + run_name):
    os.makedirs(directory + "/" + run_name)# name describing this run
metadata_file = open(directory+ "/" + run_name + "/metadata.txt", 'w') 
json.dump(metadata, metadata_file)

# State variables
frame_count = 0 # count
batch_num = 0 # count
last_entry = 0 # time
data = None # File descriptor
recording = False # whether we WERE in a recording
    

# Start recording
print(">> Recording")
try:
    # Record while we are connected or until ctrl-c
    while car.connected:
        # Only record in manual mode
        if car.mode != "manual":
            if recording:
                # Close last batch
                if data is not None:
                    data.close()
                    data = None
                recording = False
            print(">> Switch into MANUAL mode to start recording")
            time.sleep(0.3)
                
        else:
            # Check to see if we should create a new batch
            if frame_count == batch_size or not recording:
                print(">> Creating new batch")
                recording = True
                # Close last batch
                if data is not None:
                    data.close()
                    data = None
                # Create new batch
                batch_dir = directory + "/" + run_name + "/" + str(batch_num)
                if not os.path.exists(batch_dir):
                    os.makedirs(batch_dir)

                # Open data file and add header
                data = open(batch_dir + "/data.csv", 'w')
                data.write("timestamp,img_file,steering,throttle,aux1,aux2,mode\n")

                # update state
                batch_num += 1
                frame_count = 0
               

            # Record data at certain frequency
            if time.time() - last_entry > 1.0/record_rate:
                # Timestamp entry            
                timestamp = time.time()
                
                # Get RC Controller channels
                channels = car.channels_in;
                mode = car.mode;
                
                # grab image
                image = cam.GetFrame()

                # Save image - subtract 1 from batch number because batch_number is actually next batch number
                img_file = "{}/{}/{}.png".format(run_name,str(batch_num-1),str(frame_count)) 
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
                print("Batch: {}, Frame: {} -- fps: {} -- mode: {}, str: {}, thr: {}, aux1: {}, aux2: {}".format(batch_num-1,frame_count,fps,mode,channels["steering"][0], channels["throttle"][0],channels["aux1"][0],channels["aux2"][0]))

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
    # Sync all buffers
    os.sync()
    # close camera
    cam.Close()
    # Close connection to car
    car.close()


    

