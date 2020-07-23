import os, traceback
import hashlib
import argparse
from flask_cors import CORS
from flask import Flask, request, render_template, jsonify, \
        send_from_directory, make_response, send_file

from hparams import hparams
from audio import load_audio
from utils import str2bool, prepare_dirs, makedirs, add_postfix

import requests

from werkzeug.datastructures import ImmutableMultiDict

import threading
import train
import eq

app = Flask(__name__, root_path="", static_url_path='/static_folder', static_folder='static_folder')
CORS(app)

@app.route('/', methods = ['POST', 'GET'])
def index():
    return "flask"

@app.route('/train', methods = ['POST', 'GET'])
def _train():

    print(request.json['userID'])
    userID = request.json['userID']
    t = threading.Thread(target=msw_train, args=(userID, ))
    t.start()

    return request.json['userID'] + ' train start'

@app.route('/set_effect', methods = ['POST', 'GET'])
def _set_effect():

    print(request.form['fileName'])
    print(request.form['fileTime'])

    static_folder = os.getcwd() + "/static_folder/"

    file = request.files['data']
    fileName = static_folder + request.form['fileName']
    file.save(fileName + ".wav")
    print(fileName + ".wav")

    eq.set_effect(1, fileName)
    eq.set_effect(2, fileName)
    eq.set_effect(3, fileName)

    return "effect"

def msw_train(userID):
    parser = argparse.ArgumentParser()
    config = parser.parse_args()

    config.log_dir = 'logs'
    config.data_paths = './datasets/msw'
    config.load_path = None
    config.initialize_path = './logs/pre_m'

    config.num_test_per_speaker = int(2)
    config.random_seed = int(123)
    config.summary_interval = int(100)
    config.test_interval = int(1000)
    config.checkpoint_interval = int(1000)
    config.skip_path_filter = False

    config.slack_url = None
    config.git = False

    train.msw_train(config)

    requests.get("http://127.0.0.1:40000/train_complete?result=" + userID + " train complete")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000, debug=False)