# TODO:
# 3. Test that the model works with live stream images.
# 4. Make custom start and stop for program.
# 5. Build trigger to take 100 photos over a period of 10 mins calculat % good posture

from Classifier.Classifier import Classifier
from Camera.Camera import *
import os
import time


class PostureChecker:
    def __init__(self, classifier=None, camera=None):
        self.classifier = classifier
        self.camera = camera

        self.prediction = None

    def loop(self):
        running = True
        while running:
            time.sleep(1)
            self.analyze_screenshot()

    def analyze_screenshot(self):
        self.camera.take_screenshot()
        self.camera.save_working_screenshot()
        self.prediction = self.classifier.predict(image_path=os.path.join("working_image.jpg"))
        self.analyze_results()
        self.camera.delete_working_screenshot()

    def analyze_results(self):
        if self.prediction[0][0] > self.prediction[0][1]:
            return print("Thumbs up!")
        return print("Thumbs down!")

    def testing(self):
        self.test_image()
        self.analyze_results()

    def test_image(self):
        path_to_picture = os.path.join("Testing", "Thumb down.jpg")
        self.prediction = self.classifier.predict(image_path=path_to_picture)


def main():
    classifier = Classifier()
    camera = Camera()
    postureChecker = PostureChecker(classifier=classifier, camera=camera)
    # postureChecker.testing()
    postureChecker.loop()


if __name__ == "__main__":
    main()
