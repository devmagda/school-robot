import time
from threading import Thread

import cv2

import Constants
from Logger import CustomLogger
from detections import FaceClassifier, ColorGroupClassifier, CaptureDevice, Rectangle, FaceUtils
from images import ImageUtils
from pi.client import Client

logger = CustomLogger(__name__).get_logger()


class Model:
    def __init__(self, count=Constants.KM_GROUP_COUNT, color=Constants.COLOR_TRASH, capture_device=None):
        self.capture_device = capture_device
        self.face_detector = FaceClassifier()
        self.color_groups_detector = ColorGroupClassifier(count=count, color=color)
        self.current_image = None
        self.result_face = None  # Array of Rectangles
        self.result_color_groups = []
        self.old_face = None
        self.old_color_groups = []
        self.found_face_timestamp = float(-1)
        self.face_age = float(-1)
        self.last_valid_face = None

    def play_sound_threaded(self):
        Thread(target=self._play_sound).start()

    def _play_sound(self):
        from playsound import playsound
        from playsound import PlaysoundException
        time.sleep(4)
        try:
            playsound('blaster.wav')
            try_harder = False
        except PlaysoundException:
            pass

    def calculate(self, image=None):
        if image is not None:
            self.current_image = image
            h, w, _ = self.current_image.shape
            image_center = Rectangle(0, 0, w, h)

            # Face calculation
            self.face_detector.calculate(self.current_image)
            self.result_face = self.face_detector.result
            if self.result_face is not None:
                self.last_valid_face = self.get_face_image()
                self.old_face = self.result_face
                z, y = Rectangle.get_steps(image_center, self.old_face)
                Client.add_rotation(-z, -y)
            else:
                if self.old_face is not None and not self.old_face.is_alive():
                    self.old_face = None

            self.color_groups_detector.calculate(self.current_image)
            self.result_color_groups = self.color_groups_detector.result
            if self.result_color_groups is not None:
                self.old_color_groups = self.result_color_groups
            else:
                if self.old_color_groups is not None:
                    for color_group in self.old_color_groups:
                        if not color_group.is_alive():
                            if self.last_valid_face is not None:
                                Thread(target=FaceUtils.analyze_and_save_to_db, args=(self.last_valid_face,)).start()
                            self.old_color_groups = None
                            Client.shoot()
                            self.play_sound_threaded()
                            break
            return True, self
        return False, None

    def __str__(self):
        return f'Faces: {len(self.result_faces)} ColorGroups: {len(self.result_color_groups)}'

    def get_face_image(self):
        try:
            face = self.old_face
            return ImageUtils.getSubImage(self.current_image, face.x, face.y, face.width, face.height)
        except:
            return None

    def draw_current_view(self):
        image_copy = self.current_image.copy()
        gray_image = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)

        # Convert the grayscale image back to color
        colorized_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)

        colored = colorized_image

        if self.old_face is not None:
            self.old_face.draw(colored)
        if self.old_color_groups is not None:
            self.old_color_groups
            colored = ImageUtils.draw_mask_outline(colored, self.color_groups_detector.old_mask)
            for rectangle in self.old_color_groups:
                rectangle.draw(colored, only_center=True)
        # with_key_points = ImageUtils.draw_key_points_custom(colored, self.color_groups_detector.key_points)

        h, w, _ = image_copy.shape
        image_center = Rectangle(0, 0, w, h, bgr=[0, 0, 0])
        image_center.draw(colored, only_center=True, radius=5, thickness=1)


        return colored


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
            self.model.draw_current_view()

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
