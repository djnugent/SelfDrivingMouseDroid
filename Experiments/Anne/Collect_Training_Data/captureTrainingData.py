import cv2
import time

from Car import Car
if __name__ == "__main__" :

    


    # folder setup
    # folders contain 1s each, framerate is number of photos per folder
    framerate = 64 # frames per minute
    directory = "training_data" # directory this all ends up in
    run_name = "1" # name describing this run
    f = open(directory+ "/" + run_name + "/data.txt", 'w')
    metadata = open(directory+ "/" + run_name + "/metadata.txt", 'w')

    recorders = input('Who is capturing the data? ')
    location = input('Where are you recording?')
    framerate = input('What framerate are you using? ')
    obstacles = input('Obstacles (low, med, high): ')
    pedestrians = input('Pedestrians (low, med, high) ')
    tags = input('Tags:')
    notes = input('Any Notes: ')

    metadata.write("Recorded by: " + recorders + "\n")
    metadata.write("Location: " + location + "\n")
    metadata.write("Framerate: " + framerate + "\n")
    metadata.write("Obstacles: " + obstacles + "\n")
    metadata.write("Pedestrians: " + pedestrians + "\n")
    metadata.write("Tags: " + tags + "\n")
    metadata.write("notes: " + notes + "\n")

    # car setup
    car = Car()
    car.connect(port="/dev/ttyACM0")
    print("Waiting to hear from vehicle...")

    while(not car.connected):
        time.sleep(0.05)
    print("Car is connected!")


    # video setup
    cap = cv2.VideoCapture(1)
    count = 0
    success = True

    try:
        while True:

            if count % framerate == 0:
                sub = str(count % framerate);
                
            success,image = cap.read()

            if success:

                image = cv2.resize(image, (0,0), fx=0.5, fy=0.5) 

                channels = car.channels_in;
                steering_command = 0 #channels["steering"]
                
                # print ('Read a new frame: ', count, steering_command)

                # cv2.imshow("feed", image);
                cv2.imwrite(directory+ "/" + run_name + "/" + sub + "/%d.jpg" %count, image)
                # change to datestamp and get rid of count?
                # datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                f.write(str(steering_command) + " " + str(count) + ".jpg\n")

                count += 1


            time.sleep(.2)

    finally:
        print ("Done!")
        cap.release()
        car.close()
        f.close()
        cv2.destroyAllWindows()

