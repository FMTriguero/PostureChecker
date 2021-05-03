import os

from Config_Reader import config_reader
from model import get_testing_model


class KeypointsFinder:
    def __init__(self):
        self.model_path = os.path.join("Classifier", "KeypointsFinder", "model.h5")
        self.colors = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0], [85, 255, 0],
                       [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255], [0, 170, 255], [0, 85, 255],
                       [0, 0, 255], [85, 0, 255], [170, 0, 255], [255, 0, 255], [255, 0, 170], [255, 0, 85]]
        self.model = get_testing_model
        self.model.load_weights(self.model_path)
        self.params, self.model_params = config_reader()
