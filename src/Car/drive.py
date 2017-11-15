import time
import ocam
from keras.models import load_model
## Add Sibling directory to PATH
import sys, os
sys.path.append(os.path.abspath("../Comms"))
sys.path.append(os.path.abspath("../Model"))
# Import Car class from Car.py
from Car import Car
# Import model from model.py
from model import preprocess_camera, postprocess_steering, mean_precision_error, cfg


########### CONFIG ######################
# Port for Arduino
port = "/dev/ttyACM0"
# Model to use
model_path = "/home/odroid/models/model.best.h5"
########### END CONFIG ##################

print( ">> Autonomous Prime - CNN Drive ")

# Connect to Camera
# locate camera
devpath = ocam.FindCamera('oCam')
if(devpath is None):
    print(">> ERROR -- Camera not found")
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

# Load model
print( ">> Loading Model... ")
model = load_model(model_path,custom_objects={'mean_precision_error': mean_precision_error})

# Wait for controller to be turned on or in range
if car.channels_in["throttle"][0] < 930:
    print(">> Please connect transmitter")
while car.channels_in["throttle"][0] < 930:
    time.sleep(0.05)

try:
    # Record while we are connected or until ctrl-c
    while car.connected:
        # Run Pipeline
        if car.mode == "auto":
            # grab image
            start = time.time()
            image = cam.GetFrame()
            cam_perf = round((time.time() - start)*1000,1)

            # Preprocess image for CNN
            start = time.time()
            image = preprocess_camera(image)
            preproc_perf = round((time.time() - start)*1000,1)

            # Predict steering angle based on image
            start = time.time()
            raw_steering = model.predict(image[None,:,:,:])[0,0]
            cnn_perf = round((time.time()-start)*1000,1)

            # Post process steering value
            steering = postprocess_steering(raw_steering)

            # Control the car with user throttle and CNN steering
            throttle = car.channels_in["throttle"][0]
            car.control(throttle = throttle, steering=steering)

            # Print performance info
            perf = round(1000/(cam_perf + preproc_perf + cnn_perf),2)
            fmt = "Str: {}us, thr: {}us, fps:{}, cam: {}ms, resize: {}ms, model: {}ms"
            print(fmt.format(steering,throttle,perf,cam_perf,preproc_perf,cnn_perf))

        else:
            print(">> Please enter AUTO Mode")
            time.sleep(0.4)

    # Check to see if we ended gracefully
    if not car.connected:
        print(">> ERROR: Car disconnected")


finally:
    # close camera
    cam.Close()
    # Close connection to car
    car.close()
