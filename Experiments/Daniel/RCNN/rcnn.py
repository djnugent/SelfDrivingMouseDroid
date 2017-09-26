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

print("\nBuilding and compiling the model ...")

num_seq =1
seq_len = None
rows = 200
cols= 100
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

while True:

    img = np.zeros((rows,cols,1))
    start = time.time()
    model.predict(img[None,None,:,:,:])
    print("fps: ", 1.0/(time.time()-start))
