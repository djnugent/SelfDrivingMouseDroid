import cv2
import time

from Car import Car 

# folder setup
folder = "training_data"
iteration = "1"
f = open(folder+ "\\" + iteration + "\data.txt", 'w')

# car setup
car = Car()
car.connect(port="COM8")
print("Waiting to hear from vehicle...")

while(not car.connected):
    time.sleep(0.05)
print("Car is connected!")


# video setup
cap = cv2.VideoCapture(1)
count = 0
success = True

time_prev = time.time()
images_per_second = 1 #change this!!
time_span = 1 / images_per_second 

while success:
    time_cur = time.time()
    if ((time_cur - time_prev) > time_span):
        
        success,image = cap.read()

        #resize image

        channels = car.channels_in;
        steering_command = channels["steering"]

        print 'Read a new frame: ', success

        cv2.imshow("feed", image);
        cv2.imwrite(folder+ "\\" + iteration + "\%d.jpg" % count, image)

        f.write(str(steering_command) + " " + str(count) + ".jpg\n")

        count += 1

        time_prev = time_cur;
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
f.close()
cv2.destroyAllWindows()

