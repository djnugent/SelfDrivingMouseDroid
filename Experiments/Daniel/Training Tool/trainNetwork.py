import csv
import numpy as np
import imageio
import cv2
import os
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
from time import sleep
## Add Sibling directory to PATH
import sys, os
sys.path.append(os.path.abspath("../../../src/Model"))
# Import RCNN model from model.py
from model import RCNN

'''
from model import v2, extract_camera, extract_minimap, mean_precision_error
'''

base_dir = "/remote/rs/ecpeprime/training_data/"

# Generate batches of data
# Randomly selects a bin
# Randomly samples from bin
# Randomly augment the sample
def gen(bins, batch_size=32,augment=False):
    bin_num = len(bins)
    X_camera = []
    X_minimap = []
    Y_steering = []
    while 1: # Loop forever so the generator never terminates
        # uniform random on bins
        bin_idx = np.random.randint(0,bin_num)
        bin_samples = bins[bin_idx]

        # Uniform random on samples in bin
        sample_num = len(bin_samples)
        if sample_num == 0: #empty bin
            continue
        sample_idx = np.random.randint(0,sample_num)
        sample = bin_samples[sample_idx]

        # Extract sample
        steering = float(sample["steering"])
        filename = args.dir + "/" + sample["img_file"]
        image = imageio.imread(filename)

        # Augment the sample
        if augment:
            camera_image, minimap_image, steering, viz = augment(image,steering)
        else:
            camera_image,c_roi = extract_camera(image)
            minimap_image,m_roi= extract_minimap(image)
        # Append to batch
        X_camera.append(camera_image)
        X_minimap.append(minimap_image)
        Y_steering.append(steering)

        #return batch
        if(len(X_camera) >= batch_size):
            X1 = np.array(X_camera)
            X2 = np.array(X_minimap)
            y = np.array(Y_steering)
            X_camera = []
            X_minimap = []
            Y_steering = []
            yield [X1,X2], y
            #yield {"convolution2d_input_1":X1,"convolution2d_input_2":X2},y


# Randomly shift and rotate the image
def augment(image,steering, viz = False):
    # Extract minimap
    minimap_image, m_roi = extract_minimap(image)

    #randomly skew camera image
    MAX_SHIFT = 16 #pixels
    MAX_ROT = 5 #degrees
    #TODO tune these values
    STEER_PER_SHIFT =  0.005
    STEER_PER_ROT = 0.01
    aug = np.random.randint(5)
    shift = 0
    rotation = 0
    aug_steering = steering
    skew_image = image

    # No skew
    #if aug == 0:
    # shift right
    if aug == 1:
        shift = -np.random.rand() * MAX_SHIFT
        skew_image = skew(image,0,shift)
        aug_steering = steering + shift * STEER_PER_SHIFT
    # shift left
    elif aug == 2:
        shift = np.random.rand() * MAX_SHIFT
        skew_image = skew(image,0,shift)
        aug_steering = steering + shift * STEER_PER_SHIFT
    # rotate right
    elif aug == 3:
        rotation = np.random.rand() * MAX_ROT
        skew_image = skew(image,rotation,0)
        aug_steering = steering - rotation * STEER_PER_ROT
    # rotate left
    elif aug == 4:
        rotation = -np.random.rand() * MAX_ROT
        skew_image = skew(image,rotation,0)
        aug_steering = steering - rotation * STEER_PER_ROT

    camera_image,c_roi = extract_camera(skew_image)

    # Render a visualization
    render = None
    if viz:
        render = np.copy(skew_image)
        # Text overlay
        mask = np.zeros_like(image) + 127
        alpha = 1
        cv2.rectangle(mask, (0,0), (350,150),(20, 20, 20), -1)
        cv2.addWeighted(skew_image, 1, mask, alpha,-127, render)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(render,'Extracted Camera',(420,680), font, 0.7,(220,220,220),1,cv2.LINE_AA)
        cv2.putText(render,'Extracted Minimap',(810,150), font, 0.7,(220,220,220),1,cv2.LINE_AA)
        cv2.putText(render,'User Steering: {}'.format(round(steering,3)),(10,30), font, 0.7,(220,220,220),1,cv2.LINE_AA)
        cv2.putText(render,'Shift: {} px'.format(round(shift,2)),(10,60), font, 0.7,(220,220,220),1,cv2.LINE_AA)
        cv2.putText(render,'Rotation: {} deg'.format(round(rotation,2)),(10,90), font, 0.7,(220,220,220),1,cv2.LINE_AA)
        cv2.putText(render,'Augmented Steering: {}'.format(round(aug_steering,3)),(10,120), font, 0.7,(220,220,220),1,cv2.LINE_AA)
        # PIP preprocessed camera image
        render[c_roi[0][1]:c_roi[1][1],c_roi[0][0]:c_roi[1][0]] = cv2.resize(camera_image,(841,316),interpolation=cv2.INTER_NEAREST) * 127 + 127
        cv2.rectangle(render, c_roi[0], c_roi[1],(255, 51, 51), 1)
        # PIP preprocessed minimap
        pip = cv2.resize(minimap_image,None,fx=4,fy=4,interpolation=cv2.INTER_NEAREST)
        x,y = image.shape[1] - pip.shape[1], pip.shape[0]
        render[:y,x:,0] = 0
        render[:y,x:,1] = pip * 127 + 127
        render[:y,x:,2] = 0
        cv2.rectangle(render, (x,0), (image.shape[1],y),(255, 51, 51), 1)

    return camera_image, minimap_image, aug_steering, render

def bin_samples(samples,num_bins=21):
    samples = np.array(samples)
    samples = shuffle(samples)

    #Extract steering angles
    angs = []
    for sample in samples:
        angs.append(float(sample["steering"]))

    #Bin data based on steering angle
    bin_lim = np.linspace(-1.1, 1.1, num=num_bins-1,endpoint=True)
    dig = np.digitize(angs,bin_lim,right=False)

    #place data in bins
    bins = []
    max_bin_size = 0
    for i in range(num_bins):
        idx = np.where(dig == i)
        bins.append(samples[idx])
        if len(idx[0]) > max_bin_size:
            max_bin_size = len(idx[0])

    return bins, max_bin_size

# Skew the image
# Operates in the birdseye view domain to shift and rotate the lanes
# Operates on 4 points in a square pattern then calculates transform between the original square and the skewed square and apply it to the image
# This is more confusing but more efficient because only one transform is applied the image as oppessed to 4
def skew(img, rotation, shift):
    h,w,c = img.shape

    # Create a transform between camera and birdseye view
    # Define transform parameters
    lane_width = 130 #85
    apex_width = 80 #230
    horizon0 = 415 #485
    horizon1 = 0 #610
    src = np.float32([[0,h],
                    [w,h],
                    [int(w/2 - apex_width/2),horizon0],
                    [int(w/2 + apex_width/2),horizon0]])
    dst = np.float32([[int(w/2 - lane_width/2), h],
                      [int(w/2 + lane_width/2), h],
                      [int(w/2 - lane_width/2), horizon1],
                      [int(w/2 + lane_width/2), horizon1]])
    # Calculate the transform
    M = cv2.getPerspectiveTransform(src, dst)
    inv_M = cv2.getPerspectiveTransform(dst, src)
    # Apply transform to 4 points
    original_pnts = np.array([[200,500],[555,500],[80,550],[577,550]], dtype='float32')
    warped_pnts = cv2.perspectiveTransform(np.array([original_pnts]),M)[0]

    # shift points
    x = shift
    y = 0
    trans_M = np.float32([[1,0,x],[0,1,y],[0,0,1]])
    warped_pnts_shifted = cv2.perspectiveTransform(np.array([warped_pnts]),trans_M)[0]

    # Rotate points
    center = int(w/2),h
    rot_M = cv2.getRotationMatrix2D(center,rotation,1.0)
    rot_M = np.concatenate((rot_M, np.array([[0,0,1]])), axis=0)
    warped_pnts_rot = cv2.perspectiveTransform(np.array([warped_pnts_shifted]),rot_M)[0]

    # Warp back to regular perspective
    warped_pnts_final = cv2.perspectiveTransform(np.array([warped_pnts_rot]),inv_M)[0]

    # Apply transfom to image
    final_M = cv2.getPerspectiveTransform(original_pnts, warped_pnts_final)
    # Warp the image using OpenCV warpPerspective()
    result = cv2.warpPerspective(img, final_M, (w,h))
    return result


def trainOn(trainingDatasets=[], resultNumbers=[]):
      samples = []
      print("Parsing CSV")
      # Iterate through each dataset
      for dataset in trainingDatasets:
            # Iterate through each batch
            path, batches, files = os.walk(base_dir + dataset).__next__()
            for batch in batches:
                with open(base_dir + dataset + "/" + batch + "/data.csv") as f:
                    reader = csv.reader(f, skipinitialspace=True)
                    header = next(reader)
                    samples += [dict(zip(header, map(str, row))) for row in reader]
      print("Found {} samples".format(len(samples)))

      # Split samples into training/test set
      print("Splitting data")
      samples = shuffle(samples)
      train_samples, test_samples = train_test_split(samples, test_size=0.1)

      # Bin data based on steering angle
      print("Binning data")
      num_bins = 313
      train_bins,train_max_bin_size = bin_samples(train_samples,num_bins)
      test_bins,test_max_bin_size = bin_samples(test_samples,num_bins)

      # Training parameters
      batch_size = 64
      epochs = 400
      train_epoch_size = int(len(train_samples) * (num_bins/420)/ batch_size) * batch_size
      test_epoch_size = int(len(test_samples) * (num_bins/270) / batch_size) * batch_size
      print("Training samples: {}".format(train_epoch_size))
      print("Testing samples: {}".format(test_epoch_size))

      # Create generators
      train_generator = gen(train_bins, batch_size=batch_size,augment=True)
      validation_generator = gen(test_bins, batch_size=batch_size)
      '''
      # checkpoint
      filepath="../pretrained_models/model.best.h5"
      checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True)
      callbacks_list = [checkpoint]


      # model
      model = None
      print("loading model...")
      if  os.path.exists("../pretrained_models/model.best.h5"):
          print("Found model in progress. Resuming")
          model = load_model("../pretrained_models/model.best.h5",custom_objects={'mean_precision_error': mean_precision_error})
      else:
          print("No model found. Creating new model")
          model = v2()
      print("done")

      # fit model
      print("Fitting model")
      model.fit_generator(train_generator, samples_per_epoch= train_epoch_size,\
                  validation_data=validation_generator, \
                  nb_val_samples=test_epoch_size, nb_epoch=epochs,callbacks=callbacks_list)

      model.save("../pretrained_models/model.h5")
      '''
      num = 100
      resultNumbers.append(num)
      while (num > 0):
            num = num / 1.5
            print("epoch - globalNum is " + str(num))
            resultNumbers.append(num)
            sleep(10)
      print ('training thread all done')
      return
