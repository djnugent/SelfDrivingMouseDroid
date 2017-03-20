from flask import Flask, render_template_string, Response
import cv2
import numpy as np
import logging
from threading import Thread, Event

#disable logging
log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)
log.disabled = True

# HTML file for the page
html = '''<html>
          <head>
            <title>Video Debugger</title>
          </head>
          <body>
            <h1>Video Debugger</h1>
            <img id="bg" src="{{ url_for('video_feed') }}">
          </body>
        </html>'''

# Start image
blank = np.zeros((240,360,3))
cv2.putText(blank,'Waiting for images...',(10,200), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
START_IMAGE = cv2.imencode('.jpg', blank)[1].tobytes()
# Error image
blank = np.zeros((240,360,3))
cv2.putText(blank,'Error: Empty or Corrupt image',(10,200), cv2.FONT_HERSHEY_SIMPLEX, 0.65,(255,255,255),2)
ERROR_IMAGE = cv2.imencode('.jpg', blank)[1].tobytes()

# rendered image
live_image = START_IMAGE

def flask_thread():
    app.run(host='0.0.0.0', port=80)

# Call this method to queue a new image for the webserver
def imshow(image, title="Hello World"):
    global live_image
    try:
        ret, jpeg = cv2.imencode('.jpg', image)
        if ret:
            live_image = jpeg.tobytes()
        else:
            live_image = ERROR_IMAGE
    except:
        live_image = ERROR_IMAGE


# Feeds the video feed with images
def __gen():
    global live_image
    while True:
        # wait for new image before updating page
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + live_image + b'\r\n\r\n')

# Webpage stuff
app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(html)

@app.route('/video_feed')
def video_feed():
    return Response(__gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Start server
print "VideoDebugger server running on http://0.0.0.0:80/"
t = Thread(target=flask_thread, args=())
t.daemon =True
t.start()
