import threading
import time

import cv2

import Constants
from detections import FaceClassifier, ColorGroupClassifier, CaptureDevice, Rectangle
from images import ImageUtils


class Model:
    def __init__(self, count=Constants.KM_GROUP_COUNT, color=Constants.COLOR_TRASH, capture_device=None):
        self.capture_device = capture_device
        self.face_detector = FaceClassifier()
        self.color_groups_detector = ColorGroupClassifier(count=count, color=color)
        self.current_image = None
        self.result_faces = []
        self.result_color_groups = []
        self.old_faces = None
        self.old_color_groups = None

    def calculate(self, image=None):
        if image is not None:
            self.current_image = image
            found = True
        else:
            found, self.current_image = self.capture_device.get_image()
        if found:
            self.face_detector.calculate(self.current_image)
            self.color_groups_detector.calculate(self.current_image)

            self.result_faces = self.face_detector.result
            self.result_color_groups = self.color_groups_detector.result
        return found, self


    def calculate_threaded(self):
        found, self.current_image = self.capture_device.get_image()

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
        return self

    def __str__(self):
        return f'Faces: {len(self.result_faces)} ColorGroups: {len(self.result_color_groups)}'

    def get_face_images(self):
        faces = []
        for face in self.result_faces:
            faces.append(ImageUtils.getSubImage(self.current_image, face.x, face.y, face.width, face.height))
        return faces

    def get_color_key_points_image(self):
        image_copy = self.current_image.copy()
        gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
        colored = cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB)
        gray_with_key_points = ImageUtils.draw_key_points(colored, self.color_groups_detector.key_points)
        return gray_with_key_points


class View:
    def __init__(self):
        pass

    def view(self, model: Model):
        for face in model.result_faces:
            face.draw(model.current_image)

        for color_group in model.result_color_groups:
            color_group.draw(model.current_image)

        model.capture_device.center.draw(model.current_image)

        flipped = ImageUtils.mirror(model.current_image, 1)

        cv2.imshow('debug', flipped)


class Controller:
    timestamp_last = 0

    def __init__(self):
        self.model = Model(capture_device=CaptureDevice())
        self.view = View()

    def run(self):
        active = True
        while active:
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                active = False
            self.model.calculate_threaded()
            self.view.view(self.model)
            self.print_fps()
            self.show_distances()
            self.model.get_face_images()
            self.model.get_color_key_points_image()

    def show_distances(self):
        for face in self.model.result_faces:
            print('Distance: ', Rectangle.distance(face, self.model.capture_device.center))
            pass

    def print_fps(self):
        diff_sec = (time.time_ns() - Controller.timestamp_last) / 1000000000
        diff_mil = int(diff_sec * 1000)
        Controller.timestamp_last = time.time_ns()
        fps = int(1 / diff_sec)
        print(f'{fps} Fps | {diff_mil} ms -> ', end='')
