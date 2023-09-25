import time

import cv2

import Constants
from detections import FaceClassifier, ColorGroupClassifier, CaptureDevice


class Model:
    def __init__(self, count=Constants.KM_GROUP_COUNT, color=Constants.COLOR_TRASH):
        self.capture_device = CaptureDevice()
        self.face_detector = FaceClassifier()
        self.color_groups_detector = ColorGroupClassifier(count=count, color=color)
        self.current_image = None
        self.result_faces = []
        self.result_color_groups = []

    def calculate(self):
        self.current_image = self.capture_device.get_image()
        self.result_faces = self.face_detector.classify(self.current_image)
        self.result_color_groups = self.color_groups_detector.classify(self.current_image)
        print('Done')

    def __str__(self):
        return f'{self.result_faces}\n{self.result_color_groups}'


class View:
    def __init__(self):
        pass

    def view(self, model: Model):
        pass


class Controller:
    timestamp_last = 0
    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self):
        active = True
        while active:
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                active = False
            self.model.calculate()
            self.view.view(self.model)
            self.printFps()
            print(self.model)


    def printFps(self):
        diff_sec = (time.time_ns() - Controller.timestamp_last) / 1000000000
        diff_mil = int(diff_sec * 1000)
        Controller.timestamp_last = time.time_ns()
        fps = int(1 / diff_sec)
        print(f'{fps} Fps | {diff_mil} ms -> ')
