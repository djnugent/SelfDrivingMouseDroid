from __future__ import print_function
from keras.datasets import cifar10
from keras.utils import np_utils
from keras.preprocessing import image
from imagenet_utils import decode_predictions, preprocess_input
from VideoDebugger import imshow
from vgg16 import VGG16
import cv2
import numpy as np

(X_train, y_train), (X_test, y_test) = cifar10.load_data()
print('X_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')


model = VGG16(include_top=True, weights='vgg16_weights_tf_dim_ordering_tf_kernels.h5')

for img in X_test:
    img = cv2.resize(img,(224,224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = decode_predictions(model.predict(x))
    print(preds)
    cv2.putText(img,preds[0][0][1],(10,200), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
    imshow(img)
