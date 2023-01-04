from sentence_transformers import SentenceTransformer
from PIL import Image
import requests
import json

import sys
import argparse

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sentence')
    parser.add_argument('-v', dest='verbose', action='store_true')

    args, img_paths = parser.parse_known_args()

    if args.sentence:
        text_embeddings = text_model.encode([args.sentence])
        print(json.dumps(text_embeddings.tolist()[0]))
        sys.exit(0)

    images = [load_image(img) for img in img_paths]

    batch_n = 0
    batch_size = 10
    batch = []

    out = []

    i = 0
    while i < len(img_paths):
        batch = img_paths[i:batch_size]
        
        # Map images to the vector space
        img_embeddings = img_model.encode(batch)
        for i, vec in enumerate(img_embeddings.tolist()):
            out.append({
                "link": img_paths[i],
                "vector": vec,
            })

        fpath = "./tmp/%d.json" % batch_n
        with open(fpath, 'w+') as ffs:
            ffs.write(json.dumps(out))
        out = []
        batch_n += 1
