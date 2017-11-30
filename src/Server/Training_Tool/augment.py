
import cv2
import numpy as np

# Randomly change brightness
# Randomly change contrast
# Randomly add gaussian noise
# Randomly add salt and pepper noise
# Randomly gaussian blur
def augment(sample):

    sample = sample.astype(np.float64)

    # Change contrast
    alpha = max((1 + np.random.normal(1.3, 1.0)),0.87)
    sample *= alpha

    # Change brightness
    beta = max(np.random.normal(0.0, 18.0),-35)
    sample += beta


    # randomly select type of noise or blur
    aug = np.random.randint(4)

    # gaussian Noise
    if aug == 0:
        std = abs(np.random.normal(0.0, 10))
        noise = np.zeros_like(sample)
        cv2.randn(noise,0,std)
        sample = np.add(sample,noise)
    # Salt and pepper noise
    elif aug == 1:
        prob = abs(np.random.normal(0.0, 0.02))
        rnd = np.random.rand(sample.shape[0],sample.shape[1])
        sample[rnd < prob] = 0
        sample[rnd > 1 - prob] = 255
    # gaussian blur
    elif aug == 2:
        ksize = (np.random.randint(4) + 1) * 2 + 1
        sample = cv2.GaussianBlur(sample,(ksize,ksize),0)
    # No augmentation
    else:
        pass

    sample = np.clip(sample,0,255)

    return sample.astype(np.uint8)


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




if __name__=="__main__":

    import imageio
    img = imageio.imread("9.png")

    while True:
        aug = np.copy(img)
        aug = augment(aug)
        cv2.imshow("original", img)
        cv2.imshow("augment",aug)
        cv2.waitKey(0)
