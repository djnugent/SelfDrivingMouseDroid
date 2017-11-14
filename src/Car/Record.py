import time
import json
from datetime import datetime
import multiprocessing
import shutil
import imageio
import ocam
import threading
import sys, os



########### CONFIG ######################
# Port for Arduino
#port = "/dev/ttyACM0"
# Local temporary directory for storing dataset
#directory = '/home/odroid/training_data_tmp'
# Record rate
#record_rate = 9 #fps
#Mode: 0 = manual, 1 = auto
#record_mode = 0
#Thread for recording
#thread = None
#Camera object
#cam = None
#running variables
#isRunning = False
#stopRunning = False
#recording = False
########### END CONFIG ##################

class Record():
    
    def __init__(self):
        #define variables here
        mgr = multiprocessing.Manager()
        self.stop_lock = mgr.Lock()
        self.running_lock = mgr.Lock()
        self.isRunning = False
        self.stopRunning = False
        self.recording = False
        # Connect to Camera
        self.batch_size = 0
        self.cam = None
        self.thread = None
        self.record_mode = 0
        self.record_rate = 9
        self.directory = '/home/odroid/training_data_tmp'
        self.port = "/dev/ttyACM0"
        self.run_name = None
        # locate camera 
        devpath = ocam.FindCamera('oCam')
        if(devpath is None):
            sys.exit()
        self.cam = ocam.oCams(devpath, verbose=0)
        # set format to 1280*720. Must be set before starting the camera
        self.cam.Set((b'Greyscale 8-bit (Y800)', 1280, 720, 60))
        # Open camera    
        print(">> Opening camera")
        self.cam.Start()
        # Clear camera buffer. First few frames are usually corrupt
        for i in range(0,10):
            self.cam.GetFrame()
        print(">> Camera Open")
        
        # Tag this recording with extra info
        metadata = {}
        print( ">> Please type information and press enter (simply press enter to stick to defaults or leave blank) ")
        metadata["recorders"] = (input('<< Who is capturing the data? ') or "").lower()
        metadata["location"] =  (input('<< Where are you recording? ') or "").lower()
        self.batch_size = int(input('<< What batch size do you want? (Default: 128) ') or 128)
        metadata["batch_size"] = self.batch_size
        metadata["obstacles"] = (input('<< Obstacles (low, med, high): ') or "").lower()
        metadata["pedestrians"] = (input('<< Pedestrians (low, med, high): ') or "").lower()
        metadata["tags"] = (input('<< Tags (separated by commas): ') or "").lower()
        metadata["notes"] = (input('<< Any Notes: ') or "").lower()


        print('>> Writing metadata...') 
        # Create Folder for this Run based on current timestamp
        self.run_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        metadata["date"] = self.run_name
        if not os.path.exists(self.directory + "/" + self.run_name):
            os.makedirs(self.directory + "/" + self.run_name)# name describing this run
        metadata_file = open(self.directory+ "/" + self.run_name + "/metadata.txt", 'w') 
        json.dump(metadata, metadata_file)

        
        
    def close(self):
        #close all files and do any finishing work here
        self.stop_recording()
        self.recording = False
    
    def set_mode(self,mode):
        self.record_mode = mode
        
    #def set_metadata_from_file(file):
        #read in the metadata from a file
        #check with user to see if the information is correct
        
    def start_recording(self,car):
        #check to see what mode it is in, call proper recording method 
        if self.record_mode is None:
            self.thread = threading.Thread(target=self.manual_recording, args=(car,))
        else:
            self.thread = threading.Thread(target=self.auto_recording, args=(car,))
            #auto_recording(car)
        # self.recording = True
        self.thread.start()
        
    def manual_recording(self,car):
        #manual recording method
        # Start recording
        frame_count = 0
        batch_num = 0
        last_entry = 0
        data = None
        self.isRunning = True
        print(">> Recording")
        try:
            # Record while we are connected or until ctrl-c
            while car.connected:
                with self.running_lock:
                    if self.recording and self.stopRunning:
                        if data is not None:
                            data.close()
                            data = None
                            self.recording = False
                            self.isRunning = False
                            break
                # Only record in manual mode
                if car.mode != "manual":
                    if recording:
                        # Close last batch
                        if data is not None:
                            data.close()
                            data = None
                        self.recording = False
                    print(">> Switch into MANUAL mode to start recording")
                    time.sleep(0.3)
                        
                else:
                    # Check to see if we should create a new batch
                    if frame_count == self.batch_size or not self.recording:
                        print(">> Creating new batch")
                        self.recording = True
                        # Close last batch
                        if data is not None:
                            data.close()
                            data = None
                        # Create new batch
                        batch_dir = self.directory + "/" + self.run_name + "/" + str(batch_num)
                        if not os.path.exists(batch_dir):
                            os.makedirs(batch_dir)

                        # Open data file and add header
                        data = open(batch_dir + "/data.csv", 'w')
                        data.write("timestamp,img_file,steering,throttle,aux1,aux2,mode\n")

                        # update state
                        batch_num += 1
                        frame_count = 0
                       

                    # Record data at certain frequency
                    if time.time() - last_entry > 1.0/self.record_rate:
                        # Timestamp entry            
                        timestamp = time.time()
                        
                        # Get RC Controller channels
                        channels = car.channels_in;
                        mode = car.mode;
                        
                        # grab image
                        image = self.cam.GetFrame()

                        # Save image - subtract 1 from batch number because batch_number is actually next batch number
                        img_file = "{}/{}/{}.png".format(self.run_name,str(batch_num-1),str(frame_count)) 
                        imageio.imwrite(self.directory + "/" + img_file,image,compression=1)
                       
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
            self.cam.Close()
            
            

        
    def auto_recording(self,car):
        #auto recording method
                # Start recording
        frame_count = 0
        batch_num = 0
        last_entry = 0
        data = None
        self.isRunning = True
        # self.recording = False
        print(">> Recording")
        try:
            # Record while we are connected or until ctrl-c
            while car.connected:
                with self.running_lock:
                    if self.recording and self.stopRunning:
                        if data is not None:
                            data.close()
                            #data = None
                            self.recording = False
                            self.isRunning = False
                            break
                # Only record in auto mode
                print(">> car mode: {}".format(car.mode))
                if car.mode != "auto":
                    if self.recording:
                        # Close last batch
                        if data is not None:
                            data.close()
                            data = None
                        self.recording = False
                    print(">> Switch into  AUTO mode to start recording")
                    time.sleep(0.3)
                        
                else:
                    # Check to see if we should create a new batch
                    if frame_count == self.batch_size or not self.recording:
                        print(">> Creating new batch")
                        self.recording = True
                        # Close last batch
                        if data is not None:
                            data.close()
                            data = None
                        # Create new batch
                        batch_dir = self.directory + "/" + self.run_name + "/" + str(batch_num)
                        if not os.path.exists(batch_dir):
                            os.makedirs(batch_dir)

                        # Open data file and add header
                        data = open(batch_dir + "/data.csv", 'w')
                        data.write("timestamp,img_file,steering,throttle,aux1,aux2,mode\n")

                        # update state
                        batch_num += 1
                        frame_count = 0
                       

                    # Record data at certain frequency
                    if time.time() - last_entry > 1.0/self.record_rate:
                        # Timestamp entry            
                        timestamp = time.time()
                        
                        # Get RC Controller channels
                        channels = car.control_out;
                        mode = car.mode;
                        
                        # grab image
                        image = self.cam.GetFrame()

                        # Save image - subtract 1 from batch number because batch_number is actually next batch number
                        img_file = "{}/{}/{}.png".format(self.run_name,str(batch_num-1),str(frame_count)) 
                        imageio.imwrite(self.directory + "/" + img_file,image,compression=1)
                       
                        # Save entry
                        entry = "{}, {}, {}, {}, {}, {}, {}\n".format(str(timestamp),
                                                                    str(img_file),
                                                                    str(channels["steering"]),
                                                                    str(channels["throttle"]),
                                                                    str(channels["aux1"]),
                                                                    str(channels["aux2"]),
                                                                    str(mode))
                        data.write(entry)

                        # print debug
                        fps = round(1.0/(timestamp - last_entry),2)
                        print("Batch: {}, Frame: {} -- fps: {} -- mode: {}, str: {}, thr: {}, aux1: {}, aux2: {}".format(batch_num-1,frame_count,fps,mode,channels["steering"], channels["throttle"],channels["aux1"],channels["aux2"]))

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
            self.cam.Close()
            self.thread.join()
        
    def stop_recording(self):
        #stop the recording multi-threading?
        with self.running_lock:
            self.stopRunning = True
        stillRunning = True
        
        while stillRunning == True:
            time.sleep(0.05)
            with self.running_lock:
                stillRunning = self.isRunning
        
        self.recording = True
        print(">> Stopped Recording")
            
    
