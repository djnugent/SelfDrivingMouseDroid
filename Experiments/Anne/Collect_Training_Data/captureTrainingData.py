import cv2
import time

from Car import Car 

# folder setup
folder = "training_data"
iteration = "1"
f = open(folder+ "\\" + iteration + "\data.txt", 'w')

# car setup
car = Car()
car.connect(port="COM3")
#print("Waiting to hear from vehicle...")

while(not car.connected):
    time.sleep(0.05)
#print("Car is connected!")


# video setup
cap = cv2.VideoCapture(1)
count = 0
success = True

time_prev = time.time()
images_per_second = 1 #change this!!
time_span = 1 / images_per_second 

try:
    while success:
        time_cur = time.time()
        if ((time_cur - time_prev) > time_span):
            
            success,image = cap.read()

            image = cv2.resize(image, (0,0), fx=0.5, fy=0.5) 

            channels = car.channels_in;
            steering_command = channels["steering"]
            #steering_command = 0
            
            #print 'Read a new frame: ', success

            #cv2.imshow("feed", image);
            cv2.imwrite(folder+ "\\" + iteration + "\%d.jpg" % count, image)

            f.write(str(steering_command) + " " + str(count) + ".jpg\n")

            count += 1

            time_prev = time_cur;
        
        #if cv2.waitKey(1) & 0xFF == ord('q'):
         #   break

finally:
    cap.release()
    f.close()
    cv2.destroyAllWindows()

