import Constants
from ImageUtils import ImageUtils


class ValidatorError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ImageClassifier:
    def __init__(self):
        pass

    def classify(self, data):
        return len(data), data


class FeatureClassifier(ImageClassifier):
    def __init__(self, cascade_path):
        import cv2
        # os.path.exists(cascade_path)
        self.sift = cv2.SIFT_create()
        self.cascade = cv2.CascadeClassifier(cascade_path)

    def classify(self, gray):
        data = self.cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        return super().classify(data)


class EyeClassifier(FeatureClassifier):
    def __init__(self):
        super().__init__(Constants.CLASSIFIER_EYE)

    def classify(self, gray):
        return super().classify(gray)


class FaceClassifier(FeatureClassifier):
    def __init__(self):
        super().__init__(Constants.CLASSIFIER_FACE)

    def classify(self, gray):
        _, data = super().classify(gray)
        verified_data = []
        for data_point in data:
            try:
                FaceValidator().validate(gray, data_point)
                verified_data.append(data_point)
            except ValidatorError:
                pass

        return len(verified_data), verified_data


class ColorClassifier(ImageClassifier):
    def __init__(self, color=Constants.COLOR_GREEN, count=Constants.KM_GROUP_COUNT):
        from ImageUtils import Colors
        import cv2
        self.color = color
        self.lower, self.upper = Colors.getColorLimits(color)
        self.count = count
        self.sift = cv2.SIFT_create()

    def classify(self, hsv):
        from PointClouds import PointCloud
        point_cloud = PointCloud.fromLimits(hsv, self.sift, self.lower, self.upper, count=self.count, color=self.color)
        data = point_cloud.get_as_xy_wh()
        return super().classify(data)


class ImageValidator:
    def __init__(self):
        pass

    def validate(self, img, data):
        if img is None:
            raise ValidatorError(f'Image is None')
        if data is None:
            raise ValidatorError(f'Data is None')


class FaceValidator(ImageValidator):
    def __init__(self):
        self.eye_classifier = EyeClassifier()

    def validate(self, gray, data_point):
        x, y, w, h = data_point
        face_img = ImageUtils.getSubImage(gray, x, y, w, h)
        count, _ = self.eye_classifier.classify(face_img)
        if count < Constants.EYES_MINIMUM:
            raise ValidatorError(f'Face is not valid. Eye count is lower than {count}')


class ColorValidator(ImageValidator):
    def __init__(self):
        pass

    def validate(self, hsv, data):
        if 0 >= len(data):
            raise ValidatorError(f'No objects found!')


class ImageDetector:
    def __init__(self, classifier: ImageClassifier, validator: ImageValidator):
        self.classifier = classifier
        self.validator = validator

    def detect(self, image):
        data = self.classifier.classify(image)
        self.validator.validate(image, data)
        return data


class FaceDetector(ImageDetector):
    def __init__(self):
        super().__init__(FaceClassifier(), FaceValidator())

    def detect(self, image):
        return super().detect(image)


class ColorDetector(ImageDetector):
    def __init__(self):
        super().__init__(ColorClassifier(), ColorValidator())

    def detect(self, image):
        return super().detect(image)
