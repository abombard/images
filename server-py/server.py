import os
import json

from flask import Flask, request, redirect, flash
from flask_cors import CORS
from werkzeug.utils import secure_filename

from nlp import knn_search

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './tmp/upload'

cors = CORS(app)

model = 'groupvit'

# ping

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'

# store

def upload_file(file):
    filename = file.filename or ''
    if filename == '':
        flash('empty file name in request')
        return redirect(request.url)

    filename = secure_filename(filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    file.save(path)

    return path

@app.route('/image', methods=['POST'])
def image():
    if 'file' not in request.files:
        flash('no file in request')
        return redirect(request.url)

    path = upload_file(request.files['file'])

    return f'stored {path}!'

# search

@app.route('/search', methods=['POST'])
def search():
    params = json.loads(request.data)

    sentence = params.get('text')
    image_path = params.get('image')

    path = f'../vue/upload/{image_path}'

    return knn_search(model, text=sentence, image_path=path, max_results=30)
