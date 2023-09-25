import threading
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


        # Create thread objects for both functions
        faces_thread = threading.Thread(target=self.face_detector.calculate, args=(self.current_image,))
        colors_thread = threading.Thread(target=self.color_groups_detector.calculate, args=(self.current_image,))

        # Start both threads
        faces_thread.start()
        colors_thread.start()

        # Wait for both threads to finish
        faces_thread.join()
        colors_thread.join()

        self.result_faces = self.face_detector.result
        self.result_color_groups = self.color_groups_detector.result
        # print('Done')

    def __str__(self):
        return f'Faces: {len(self.result_faces)} ColorGroups: {len(self.result_color_groups)}'


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
        print(f'{fps} Fps | {diff_mil} ms -> ', end='')
