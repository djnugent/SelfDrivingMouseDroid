import multiprocessing
import cv2

class Camera:

    EXIT = -1
    REQUEST = 1

    def __init__(self,index=0,background_capture = True):
        #create a camera object
        self.index = index
        self.camera = None

        # background image processing variables
        self.proc = None                              # background process object
        self.parent_conn = None                       # parent end of communicatoin pipe
        self.background_capture = background_capture  #state variable for background capture

        #open the camera
        self.open()


    #
    # background image processing routines
    #

    # image_capture_background - captures all images from the camera in the background and returning the latest image via the pipe when the parent requests it
    def _image_capture_background(self, imgcap_connection,index):

        # open camera
        camera = cv2.VideoCapture(index)
        if not camera.isOpened():
            print("failed to open camera, exiting!")
            sys.exit(0)


        # exit immediately if imgcap_connection is invalid
        if imgcap_connection is None:
            print("image_capture failed because pipe is uninitialised")
            return

        # clear latest image
        latest_image = None

        while True:
            # constantly get the image from the webcam
            success_flag, image=camera.read()

            # if successful overwrite our latest image
            if success_flag:
                latest_image = image

            # check if the parent wants the image
            if imgcap_connection.poll():
                recv_obj = imgcap_connection.recv()
                # if -1 is received we exit
                if recv_obj == Camera.EXIT:
                    break

                # otherwise we return the latest image
                imgcap_connection.send(latest_image)

        # release camera when exiting
        self.camera.release()

    # close - closes the camera
    def close(self):
        #Clean up when exitting background capture
        if(self.background_capture):
            # send exit command to image capture process
            self.parent_conn.send(Camera.EXIT)
            # join process
            self.proc.join()

    # open - starts the camera(and possibly background capture)
    def open(self):
        #background capture is desired
        if self.background_capture:
            # create pipe
            self.parent_conn, imgcap_conn = multiprocessing.Pipe()

            # create and start the sub process and pass it it's end of the pipe
            self.proc = multiprocessing.Process(target=self._image_capture_background, args=(imgcap_conn,self.index))
            self.proc.daemon = True
            self.proc.start()


    # read - returns latest image from the camera captured from the background process
    def read(self):
        img = None
        success_flag = False

        #grab image from pipe of background capture
        if(self.background_capture):
            # return immediately if pipe is not initialised
            if self.parent_conn == None:
                return success_flag, img

            # send request to image capture for image
            self.parent_conn.send(Camera.REQUEST)

            # wait endlessly until image is returned
            img = self.parent_conn.recv()
            success_flag = img is not None

        #use standard image cap
        else:
            #Grab an image
            success_flag, img= self.camera.read()

        # return image to caller
        return success_flag, img


if __name__ == "__main__":
    import time

    cam = Camera(0,background_capture = True)

    try:
        while True:
            # send request to image capture for image
            ret,img = cam.read()

            # check image is valid
            if ret:
                # display image
                cv2.imshow ('image_display', img)
            else:
                print("no image")

            # check for ESC key being pressed
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break

            # take a rest for a bit
            time.sleep(0.1)
    finally:
        cam.close()
