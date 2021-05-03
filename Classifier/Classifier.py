import tensorflow.keras
import os
from PIL import Image, ImageOps
import numpy as np

from KeypointsFinder.Keypoints_Finder import KeypointsFinder


class Classifier:
    def __init__(self):
        self.keypoints_finder = KeypointsFinder()

        self.image = None

    def predict(self, image_path=None, image=None):  # To work with image path or image object (careful type)
        if image_path is not None:
            self.image = Image.open(image_path)
        else:
            self.image = image

        return "TODO"
