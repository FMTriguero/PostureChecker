# TODO:
# 4. Make custom start and stop for program.
# 5. Build trigger to take 100 photos over a period of 10 mins calculat % good posture
# !!!Modifying 5. to "Build trigger that sends alert (shutdown for now) when x bad posture has been recorded
# 6. Add a config file to have modify things like "bad posture before alert", camera index...

from Classifier.Classifier import Classifier
from Camera.Camera import Camera
import os
import time


class PostureChecker:
    def __init__(self, classifier=None, camera=None):
        self.classifier = classifier
        self.camera = camera

        self.prediction = None
        self.running_counter_bad = 0

    def loop(self):
        running = True
        while running:
            time.sleep(1)
            self.take_image()
            self.analyze_image()
            print("Work in progress, need analyze_results")

    def take_image(self):
        image = self.camera.take_screenshot()
        self.camera.save_screenshot(image=image)

    def analyze_image(self):
        self.prediction = self.classifier.predict(image_path=os.path.join("working_image.jpg"))
        self.analyze_results()

    def analyze_results(self):
        print("Work in progress, need second model")

    def testing(self):
        self.test_image()
        self.classifier.keypoints_finder.test_show_image(black_image=True)

    def test_image(self):
        self.classifier.predict(image_path=os.path.join("Testing", "good_posture_me2.jpg"))

    def cleanup(self):
        """Check for when app is not closed properly"""
        self.camera.delete_working_screenshot()


def main():
    classifier = Classifier()
    camera = Camera()
    postureChecker = PostureChecker(classifier=classifier, camera=camera)

    postureChecker.cleanup()
    postureChecker.testing()
    # postureChecker.loop()


if __name__ == "__main__":
    main()
