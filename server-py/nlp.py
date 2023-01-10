from PIL import Image, ImageFile
import requests

import os
import sys
import glob
import argparse

from es import create_index, delete_index, search_knn

ImageFile.LOAD_TRUNCATED_IMAGES = True

from models.clip import CLIP
from models.groupvit import GROUPVIT

models = {
    CLIP.name: CLIP(),
    GROUPVIT.name: GROUPVIT(),
}

# Now we load and encode the images
def load_image(url_or_path):
    if url_or_path.startswith("http://") or url_or_path.startswith("https://"):
        return Image.open(requests.get(url_or_path, stream=True).raw)
    else:
        return Image.open(url_or_path)

def images_to_vectors(model, img_paths):
    imgs = [load_image(path) for path in img_paths]

    emb = model.images_encode(imgs)

    for img in imgs:
        img.close()

    return emb

def images_to_documents(imgs, img_emb):
    return [{"link": imgs[i], "vector": img_emb[i]} for i, _ in enumerate(img_emb)]

def texts_to_vectors(model, texts):
    print('coucou', texts)
    return model.texts_encode(texts)

def store(model, img_paths):
    imgs = []
    for path in img_paths:
        if os.path.isdir(path):
            imgs += list(glob.glob(f'{path}/*.jpg'))
        else:
            imgs += [path]

    batch_size = 64

    uid = 0
    while uid < len(imgs):
        img_emb = images_to_vectors(model, imgs[uid:uid+batch_size])
        print(f"indexed {uid} photos ...")
        documents = images_to_documents(imgs[uid:uid+batch_size], img_emb)

        for document in documents:
            res = requests.post(f'http://localhost:9200/{model.name}/_doc/{uid}', json=document)
            print(res.json())
            uid += 1

def knn_search(model, text=None, image_path=None, max_results=10):
    m = models[model]

    emb = []

    if text:
        emb = texts_to_vectors(m, [text])[0]
    elif image_path:
        emb = images_to_vectors(m, [image_path])[0]

    assert emb

    return search_knn(model, emb, max_results)


class Bin(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='fun with nlp',
            usage='''
            python nlp.py <model> <comand> [<args>]

            model:
            - clip
            - groupvit

            command:
            - create
            - delete
            - store
            - search
            '''
        )

        parser.add_argument('model')
        parser.add_argument('command')

        args = parser.parse_args(sys.argv[1:3])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        self.model = models[args.model]

        getattr(self, args.command)()

    def store(self):
        return store(self.model, sys.argv[3:])

    def search(self):
        parser = argparse.ArgumentParser(
            description='knn search',
            usage='''
            --sentence    the text to search
            --image       the image path to search
            '''
        )

        parser.add_argument('-s', '--sentence')
        parser.add_argument('-i', '--image')

        args = parser.parse_args(sys.argv[3:])

        res = search(self.model.name, text=args.sentence, image_path=args.image)
        print(res)

    def create(self):
        create_index(self.model.name, self.model.dims)

    def delete(self):
        delete_index(self.model.name)

if __name__ == '__main__':
    Bin()
