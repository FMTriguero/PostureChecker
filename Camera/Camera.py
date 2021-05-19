from cv2 import *


class Camera:
    def __init__(self):
        # Might need to change based on index of camera, 0 for the default camera -- VideoCapture(0)
        self.cam = VideoCapture('http://10.108.112.132:4747/mjpegfeed?640x480')
        self.working_path = "working_image.jpg"

    def take_screenshot(self):
        ret, Image = self.cam.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
        return Image

    def save_screenshot(self, image, path=""):
        if len(path) != 0:
            cv2.imwrite(path, image)
        else:
            cv2.imwrite(self.working_path, image)
        print(path)

    def delete_working_screenshot(self):
        if os.path.exists(os.path.join(self.working_path)):
            os.remove(os.path.join(self.working_path))


