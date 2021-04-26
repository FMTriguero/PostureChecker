import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np


class Classifier:
    def __init__(self):
        path = '/Users/carterash/PostureChecker/.gitignore/keras_model.h5'  #TODO program loads model without path
        self.path = path
        self.model = tensorflow.keras.models.load_model(self.path)
        np.set_printoptions(suppress=True)

    def predict(self, image_path):
        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # 2. Test that the model works with single image.
        image = Image.open(image_path)

        # resize the image to a 224x224 with the same strategy as in TM2:
        # resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        # turn the image into a numpy array
        image_array = np.asarray(image)

        # display the resized image
        image.show()

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = self.model.predict(data)
        return prediction
