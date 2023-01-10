from transformers import AutoProcessor, CLIPTokenizer, GroupViTModel

class GROUPVIT:
    name = "groupvit"
    dims = 256

    def __init__(self):
        self.model = GroupViTModel.from_pretrained("nvidia/groupvit-gcc-yfcc")
        self.tokenizer = CLIPTokenizer.from_pretrained("nvidia/groupvit-gcc-yfcc")
        self.processor = AutoProcessor.from_pretrained("nvidia/groupvit-gcc-yfcc")

    def images_encode(self, imgs):
        inputs = self.processor(images=imgs, return_tensors="pt")
        emb = self.model.get_image_features(**inputs)
        return emb.tolist()

    def texts_encode(self, texts):
        inputs = self.tokenizer(texts, padding=True, return_tensors="pt")
        emb = self.model.get_text_features(**inputs)
        return emb.tolist()
