from Classifier.Classifier import Classifier
from Camera.Camera import Camera
import time
import os


def get_all_directories(base_path="Saving_screenshots"):
    directories = [f for f in os.listdir(base_path) if
                   os.path.isdir(os.path.join(base_path, f))]
    return directories


def get_all_files_in_directory(directories, base_path="Saving_screenshots"):
    files = []
    for directory in directories:
        files.append([f for f in os.listdir(os.path.join(base_path, directory)) if
                      os.path.isfile(os.path.join(base_path, directory, f))])
    return files


class Tools:

    def __init__(self, classifier=None, camera=None):
        self.classifier = classifier
        self.camera = camera
        self.base_path = "Saving_screenshots"

    def take_screenshots_for_posture_data(self, posture, number_pictures, wait_time):
        print("Please keep a " + posture + " while this tests runs")
        print("Initiating\n")
        time.sleep(5)
        folder_path = os.path.join(self.base_path, posture)
        os.mkdir(folder_path)
        for i in range(number_pictures):
            time.sleep(wait_time)
            image = self.camera.take_screenshot()
            self.camera.save_screenshot(image,
                                        path=(os.path.join(folder_path, posture + "_" + str(i) + ".jpg")))
            print("Taken " + str(i + 1) + " images")

    def transform_screenshots_to_key_point_data(self):
        directories = get_all_directories()
        files = get_all_files_in_directory(directories)
        self.key_point_extraction_data(directories, files)

    def key_point_extraction_data(self, directories, files):
        i = 0
        for directory in directories:
            new_directory = directory + "_key_points"
            os.mkdir(os.path.join(self.base_path, new_directory))
            for file in files[i]:
                print(os.path.join(self.base_path, directory, file))
                self.classifier.predict(os.path.join(self.base_path, directory, file))
                canvas = self.classifier.keypoints_finder.draw_peaks_over_canvas(black_image=True)
                self.camera.save_screenshot(image=canvas, path=os.path.join(self.base_path, new_directory, file))
            i = i + 1


def running_tools():
    classifier = Classifier()
    camera = Camera()

    tools = Tools(classifier=classifier, camera=camera)

    # tools.take_screenshots_for_posture_data("testing", 10, 3)
    # tools.transform_screenshots_to_key_point_data()


running_tools()
