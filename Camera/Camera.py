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

    def save_screenshot(self, image=None, image_path=None, path=None):
        if image is None and image_path is None:
            AssertionError("Need either an image input or an image path")
        if path is None:
            path = self.working_path
        if image is None:
            image = cv2.imread(image_path)

        cv2.imwrite(path, image)
        print(path)

    def delete_working_screenshot(self):
        if os.path.exists(os.path.join(self.working_path)):
            os.remove(os.path.join(self.working_path))


