## Video Debugger

### Description
Stream OpenCV images to browser to debug  your video pipeline on a server with no display

### Install
1. In this directory run `python3 setup.py install --user`

### Usage
1. In this directory run "python3 test.py".
2. If running locally navigate the browser to the `127.0.0.1:8080`
3. Otherwise if in a docker us the `-p 8080:8080` flag to map port 8080 into the machine
and navigate your browser to IP of the docker container. This is printed at the top of the docker terminal upon start up.


**Note:** Once you install videodebugger it can be imported into any script in any directory.
