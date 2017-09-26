from keras.models import Sequential, Model
from keras.layers.core import Lambda, Dense, Activation, Flatten, Dropout
from keras.layers.convolutional import Cropping2D, Convolution2D
from keras.layers.recurrent import LSTM
from keras.layers.wrappers import TimeDistributed
from keras.layers.advanced_activations import ELU
from keras.layers.noise import GaussianNoise
from keras.optimizers import Adam
import numpy as np
import time
from ocam_fast import Camera
import cv2

print("\nBuilding and compiling the model ...")

num_seq =1
seq_len = None
rows = 150
cols= 300
num_chan = 1

model = Sequential()
# Block - conv
model.add(TimeDistributed(Convolution2D(16, 8, 8, border_mode='same', subsample=[4,4], activation='elu', name='Conv1'),batch_input_shape=(num_seq,seq_len,rows,cols,num_chan)))
# Block - conv
model.add(TimeDistributed(Convolution2D(36, 5, 5, border_mode='same', subsample=[2,2], activation='elu', name='Conv2')))
# Block - conv
model.add(TimeDistributed(Convolution2D(64, 5, 5, border_mode='same', subsample=[2,2], activation='elu', name='Conv3')))
# Block - flatten
model.add(TimeDistributed(Flatten()))
model.add(Dropout(0.2))
# Block - fully connected
model.add(Dense(512, activation='elu', name='FC1'))
model.add(Dropout(0.5))
# Block - LSTM
model.add(LSTM(256, activation='elu',stateful=True, name='LSTM1'))
model.add(Dropout(0.5))
# Block - output
model.add(Dense(1, name='output'))
model.summary()


cam = Camera(background_capture = False)
while True:

    # crop
    start = time.time()
    ret,img = cam.read()
    crop = img[:rows,:cols]
    model.predict(crop[None,None,:,:,:])
    crop_fps = 1.0/(time.time()-start)

    # resize
    start = time.time()
    ret,img = cam.read()
    resize = cv2.resize(img,(cols,rows), interpolation = cv2.INTER_AREA)[:,:,None]
    model.predict(resize[None,None,:,:,:])
    resize_fps = 1.0/(time.time()-start)

    # both
    start = time.time()
    ret,img = cam.read()
    img = img[:500,:500]
    resize = cv2.resize(img,(cols,rows), interpolation = cv2.INTER_AREA)[:,:,None]
    model.predict(resize[None,None,:,:,:])
    both_fps = 1.0/(time.time()-start)

    print("crop fps: ", crop_fps, "resize fps", resize_fps, "both", both_fps)
