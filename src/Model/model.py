import cv2
from keras.models import Sequential, Model
from keras.layers import BatchNormalization, RELU
from keras.layers.core import Dense, Dropout, Activation, Flatten, Reshape
from keras.layers.convolutional import Convolution2D
from keras import backend as K
import numpy as np


# Constants
rows = 100
cols = 100
num_chan = 1


# Prep data before it enters the network
def preprocess_camera(img):
    roi = ((92,335),(933,651))
    #crop
    img = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
    # resize
    img = cv2.resize(img,None,fx=0.35,fy=0.35)
    # Mean zero
    img = img/127.5 -1.
    return img, roi

# Custom lost function - Amplifies errors that occur near zero
def mean_precision_error(y_true, y_pred):
    return K.mean(K.square(y_pred - y_true)/(K.abs(y_true) + 0.1), axis=-1)

# Uses ReLu instead of ELU because Relu is faster
# Uses batch normalization to help generalize
# Uses dropout to help generalize
def v1():
    model = Sequential()
    # Block - conv
    model.add(Convolution2D(16, 8, 8, border_mode='valid', subsample=[4,4], activation='relu', name='Conv1',input_shape=(None,rows,cols,num_chan)))
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
    model.summary()
