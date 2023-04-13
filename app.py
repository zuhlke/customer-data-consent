from flask import Flask, request, jsonify, render_template
from jsonschema import validate
import json
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, jsonify,request
from threading import Thread, Event, Lock
from time import sleep
import sys
import pandas as pd

import consent_data_mods.data_quality as dq







app = Flask(__name__)
#turn the flask app into a socketio app
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None
thread_lock = Lock()
import os
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)







@app.route('/')
def index():
    return render_template('index.html')


# Define the route for uploading a JSON file
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the request contains a file
    if 'file' not in request.files:
        return jsonify({'message': 'No file uploaded'}), 400

    # Read the uploaded file and parse it as JSON
    file = request.files['file']
    json_data = json.load(file)

    return dq.consent_quality_checks(json_data)



if __name__ == '__main__':
    app.run(debug=True)