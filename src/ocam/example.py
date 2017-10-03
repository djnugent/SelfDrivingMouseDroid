#! /usr/bin/env python3

import ocam
import time
     
# locate camera 
devpath = ocam.FindCamera('oCam')
cam = ocam.oCams(devpath, verbose=0)
print(">>Found camera ",cam.GetName())

# print available formats
print('>>Format List')
fmtlist = cam.GetFormatList()
for fmt in fmtlist:
    print('\t', fmt)

# print available controls
print('>>Control List')
ctrlist = cam.GetControlList()
for key in ctrlist:
    print('\t', key, '\tID:', ctrlist[key])


# set format to 1280*720. Must be set before starting the camera
cam.Set(fmtlist[1])

print(">>Opening camera")
# Open camera    
cam.Start()


frames = 60

try:
 
    # capture 60 frames
    print(">>Capturing", frames, "frames at 1280x720")

    # first 3 frames are usually corrupt

    start = time.time()
    for i in range(frames):

        #example code for camera control
        #val = cam.GetControl(ctrlist['Exposure (Absolute)'])
        #cam.SetControl(ctrlist['Exposure (Absolute)'], 2)

        # capture grayscale frame
        gray = cam.GetFrame()
  
      
    #calculate average fps
    print('>>Result Frame Per Second:', frames/(time.time()-start))


finally:
    cam.Stop()  
    cam.Close()





