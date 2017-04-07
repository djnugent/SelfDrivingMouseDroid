import numpy as np
import cv2
from matplotlib import pyplot as plt

fig = plt.figure()


img = cv2.imread('Hallway_3.jpg', cv2.IMREAD_COLOR)
a=fig.add_subplot(4,3,1)
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)
a.set_title("Original, Full Size")
plt.imshow(img)

img_small = cv2.imread('Hallway_3_small.jpg', cv2.IMREAD_COLOR)
a=fig.add_subplot(4,3,2)
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)
a.set_title("Original, Reduced Size")
plt.imshow(img_small)

img_small_blurred = cv2.blur(img_small,(4,4))
a=fig.add_subplot(4,3,3)
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)
a.set_title("Blurred, Reduced Size")
plt.imshow(img_small_blurred)


grayscale_img = None
grayscale_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# #### ORB ####
# Initiate STAR detector
orb = cv2.ORB_create()
# find the keypoints with ORB
kp = orb.detect(img,None)
# compute the descriptors with ORB
kp, des = orb.compute(img, kp)
# draw only keypoints location,not size and orientation
orb_img = None
orb_img = cv2.drawKeypoints(img,kp,orb_img,color=(255,0,0), flags=0)
a=fig.add_subplot(4,3,4)
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)
a.set_title("ORB")
plt.imshow(orb_img)

# #### Harris Corner ####
gray = np.float32(grayscale_img)
dst = cv2.cornerHarris(gray,2,3,0.04)
#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)
# Threshold for an optimal value, it may vary depending on the image.
hc_img = img.copy()
hc_img[dst>0.005*dst.max()]=[255,0,0]
a=fig.add_subplot(4,3,7)
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)
a.set_title("Harris Corner")
plt.imshow(hc_img)

# #### Hough Lines using Canny Edge ####
E = cv2.Canny(grayscale_img, 50, 200, 3)
lines = cv2.HoughLinesP(E,rho = 1,theta = 1*np.pi/180,threshold = 80,minLineLength = 30,maxLineGap = 10)
N = lines.shape[0]
hough_img = img.copy()
for i in range(N):
    x1 = lines[i][0][0]
    y1 = lines[i][0][1]    
    x2 = lines[i][0][2]
    y2 = lines[i][0][3]    
    cv2.line(hough_img,(x1,y1),(x2,y2),(255,0,0),3)
a=fig.add_subplot(4,3,10)
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)
a.set_title("Hough Lines")
plt.imshow(hough_img)



# ######### Reduced Size Image ########
grayscale_img_small = None
grayscale_img_small = cv2.cvtColor(img_small, cv2.COLOR_RGB2GRAY)

# #### ORB ####
# Initiate STAR detector
orb = cv2.ORB_create()
# find the keypoints with ORB
kp = orb.detect(img_small,None)
# compute the descriptors with ORB
kp, des = orb.compute(img_small, kp)
# draw only keypoints location,not size and orientation
orb_img = None
orb_img = cv2.drawKeypoints(img_small,kp,orb_img,color=(255,0,0), flags=0)
a=fig.add_subplot(4,3,5)
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)
a.set_title("ORB")
plt.imshow(orb_img)

# #### Harris Corner ####
gray = np.float32(grayscale_img_small)
dst = cv2.cornerHarris(gray,2,3,0.04)
#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)
# Threshold for an optimal value, it may vary depending on the image.
hc_img = img_small.copy()
hc_img[dst>0.005*dst.max()]=[255,0,0]
a=fig.add_subplot(4,3,8)
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)
a.set_title("Harris Corner")
plt.imshow(hc_img)

# #### Hough Lines using Canny Edge ####
E = cv2.Canny(grayscale_img_small, 50, 200, 3)
lines = cv2.HoughLinesP(E,rho = 1,theta = 1*np.pi/180,threshold = 80,minLineLength = 30,maxLineGap = 10)
N = lines.shape[0]
hough_img = img_small.copy()
for i in range(N):
    x1 = lines[i][0][0]
    y1 = lines[i][0][1]    
    x2 = lines[i][0][2]
    y2 = lines[i][0][3]    
    cv2.line(hough_img,(x1,y1),(x2,y2),(255,0,0),3)
a=fig.add_subplot(4,3,11)
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)
a.set_title("Hough Lines")
plt.imshow(hough_img)


# ######### Reduced Size Blurred Image ########
grayscale_img_small_blurred = None
grayscale_img_small_blurred = cv2.cvtColor(img_small_blurred, cv2.COLOR_RGB2GRAY)

# #### ORB ####
# Initiate STAR detector
orb = cv2.ORB_create()
# find the keypoints with ORB
kp = orb.detect(img_small_blurred,None)
# compute the descriptors with ORB
kp, des = orb.compute(img_small_blurred, kp)
# draw only keypoints location,not size and orientation
orb_img = None
orb_img = cv2.drawKeypoints(img_small_blurred,kp,orb_img,color=(255,0,0), flags=0)
a=fig.add_subplot(4,3,6)
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)
a.set_title("ORB")
plt.imshow(orb_img)

# #### Harris Corner ####
gray = np.float32(grayscale_img_small_blurred)
dst = cv2.cornerHarris(gray,2,3,0.04)
#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)
# Threshold for an optimal value, it may vary depending on the image.
hc_img = img_small_blurred.copy()
hc_img[dst>0.005*dst.max()]=[255,0,0]
a=fig.add_subplot(4,3,9)
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)
a.set_title("Harris Corner")
plt.imshow(hc_img)

# #### Hough Lines using Canny Edge ####
E = cv2.Canny(grayscale_img_small_blurred, 50, 200, 3)
lines = cv2.HoughLinesP(E,rho = 1,theta = 1*np.pi/180,threshold = 80,minLineLength = 30,maxLineGap = 10)
N = lines.shape[0]
hough_img = img_small_blurred.copy()
for i in range(N):
    x1 = lines[i][0][0]
    y1 = lines[i][0][1]    
    x2 = lines[i][0][2]
    y2 = lines[i][0][3]    
    cv2.line(hough_img,(x1,y1),(x2,y2),(255,0,0),3)
a=fig.add_subplot(4,3,12)
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)
a.set_title("Hough Lines")
plt.imshow(hough_img)


plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
