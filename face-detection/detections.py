import datetime

import cv2
import numpy
import numpy as np
from deepface import DeepFace

import Constants
from Logger import CustomLogger
from db.sql import SqlUtil
from images import ImageUtils

logger = CustomLogger(__name__).get_logger()


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

    def log(self):
        logger.info(f'Capture device: {self.width}, {self.height}, {self.center}')


class Classifier:
    def __init__(self):
        self.result = []

    def classify(self, image):
        pass


class ClassifierResult:
    def __init__(self):
        pass


class Rectangle:
    # Time in seconds
    survival_time = float(Constants.RECTANGLE_MAX_AGE)

    def __init__(self, x, y, width, height, bgr=[255, 255, 255]):
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.center = (self.x + (self.width / 2), self.y + (self.height / 2))
        self.color = bgr
        self.creation_time = datetime.datetime.now().timestamp()

    def get_age(self):
        now = datetime.datetime.now().timestamp()
        age = now - self.creation_time
        return float(age)

    def get_color_by_age(self):
        age = self.get_age()
        factor_age = ((100 / Rectangle.survival_time) * age) / 100
        b, g, r = self.color
        b = int(b - factor_age * 255)
        g = int(g - factor_age * 255)
        r = int(factor_age * 255)
        if b < 0:
            b = 0
        if g < 0:
            g = 0
        return [b, g, r]

    def is_alive(self):
        age = self.get_age()
        return age < Rectangle.survival_time

    def __str__(self):
        return f'Rectangle(x={self.x}, y={self.y}, width={self.width}, height={self.height}, center={self.center})'

    def scale(self, scale=1.0):
        self.x = int(self.x * scale)
        self.y = int(self.y * scale)
        self.width = int(self.width * scale)
        self.height = int(self.height * scale)
        self.center = (self.x + (self.width / 2), self.y + (self.height / 2))
        return self

    def draw(self, image, only_center=False, radius=4, thickness=2):
        center_x, center_y = self.center
        image = cv2.putText(image, f'{self.center}', (int(center_x), int(center_y)), Constants.TEXT_FONT,
                            Constants.TEXT_FONT_SCALE, self.get_color_by_age(), thickness=1)
        if only_center:
            cv2.circle(image, (int(center_x), int(center_y)), radius, color=self.get_color_by_age(),
                       thickness=thickness)
        else:
            cv2.circle(image, (int(center_x), int(center_y)), 2, color=self.get_color_by_age(), thickness=2)
            cv2.rectangle(image, (self.x, self.y), (self.x + self.width, self.y + self.height),
                          color=self.get_color_by_age(), thickness=1)

    # Rectangle.distance(s_temp, s)
    @staticmethod
    def distance(rectangle_1, rectangle_2):
        a = numpy.array(rectangle_1.center)
        b = numpy.array(rectangle_2.center)
        return numpy.linalg.norm(a - b)

    @staticmethod
    def get_steps(rectangle_1, rectangle_2):
        x1, y1 = rectangle_1.center
        x2, y2 = rectangle_2.center
        # logger.info(f'{rectangle_1.center}, {rectangle_2.center}')
        return x2 - x1, y2 - y1


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
        from images import ImageUtils
        gray_scaled = ImageUtils.scaleImage(gray, scale)
        return super().classify(gray_scaled)


class FaceClassifier(CascadeClassifier):
    def __init__(self):
        super().__init__('haarcascade_frontalface_default.xml')
        self.eye_classifier = EyeClassifier()

    @staticmethod
    def analyze(image, actions=['age', 'gender', 'race', 'emotion']) -> tuple[str, str, {}]:
        try:
            data = DeepFace.analyze(
                image,
                actions=actions,
                detector_backend='opencv',
                silent=True
            )
            # logger.info(f'Data: {data[0]}')
            return data[0]
        except:
            raise ValueError('Could not analyze')

    def classify(self, image, scale=0.5):
        inverted_scale = 1 / scale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        from images import ImageUtils
        gray_scaled = ImageUtils.scaleImage(gray, scale)
        result = []
        result_faces = super().classify(gray_scaled)
        for face in result_faces:
            x, y, w, h = face
            cut_face = ImageUtils.getSubImage(gray_scaled, x, y, w, h)
            # ImageUtils.IO.saveJpg('face', cut_face)
            result_eyes = self.eye_classifier.classify(cut_face)
            if Constants.FILTER_FACES and len(result_eyes) >= Constants.EYES_MINIMUM:
                result.append(Rectangle(x, y, w, h, bgr=[0, 0, 0]).scale(inverted_scale))
        return result

    def calculate(self, gray):
        try:
            self.result = self.classify(gray)[0]
        except:
            self.result = None


class ColorGroupClassifier(Classifier):

    def __init__(self, count=Constants.KM_GROUP_COUNT, color=Constants.COLOR_TRASH):
        from images import Colors
        self.lower, self.upper = Colors.get_color_limits(color)
        self.color = color
        self.count = count
        self.sift = cv2.SIFT_create()
        self.key_points = []
        self.old_mask = None

    def classify(self, image, scale=1 / 5):
        inverted_scale = 1 / scale
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower, self.upper)
        denoised = cv2.fastNlMeansDenoising(mask, None, h=40, templateWindowSize=3, searchWindowSize=5)
        from images import ImageUtils
        scaled_mask = ImageUtils.scaleImage(denoised, scale)
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
                result.append(Rectangle(x - 10, y - 10, 20, 20, bgr=Constants.COLOR_BLACK[1]))
        if len(result) == 0:
            return None
        self.old_mask = denoised
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


class FaceUtils:
    @staticmethod
    def analyze_and_save_to_db(face):
        base64 = ImageUtils.to_base_64(face)
        try:
            analysis_result = FaceClassifier.analyze(face)
            gender = str(analysis_result['dominant_gender'])
            age = str(analysis_result['age'])
            emotion = str(analysis_result['dominant_emotion'])
            race = str(analysis_result['dominant_race'])
            logger.info(f'Person succesfully classified:\n'
                        f'------------------------------------\n'
                        f'Gender:  {gender}\n'
                        f'Age:     ~{age}\n'
                        f'Emotion: {emotion}\n'
                        f'Race:    {race}\n'
                        f'------------------------------------')
        except ValueError:
            age = 'CLASSIFIED'
            emotion = 'CLASSIFIED'
            race = 'CLASSIFIED'
            gender = 'CLASSIFIED'
        values = (base64, age, race, gender, emotion)
        SqlUtil.execute('insert into tbl_faces(base, age, race, gender, emotion) values(%s, %s, %s, %s, %s)',
                        values=values)

    @staticmethod
    def load_from_db():
        try:
            result_set = SqlUtil.execute('select * from tbl_faces', fetch='all')
        except:
            result_set = []
        return result_set

    @staticmethod
    def to_html_view(result_set):
        result = ''
        for _, base64, age, race, gender, emotion in result_set:

            base_image = base64.tobytes().decode('utf-8')
            src = f'data:image/jpeg;base64,{base_image}'
            alt = f'{race} {gender}'

            # logger.info(base_image)
            text = f'{race} {gender}<br>' \
                   f'Age:       {age}<br>' \
                   f'Currently: {emotion}<br>'

            html = f'<li class="list-item">' \
                   f'    <div>' \
                   f'        <img src="{src}" alt="{alt}"/>' \
                   f'        <p>{text}</p>' \
                   f'    </div>' \
                   f'</li>'

            result += html
        return result
