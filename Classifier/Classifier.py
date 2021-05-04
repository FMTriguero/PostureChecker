import cv2

from Classifier.KeypointsFinder.Keypoints_Finder import KeypointsFinder


class Classifier:
    def __init__(self):
        self.keypoints_finder = KeypointsFinder()

        self.image = None

    def predict(self, image_path=None, image=None):
        if image_path is not None:              # To work with image path or image object (must be cv2 image)
            self.image = cv2.imread(image_path)
        else:
            self.image = image

        self.keypoints_finder.find_keypoints(self.image)
