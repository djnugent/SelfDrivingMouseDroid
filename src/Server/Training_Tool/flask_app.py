import flask
from flask import request, jsonify
import json
import sys
import threading

from dataManage import *
from trainNetwork import *

# Create the application.
APP = flask.Flask(__name__)

resultNumbers = []

@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    if (len(resultNumbers) > 0):
        return flask.render_template('index0.html', data = resultNumbers)
    else:
        metadata = fetchMetadata()
        return flask.render_template('index.html', data = metadata)


@APP.route('/keras/callback', methods=['POST'])
def update_metrics():
    if request.method == "POST":
        print("KERAS CALLBACK")
        content = request.get_json()
        print(content["data"])

@APP.route('/train', methods=['POST'])
def train():
    if request.method == "POST":
        #print("TRAINING")
        content = request.get_json()
        print(content)
        trainingThread = threading.Thread(target = trainOn, args=(), kwargs={'modelData':content['modelData']})
        trainingThread.start()
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
