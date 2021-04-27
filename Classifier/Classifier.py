import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np


class Classifier:
    def __init__(self):
        path = "D:\FMTriguero\PostureChecker\Classifier\keras_model.h5"  # TODO program loads model without path
        self.path = path
        self.model = tensorflow.keras.models.load_model(self.path)
        np.set_printoptions(suppress=True)

        self.image = None

    def predict(self, image_path):
        self.image = Image.open(image_path)
        data = self.prepare_image()

        # run the inference
        prediction = self.model.predict(data)
        return prediction

    def prepare_image(self):
        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # resize the image to a 224x224 with the same strategy as in TM2:
        # resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        self.image = ImageOps.fit(self.image, size, Image.ANTIALIAS)

        # turn the image into a numpy array
        image_array = np.asarray(self.image)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        return data
