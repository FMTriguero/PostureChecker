from cv2 import *


class Camera:
    def __init__(self):
        self.cam = VideoCapture(1)      # Might need to change based on index of camera, 0 for the default camera
        self.working_path = "working_image.jpg"
        self.screenshot = None

    def take_screenshot(self):
        ret, self.screenshot = self.cam.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")

    def save_working_screenshot(self):
        cv2.imwrite(self.working_path, self.screenshot)

    def delete_working_screenshot(self):
        os.remove(os.path.join(self.working_path))


