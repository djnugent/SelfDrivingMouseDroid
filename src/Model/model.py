import cv2
from keras.models import Sequential, Model
from keras.layers import BatchNormalization
from keras.layers.core import Dense, Dropout, Activation, Flatten, Reshape
from keras.layers.convolutional import Convolution2D
from keras import backend as K
import numpy as np


# Constants
class Object(object):
    pass
cfg = Object()
cfg.rows = 100
cfg.cols = 100
cfg.num_chan = 1
cfg.roi = ((170,190),(1110,590)) # ((left,top),(right,bottom))

# Prep data before it enters the network
def preprocess_camera(img):
    #crop
    img = img[cfg.roi[0][1]:cfg.roi[1][1],cfg.roi[0][0]:cfg.roi[1][0]]
    # resize
    img = cv2.resize(img,(cfg.rows,cfg.cols))[:,:,None]
    # Mean zero
    img = img/127.5 -1.
    return img

# Normalize data before it enters the network
# Zero mean, stdev = 1
def preprocess_steering(val):
    return (val - 1500) /500.0

# Scale data from network for arduino
def postprocess_steering(val):
    return int(val * 500.0 + 1500)

# Custom lost function - Amplifies errors that occur near zero
def mean_precision_error(y_true, y_pred):
    return K.mean(K.square(y_pred - y_true)/(K.abs(y_true) + 0.1), axis=-1)

# Uses ReLu instead of ELU because Relu is faster
# Uses batch normalization to help generalize
# Uses dropout to help generalize
def v1():
    model = Sequential()
    # Block - conv
    model.add(Convolution2D(16, 8, 8, border_mode='valid', subsample=[4,4], activation='relu', name='Conv1',input_shape=(cfg.rows,cfg.cols,cfg.num_chan)))
    model.add(BatchNormalization())
    # Block - conv
    model.add(Convolution2D(36, 5, 5, border_mode='valid', subsample=[2,2], activation='relu', name='Conv2'))
    model.add(BatchNormalization())
    # Block - conv
    model.add(Convolution2D(64, 5, 5, border_mode='valid', subsample=[2,2], activation='relu', name='Conv3'))
    model.add(BatchNormalization())
    # Block - flatten
    model.add(Flatten())
    model.add(Dropout(0.35))
    # Block - fully connected
    model.add(Dense(512, activation='relu', name='FC1'))
    model.add(Dropout(0.5))
    # Block - fully connected
    model.add(Dense(256, activation='relu', name='FC2'))
    model.add(Dropout(0.5))
    # Block - output - linear
    model.add(Dense(1, name='output'))
    model.compile(loss='mse', optimizer='adam')
    return model
