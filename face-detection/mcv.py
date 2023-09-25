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


class View:
    def __init__(self):
        pass

    def view(self, model: Model):
        pass


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self):
        while True:
            self.model.calculate()
            self.view.view(self.model)