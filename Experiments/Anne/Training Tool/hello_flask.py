import flask
from flask import request, jsonify
import json
import sys
import threading

from fetchMetadata import fetch
from trainNetwork import *

# Create the application.
APP = flask.Flask(__name__)

metadata = fetch()
print(metadata)

resultNumbers = []

@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    if (len(resultNumbers) > 0):
        return flask.render_template('index0.html', metadata = resultNumbers)
    else:
        return flask.render_template('index.html', metadata = metadata)


@APP.route('/train', methods=['POST'])
def train():
    if request.method == "POST":
        #print("TRAINING")
        content = request.get_json()

        for data in content['trainingDatasets']:
               print(data)
        trainingThread = threading.Thread(target = trainOn, args=(), kwargs={'trainingDatasets':content['trainingDatasets'], 'resultNumbers':resultNumbers})
        trainingThread.start()

        currentlyTraining = True
        return json.dumps({'status':'OK'})

@APP.route('/refetch', methods=['POST'])
def refetch():
        return json.dumps({'latest result':resultNumbers[-1]})


if __name__ == "__main__":
	APP.run(host="0.0.0.0", port="8080")
