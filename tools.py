from Classifier.Classifier import Classifier
from Camera.Camera import Camera
import time
import os


class Tools:

    def __init__(self, classifier=None, camera=None):
        self.classifier = classifier
        self.camera = camera

    def take_screenshots_for_posture_data(self, posture, number_pictures, wait_time):
        print("Please keep a " + posture + " while this tests runs")
        print("Initiating\n")
        time.sleep(5)
        folder_path = os.path.join("Saving_screenshots", posture)
        os.mkdir(folder_path)
        for i in range(number_pictures):
            time.sleep(wait_time)
            image = self.camera.take_screenshot()
            self.camera.save_screenshot(image,
                                        path=(os.path.join(folder_path, posture + "_" + str(i) + ".jpg")))
            print("Taken " + str(i) + " images")

    def key_point_extraction_data(self):
        self.predict_image_data()
        self.classifier.keypoints_finder.test_show_image()

    def predict_image_data(self):
        self.classifier.predict(image_path=os.path.join("Saving_screenshots", "Good_Posture_Playtime", "Good_Posture_Playtime_0.jpg"))


def running_tools():
    classifier = Classifier()
    camera = Camera()

    # tools = Tools(camera=camera)
    tools = Tools(classifier=classifier, camera=camera)

    # tools.take_screenshots_for_posture_data("Bad_Posture_SquishNeck", 10, 3)
    tools.key_point_extraction_data()


running_tools()
