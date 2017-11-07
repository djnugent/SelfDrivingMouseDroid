
# TODO
# Save model on file server
# Cache datasets
# Take in augmentation stuff

import csv
import numpy as np
import imageio
import cv2
import os
import shutil, sys
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from keras.callbacks import ModelCheckpoint, RemoteMonitor, TensorBoard
from keras.models import load_model
from datetime import datetime
from dataManage import *

## Add Sibling directory to PATH
import sys, os
sys.path.append(os.path.abspath("../../../src/Model"))
# Import model from model.py
from model import v1, preprocess_camera, preprocess_steering, mean_precision_error, cfg

# Location of training data
remote_dir = "/remote/rs/ecpeprime/training_data/"
cache_dir = "/var/tmp/training_data/"

# Location of pretrained models
model_dir = "/remote/rs/ecpeprime/pretrained_models/"

# Location of logs
log_dir = "/remote/rs/ecpeprime/training_logs/"

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
            image = imageio.imread(cache_dir + sample["img_file"])
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


def cacheDataset(dataset,storage_directory, tmp_directory):
    dst_dir = os.path.join(tmp_directory, dataset)
    src_dir = os.path.join(storage_directory, dataset)

    # Only copy directories that don't exist
    if not os.path.exists(dst_dir):
        print("Caching dir: ", src_dir)
        os.makedirs(dst_dir, exist_ok=True)
        for src_dir, dirs, files in os.walk(src_dir):
            for subdir in dirs:
                dst_subdir = os.path.join(dst_dir, subdir)
                src_subdir = os.path.join(src_dir, subdir)

                if not os.path.exists(dst_subdir):
                    os.makedirs(dst_subdir, exist_ok=True)
                for src_subdir, subdirs, files in os.walk(src_subdir):
                    for file_ in files:
                        src_file = os.path.join(src_subdir, file_)
                        dst_file = os.path.join(dst_subdir, file_)
                        shutil.copy(src_file, dst_subdir)



def trainOn(modelData, config=""):
      train_samples = []
      test_samples = []

      model_dir = os.path.join(model_dir, modelData["name"])
      if not os.path.exists(model_dir):
          os.makedirs(model_dir, exist_ok=True)

      writeModelData(model_dir, modelData)

      print("Parsing CSV")
      # Iterate through each dataset
      for dataset in modelData["datasets"]:
            #'augmentations': {'simple_uniform': False, 'skew': False, 'bin_uniform': False}

            date = dataset["date"]
            if not "use" in dataset:
                continue
            use = dataset["use"]

            # Cache dataset if needed
            cacheDataset(date, remote_dir,cache_dir)

            # Iterate through each batch
            path, batches, files = os.walk(cache_dir + date).__next__()
            for batch in batches:
                with open(cache_dir + date + "/" + batch + "/data.csv") as f:
                    reader = csv.reader(f, skipinitialspace=True)
                    header = next(reader)
                    if use == "train":
                        train_samples += [dict(zip(header, map(str, row))) for row in reader]
                    elif use == "test":
                        test_samples += [dict(zip(header, map(str, row))) for row in reader]
                    elif use == "split":
                        temp_samples = [dict(zip(header, map(str, row))) for row in reader]
                        temp_samples = shuffle(temp_samples)
                        temp_train_samples, temp_test_samples = train_test_split(temp_samples, test_size=0.15)
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

      # Tensorboard
      log_path = log_dir + datetime.now().strftime('%m_%d_%Y--%H_%M')
      tb = TensorBoard(log_dir=log_path)

      # Checkpoint callback
      best_model_path= model_dir + "model.best.h5"
      model_path = model_dir + "model.h5"
      checkpoint = ModelCheckpoint(best_model_path, monitor='val_loss', verbose=1, save_best_only=True)

      # model
      model = None
      print("loading model...")
      if  os.path.exists(best_model_path):
          print("Found model in progress. Resuming")
          model = load_model(best_model_path,custom_objects={'mean_precision_error': mean_precision_error})
      else:
          print("No model found. Creating new model")
          model = v1()
      model.summary()

      # fit model
      print("Fitting model")
      model.fit_generator(train_generator, samples_per_epoch= train_epoch_size,\
        validation_data=validation_generator, nb_val_samples=test_epoch_size,\
        nb_epoch=epochs,callbacks=[checkpoint, tb])

      model.save(model_path)
      print('Training thread all done')

'''

#writeModelData(modelData):
      #{"stats":{"loss":"100", "epochs":"6h45"}, "modelName":"modelName"}
'''
