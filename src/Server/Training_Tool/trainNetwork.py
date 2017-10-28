
# TODO
# Save model on file server
# Cache datasets
# Log results in CSV
# Take in augmentation stuff

import csv
import numpy as np
import imageio
import cv2
import os
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from keras.callbacks import ModelCheckpoint, RemoteMonitor
from keras.models import load_model

## Add Sibling directory to PATH
import sys, os
sys.path.append(os.path.abspath("../../../src/Model"))
# Import model from model.py
from model import v1, preprocess_camera, preprocess_steering, mean_precision_error, cfg

# Location of training data
base_dir = "/remote/rs/ecpeprime/training_data/"

# Generate batches of data
# Randomly Drop near zero batches
def gen(samples, batch_size=32):

    while 1: # Loop forever so the generator never terminates
        shuffle(samples)

        images = []
        labels = []

        for sample in samples:
            # Extract steering
            steering = preprocess_steering(float(sample["steering"]))

            # Randomly drop near zero steering values
            if(abs(steering) < 0.1 and np.random.rand() < 0.7):
                continue

            # read in image
            image = imageio.imread(base_dir + sample["img_file"])
            image = preprocess_camera(image)

            images.append(image)
            labels.append(steering)

            #return batch
            if(len(images) >= batch_size):
                X = np.array(images)
                y = np.array(labels)
                images = []
                labels = []
                yield shuffle(X,y)



def trainOn(modelData, config=""):
      train_samples = []
      test_samples = []
      print("Caching Files...")

      print("Parsing CSV")
      # Iterate through each dataset
      for dataset in modelData["datasets"]:
            #'augmentations': {'simple_uniform': False, 'skew': False, 'bin_uniform': False}

            date = dataset["date"]
            if not "use" in dataset:
                continue
            use = dataset["use"]

            # Iterate through each batch
            path, batches, files = os.walk(base_dir + date).__next__()
            for batch in batches:
                with open(base_dir + date + "/" + batch + "/data.csv") as f:
                    reader = csv.reader(f, skipinitialspace=True)
                    header = next(reader)
                    if use == "train":
                        train_samples += [dict(zip(header, map(str, row))) for row in reader]
                    elif use == "test":
                        test_samples += [dict(zip(header, map(str, row))) for row in reader]
                    elif use == "split":
                        temp_samples = [dict(zip(header, map(str, row))) for row in reader]
                        temp_samples = shuffle(temp_samples)
                        temp_train_samples, temp_test_samples = train_test_split(temp_samples, test_size=0.3)
                        train_samples += temp_train_samples
                        test_samples += temp_test_samples


      '''
      # Bin data based on steering angle
      print("Binning data")
      num_bins = 313
      train_bins,train_max_bin_size = bin_samples(train_samples,num_bins)
      test_bins,test_max_bin_size = bin_samples(test_samples,num_bins)
      '''

      # Training parameters
      batch_size = 64
      epochs = 50
      #train_epoch_size = int(len(train_samples) * (num_bins/420)/ batch_size) * batch_size
      #test_epoch_size = int(len(test_samples) * (num_bins/270) / batch_size) * batch_size
      train_epoch_size = len(train_samples)
      test_epoch_size = len(test_samples)
      print("Training samples: {}".format(train_epoch_size))
      print("Testing samples: {}".format(test_epoch_size))

      # Create generators
      train_generator = gen(train_samples, batch_size=batch_size)
      validation_generator = gen(test_samples, batch_size=batch_size)

      # Remote callback
      remote = RemoteMonitor(root='http://0.0.0.0:8080', path='/keras/callback/', field='data', headers=None)

      # Checkpoint callback
      best_model_path= "../../Model/pretrained_models/model.best.h5"
      model_path = "../../Model/pretrained_models/model.h5"
      checkpoint = ModelCheckpoint(best_model_path, monitor='val_loss', verbose=1, save_best_only=True)

      # model
      model = None
      print("loading model...")
      if  os.path.exists(best_model_path):
          print("Found model in progress. Resuming")
          model = load_model("best_model_path",custom_objects={'mean_precision_error': mean_precision_error})
      else:
          print("No model found. Creating new model")
          model = v1()
      model.summary()

      # fit model
      print("Fitting model")
      model.fit_generator(train_generator, samples_per_epoch= train_epoch_size, validation_data=validation_generator, nb_val_samples=test_epoch_size, nb_epoch=epochs,callbacks=[checkpoint, remote])

      model.save(model_path)
      print('Training thread all done')

'''
import os
from time import sleep

from dataManage import writeModelData

def trainOn(modelData, resultNumbers=[]):
      for dataset in modelData["datasets"]:
            print("dataset: " + str(dataset))
      num = 100
      resultNumbers.append(num)
      while (num > 1):
            num = num / 1.5
            print("epoch - globalNum is " + str(num))
            resultNumbers.append(num)
            sleep(10)
      print ('training thread all done')
      #store resultNumbers in a file somewhere, along with ModelName, notes, etc.
      del resultNumbers[:]
      return

#writeModelData(modelData):
      #{"stats":{"loss":"100", "epochs":"6h45"}, "modelName":"modelName"}
'''
