# TODO:
# 4. Make custom start and stop for program.
# !!!Modifying 5. to "Build trigger that sends alert (shutdown for now) when x bad posture has been recorded
# 6. Add a config file to have modify things like "bad posture before alert", camera index...

from UI.UI import UI_run_app
from Classifier.Classifier import Classifier
from Camera.Camera import Camera
from Alarm.Alarm import Alarm
import time


class PostureChecker:
    def __init__(self, classifier=None, camera=None, alarm=None):
        self.classifier = classifier
        self.camera = camera
        self.alarm = alarm

    def loop(self):
        running = True
        while running:
            time.sleep(5)
            image = self.camera.take_screenshot()
            result, prediction = self.classifier.predict(image=image)
            print(result)
            if result == "Bad":
                self.alarm.ring()

    def cleanup(self):
        """Check for when app is not closed properly"""
        self.camera.delete_working_screenshot()


def main():
    UI_run_app()

    classifier = Classifier()
    camera = Camera()
    alarm = Alarm()
    postureChecker = PostureChecker(classifier=classifier, camera=camera, alarm=alarm)

    postureChecker.cleanup()
    postureChecker.loop()


if __name__ == "__main__":
    main()
