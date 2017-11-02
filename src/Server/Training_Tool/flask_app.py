import flask
from flask import request, jsonify
import json
import sys
import threading

from dataManage import *
from trainNetwork import *

# Create the application.
APP = flask.Flask(__name__)

@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    metadata = fetchMetadata()
    return flask.render_template('index.html', data = metadata)


@APP.route('/train', methods=['POST'])
def train():
    if request.method == "POST":
        #print("TRAINING")
        content = request.get_json()
        trainingThread = threading.Thread(target = trainOn, args=(), kwargs={'modelData':content['modelData']})
        trainingThread.start()
        resultNumbers = []
        return json.dumps({"status":"ok"})

@APP.route('/delete', methods=['POST'])
def delete():
   if request.method == "POST":
      content = request.get_json()
      print(content["dataset"])
      deleteDataset(content['dataset'])
      return json.dumps({"status":"ok"})

if __name__ == "__main__":
	APP.run(host="0.0.0.0", port="8080")
