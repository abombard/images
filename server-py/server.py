import os
import json
import requests

from flask import Flask, request, redirect, flash
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from sentence_transformers import SentenceTransformer

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './tmp/upload'

cors = CORS(app)

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

@cross_origin()
@app.route('/image', methods=['POST'])
def image():
    if 'file' not in request.files:
        flash('no file in request')
        return redirect(request.url)

    path = upload_file(request.files['file'])

    return f'stored {path}!'

# search

text_model = SentenceTransformer('sentence-transformers/clip-ViT-B-32-multilingual-v1')

@cross_origin()
@app.route('/search', methods=['POST'])
def search():
    params = json.loads(request.data)

    sentence = params.get('text') or ''
    if sentence == '':
        return 'empty request'

    text_embeddings = text_model.encode(sentence)

    res = requests.post('http://localhost:9000/clip/_search', {
        'knn': {
            'field': 'vector',
            'k': 10,
            'num_candidates': 100,
            'query_vector': text_embeddings,
        },
        '_source': ['id', 'link'],
    })

    return str(res)
