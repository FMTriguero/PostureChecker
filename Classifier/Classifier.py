import tensorflow.keras
import os
from PIL import Image, ImageOps
import numpy as np


class Classifier:
    def __init__(self):
        path = os.path.join("Classifier", "keras_model.h5")
        self.path = path
        self.model = tensorflow.keras.models.load_model(self.path)
        np.set_printoptions(suppress=True)

        self.image = None

    def predict(self, image_path=None, image=None):
        if image_path is not None:
            self.image = Image.open(image_path)
        else:
            self.image = image

        data = self.prepare_image()

        prediction = self.model.predict(data)
        return prediction

    def prepare_image(self):
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        size = (224, 224)
        self.image = ImageOps.fit(self.image, size, Image.ANTIALIAS)
        image_array = np.asarray(self.image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        return data
