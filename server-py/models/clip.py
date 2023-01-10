from sentence_transformers import SentenceTransformer

class CLIP:
    name = "clip"
    dims = 512

    def __init__(self):
        # We use the original clip-ViT-B-32 for encoding images
        self.img_model = SentenceTransformer('clip-ViT-B-32')

        # Our text embedding model is aligned to the img_model and maps 50+
        # languages to the same vector space
        self.text_model = SentenceTransformer('sentence-transformers/clip-ViT-B-32-multilingual-v1')

    def images_encode(self, imgs):
        emb = self.img_model.encode(imgs)
        return emb.tolist()

    def texts_encode(self, texts):
        emb = self.text_model.encode(texts)
        return emb.tolist()
