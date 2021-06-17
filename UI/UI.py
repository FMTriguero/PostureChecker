import sys
import time
import cv2
import numpy as np
from functools import partial
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.capturing_next_frame = False
        self.captured_frame = None

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
            if self.capturing_next_frame:
                self.captured_frame = ret
                self.capturing_next_frame = False

        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

    def capture_next_frame(self):
        self.capturing_next_frame = True


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.working_images_good = []
        self.working_images_bad = []

        self.setWindowTitle("Recording Posture Images")
        self.display_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.display_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')

        # create button to take good posture screenshot
        self.button_good = QPushButton("Good Posture", self)
        self.button_good.clicked.connect(partial(self.take_screenshot, "Good"))
        # create button to take bad posture screenshot
        self.button_bad = QPushButton("Bad Posture", self)
        self.button_bad.clicked.connect(partial(self.take_screenshot, "Bad"))

        # create button to load the learner
        self.button_trainer = QPushButton("Train model", self)
        self.button_trainer.clicked.connect(self.start_trainer)

        # create a horizontal box layout and add the two buttons
        hbox = QHBoxLayout()
        hbox.addWidget(self.button_good)
        hbox.addWidget(self.button_bad)

        # create a vertical box layout and add the hbox and the two labels
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        vbox.addWidget(self.button_trainer)

        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    def take_screenshot(self, type_button):
        print("Taking screenshot for trainer")
        self.thread.capture_next_frame()
        while self.thread.captured_frame is None:
            time.sleep(0.1)
        if type_button == "Good":
            self.working_images_good.append(self.thread.captured_frame)
        else:
            self.working_images_bad.append(self.thread.captured_frame)
        self.thread.captured_frame = None


    def start_trainer(self):
        print("To-do")

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


def UI_run_app():
    app = QApplication(sys.argv)
    win = App()
    win.show()
    app.exec_()
