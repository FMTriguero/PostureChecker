import cv2

from Classifier.KeypointsFinder.Keypoints_Finder import KeypointsFinder
from Classifier.PostureClassifier.Posture_Classifier import PostureClassifier


def analyze_prediction(prediction):
    if prediction[0][0] < prediction[0][1]:
        prediction = "Good"
    else:
        prediction = "Bad"
    return prediction


class Classifier:
    def __init__(self):
        self.keypoints_finder = KeypointsFinder()
        self.posture_classifier = PostureClassifier()

        self.image = None

    def predict(self, image_path=None, image=None):
        if image_path is not None:              # To work with image path or image object (must be cv2 image)
            self.image = cv2.imread(image_path)
        else:
            self.image = image

        self.keypoints_finder.find_keypoints(self.image)
        canvas = self.keypoints_finder.draw_peaks_over_canvas(black_image=True)
        prediction = self.posture_classifier.predict(image=canvas)
        results = analyze_prediction(prediction)
        return results, prediction
