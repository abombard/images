from sentence_transformers import SentenceTransformer
from PIL import Image, ImageFile
import requests
import json

import os
import sys
import glob
import argparse

ImageFile.LOAD_TRUNCATED_IMAGES = True

# We use the original clip-ViT-B-32 for encoding images
img_model = SentenceTransformer('clip-ViT-B-32')

# Our text embedding model is aligned to the img_model and maps 50+
# languages to the same vector space
text_model = SentenceTransformer('sentence-transformers/clip-ViT-B-32-multilingual-v1')

# Now we load and encode the images
def load_image(url_or_path):
    if url_or_path.startswith("http://") or url_or_path.startswith("https://"):
        return Image.open(requests.get(url_or_path, stream=True).raw)
    else:
        return Image.open(url_or_path)

def images_to_vectors(img_paths, show_progress_bar=False):
    batch_size = 128

    imgs = [load_image(path) for path in img_paths]

    emb =  img_model.encode(
        imgs,
        batch_size=batch_size,
        convert_to_tensor=True,
        show_progress_bar=show_progress_bar,
    ).tolist()

    for img in imgs:
        img.close()

    return emb

def images_to_documents(imgs, img_emb):
    return [{"link": imgs[i], "vector": img_emb[i]} for i, _ in enumerate(img_emb)]

def texts_to_vectors(texts):
    return text_model.encode(texts).tolist()

def store(img_paths):
    imgs = []
    for path in img_paths:
        if os.path.isdir(path):
            imgs += list(glob.glob(f'{path}/*.jpg'))
        else:
            imgs += [path]

    batch_size = 512

    uid = 0
    while uid < len(imgs):
        img_emb = images_to_vectors(imgs[uid:uid+batch_size], show_progress_bar=True)
        documents = images_to_documents(imgs[uid:uid+batch_size], img_emb)

        for document in documents:
            res = requests.post(f'http://localhost:9200/clip/_doc/{uid}', json=document)
            if args.verbose:
                print(res.json())
            uid += 1

def search_knn(text=None, image_path=None, max_results=10):
    emb = []

    if text:
        emb = texts_to_vectors([text])[0]
    elif image_path:
        emb = images_to_vectors([image_path])[0]

    assert emb

    body = {
        'knn': {
            'field': 'vector',
            'k': max_results,
            'num_candidates': 500,
            'query_vector': emb,
        },
        '_source': ['id', 'link'],
    }

    res = requests.post('http://localhost:9200/clip/_knn_search', json=body)

    resp = res.json()

    items = []
    for hit in resp['hits']['hits']:
        items.append(hit['_source']['link'])

    return items

parser = argparse.ArgumentParser()
parser.add_argument('store', nargs='*', default=[])
parser.add_argument('search', action='store_true')
parser.add_argument('-s', '--sentence')
parser.add_argument('-i', '--image')
parser.add_argument('-v', '--verbose')

if __name__ == '__main__':
    args, paths = parser.parse_known_args()

    if args.search:
        if args.sentence:
            res = search_knn(text=args.sentence)
            print(json.dumps(res))
            sys.exit(0)

        if args.image:
            res = search_knn(image_path=args.image)
            print(json.dumps(res))
            sys.exit(0)

    if args.store:
        store(args.store[1:])
        sys.exit(0)
