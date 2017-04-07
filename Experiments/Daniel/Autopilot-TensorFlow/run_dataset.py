import tensorflow as tf
import scipy.misc
import model
import cv2
from subprocess import call
from videodebugger import imshow
import numpy as np
import time

sess = tf.InteractiveSession()
saver = tf.train.Saver()
saver.restore(sess, "save/model.ckpt")

img = cv2.imread('steering_wheel_image.jpg',0)
rows,cols = img.shape

smoothed_angle = 0

i = 0
while(True):
    full_image = scipy.misc.imread("driving_dataset/" + str(i) + ".jpg", mode="RGB")
    image = scipy.misc.imresize(full_image[-150:], [66, 200]) / 255.0
    start = time.time()
    degrees = model.y.eval(feed_dict={model.x: [image], model.keep_prob: 1.0})[0][0] * 180.0 / scipy.pi
    fps = int(1.0/(time.time()-start))
    call("clear")
    print("Predicted steering angle: " + str(degrees) + " degrees, FPS: " + str(fps))
    #make smooth angle transitions by turning the steering wheel based on the difference of the current angle
    #and the predicted angle
    smoothed_angle += 0.2 * pow(abs((degrees - smoothed_angle)), 2.0 / 3.0) * (degrees - smoothed_angle) / abs(degrees - smoothed_angle)
    M = cv2.getRotationMatrix2D((cols/2,rows/2),-smoothed_angle,1)
    dst = cv2.warpAffine(img,M,(cols,rows))
    #resize steering wheel image and add it merge it video input
    dst = cv2.resize(dst,(455,256))
    vis = np.concatenate((cv2.cvtColor(full_image, cv2.COLOR_RGB2BGR), cv2.cvtColor(dst,cv2.COLOR_GRAY2BGR)), axis=0)
    #Show image
    imshow(vis)
    i += 1


