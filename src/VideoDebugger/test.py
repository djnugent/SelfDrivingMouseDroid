from VideoDebugger import imshow
import cv2
import numpy as np
import time

frame_rate = 10
i = 0

while True:
    # create test images
    img = np.zeros((480,640,3))
    cv2.putText(img,'Test image: ' + str(i),(10,200), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)

    #print frame number
    print "frame: " + str(i)

    #display image
    imshow(img)
    time.sleep(1.0/frame_rate)
    i += 1
