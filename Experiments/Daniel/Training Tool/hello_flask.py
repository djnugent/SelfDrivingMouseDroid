import flask
from flask import request, jsonify
import json
import sys
import threading

from fetchMetadata import fetch
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
        metadata = fetch()
        return flask.render_template('index.html', data = metadata)


@APP.route('/train', methods=['POST'])
def train():
    if request.method == "POST":
        content = request.get_json()
        trainingThread = threading.Thread(target = trainOn, args=(), kwargs={'trainingDatasets':content['trainingDatasets'], 'resultNumbers':resultNumbers})
        trainingThread.start()
        return json.dumps({"status":"ok"})

if __name__ == "__main__":
	APP.run(host="0.0.0.0", port="8080")
