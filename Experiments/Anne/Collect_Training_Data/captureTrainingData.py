import cv2
import time
from datetime import datetime
import os
import shutil

from Car import Car
if __name__ == "__main__" :

    print( " Autonomous Prime - Collect Training Data " )
    print( " Please type information and press enter (simply press enter to stick to defaults or leave blank) ")

    directory = raw_input('Mapped Network Drive: (Default: \\h01.ece.iastate.edu/ecpeprime/training_data) ') or "//h01.ece.iastate.edu/ecpeprime/training_data"
    recorders = raw_input('Who is capturing the data? ') or ""
    location =  raw_input('Where are you recording? ') or ""
    batch_size = int(raw_input('What batch size do you want? (Default: 64) ') or 64)
    obstacles = raw_input('Obstacles (low, med, high): ') or ""
    pedestrians = raw_input('Pedestrians (low, med, high): ') or ""
    tags = raw_input('Tags (separated by commas): ') or ""
    notes = raw_input('Any Notes: ') or ""


    # folders contain batch_size photos, framerate is number of photos per folder
    run_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    if not os.path.exists(directory + "/" + run_name):
        os.makedirs(directory + "/" + run_name)# name describing this run
    metadata = open(directory+ "/" + run_name + "/metadata.txt", 'w') 
    
    metadata.write(" Recorded by: " + recorders + "~")
    metadata.write(" Location: " + location + "~")
    metadata.write(" Batch Size: " + str(batch_size) + "~")
    metadata.write(" Obstacles: " + obstacles + "~")
    metadata.write(" Pedestrians: " + pedestrians + "~")
    metadata.write(" Tags: " + tags + "~")
    metadata.write(" Notes: " + notes + "~")
    metadata.write(" Date: " + run_name + "~")

    # car setup
    #car = Car()
    #car.connect(port="/dev/ttyACM0")
    print("Waiting to hear from vehicle...")

    #while(not car.connected):
     #   time.sleep(0.05)
    print("Car is connected!")


    # video setup
    cap = cv2.VideoCapture(1)
    count = 0
    success = True

    batch_num = 0;

    try:
        while True:

            if count % batch_size == 0:
                if (count > 0) :
                    data.close()
                    batch_num += 1
                    count = 0
                if not os.path.exists(directory + "/" + run_name + "/" + str(batch_num)):
                    os.makedirs(directory + "/" + run_name + "/" + str(batch_num))# name describing this run
                data = open(directory + "/" + run_name + "/" + str(batch_num) + "/data.txt", 'w')
                
            success,image = cap.read()

            if success:

                image = cv2.resize(image, (0,0), fx=0.5, fy=0.5) 

                #channels = car.channels_in;
                steering_command = 0# channels["steering"]
                
                # print ('Read a new frame: ', count, steering_command)

                # cv2.imshow("feed", image);
                cv2.imwrite(directory+ "/" + run_name + "/" + str(batch_num) + "/%d.jpg" %count, image)

                data.write(str(steering_command) + " " + str(count) + ".jpg\n")

                count += 1


            time.sleep(.2)
            

    finally:
        data.close()
        metadata.close()
        if (count < batch_size - 1):
            shutil.rmtree(directory + "/" + run_name + "/" + str(batch_num))

        
        print ("Done!")
        cap.release()
        #car.close()
        
        cv2.destroyAllWindows()

