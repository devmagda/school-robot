import cv2
import numpy
import numpy as np

import Constants
from images import ImageUtils, Colors


class CaptureDevice:
    def get_image(self):
        return self.cap.read()

    def __init__(self, width=Constants.SCREEN_WIDTH, height=Constants.SCREEN_HEIGHT):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        _, self.image = self.cap.read()
        self.width, self.height, _ = self.image.shape
        self.center = Rectangle(width / 2, height / 2, 0, 0)


class Classifier:
    def __init__(self):
        self.result = []

    def classify(self, image):
        pass


class ClassifierResult:
    def __init__(self):
        pass


class Rectangle:
    def __init__(self, x, y, width, height, bgr=[255, 255, 255]):
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.center = (self.x + (self.width / 2), self.y + (self.height / 2))
        self.color = bgr

    def __str__(self):
        return f'Rectangle(x={self.x}, y={self.y}, width={self.width}, height={self.height})'

    def scale(self, scale=1.0):
        self.x = int(self.x * scale)
        self.y = int(self.y * scale)
        self.width = int(self.width * scale)
        self.height = int(self.height * scale)
        self.center = (self.x + (self.width / 2), self.y + (self.height / 2))
        return self

    def draw(self, image):
        cv2.rectangle(image, (self.x, self.y), (self.x + self.width, self.y + self.height),
                      color=self.color, thickness=2)
        # center_x, center_y = self.center
        # cv2.circle(image, (int(center_x), int(center_y)), 2, color=self.color, thickness=4)

    # Rectangle.distance(s_temp, s)
    @staticmethod
    def distance(rectangle_1, rectangle_2):
        a = numpy.array(rectangle_1.center)
        b = numpy.array(rectangle_2.center)
        return numpy.linalg.norm(a - b)


class CascadeClassifier(Classifier):
    def __init__(self, path_to_cascade: str):
        self.cascade = cv2.CascadeClassifier(path_to_cascade)

    def classify(self, gray):
        try:
            return self.cascade.detectMultiScale(gray, 1.1, 4)
        except:
            return []


class EyeClassifier(CascadeClassifier):
    def __init__(self):
        super().__init__('haarcascade_eye.xml')

    def classify(self, gray, scale=1.0):
        gray_scaled = ImageUtils.scaleImage(gray, scale)
        return super().classify(gray_scaled)


class FaceClassifier(CascadeClassifier):
    def __init__(self):
        super().__init__('haarcascade_frontalface_default.xml')
        self.eye_classifier = EyeClassifier()

    def classify(self, image, scale=0.5):
        inverted_scale = 1 / scale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_scaled = ImageUtils.scaleImage(gray, scale)
        result = []
        result_faces = super().classify(gray_scaled)
        for face in result_faces:
            x, y, w, h = face
            cut_face = ImageUtils.getSubImage(gray_scaled, x, y, w, h)
            # ImageUtils.IO.saveJpg('face', cut_face)
            result_eyes = self.eye_classifier.classify(cut_face)
            if len(result_eyes) >= Constants.EYES_MINIMUM:
                result.append(Rectangle(x, y, w, h, bgr=[255, 0, 0]).scale(inverted_scale))
        return result

    def calculate(self, gray):
        try:
            self.result = self.classify(gray)[0]
        except:
            self.result = None


class ColorGroupClassifier(Classifier):
    def __init__(self, count=Constants.KM_GROUP_COUNT, color=Constants.COLOR_TRASH):
        self.lower, self.upper = Colors.get_color_limits(color)
        self.color = color
        self.count = count
        self.sift = cv2.SIFT_create()
        self.key_points = []

    def classify(self, image, scale=1 / 5):
        inverted_scale = 1 / scale
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower, self.upper)
        scaled_mask = ImageUtils.scaleImage(mask, scale)
        scaled_mask = cv2.fastNlMeansDenoising(scaled_mask, None, h=20, templateWindowSize=3, searchWindowSize=5)
        scaled_key_points = []
        for key_point in self.sift.detect(scaled_mask, None):
            x, y = key_point.pt
            x = x * inverted_scale
            y = y * inverted_scale
            key_point.pt = (x, y)
            scaled_key_points.append(key_point)
        self.key_points = scaled_key_points

        # Creating numpy array for kmeans calculation
        key_points_as_np_array = np.empty((len(self.key_points), 2), np.float32)  # creates empty 2d numpy array
        for i, key_point in enumerate(self.key_points):
            x = np.float32(key_point.pt[0])
            y = np.float32(key_point.pt[1])
            key_points_as_np_array[i] = (x, y)

        result = []
        centers = ColorGroupClassifier.Helper.kmeans(key_points_as_np_array, self.count)
        for center in centers:
            if len(center) == 2:
                x, y = center
                result.append(Rectangle(x, y, 0, 0, bgr=self.color[2]).scale(inverted_scale))

        return result

    def calculate(self, image):
        self.result = self.classify(image)

    class Helper:
        @staticmethod
        def kmeans(key_points_as_np_array, kmeans_count: int):
            if key_points_as_np_array is None:
                return []

            key_point_count = len(key_points_as_np_array)

            if key_point_count == 0:
                return []

            if key_point_count < kmeans_count:
                kmeans_count = key_point_count

            _, _, centers = cv2.kmeans(key_points_as_np_array, kmeans_count, None,
                                       Constants.KM_CRITERIA, Constants.KM_TRIES,
                                       Constants.KM_FLAGS)

            return centers

        @staticmethod
        def draw_points_to_image_and_save(key_points, image):
            image_copied = image.copy()
            cv2.drawKeypoints(image_copied, key_points, image_copied)
            # ImageUtils.IO.saveJpg('keypoints', image_copied)
