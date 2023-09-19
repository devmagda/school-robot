import os.path


class ImageClassifier:
    def __init__(self):
        pass

    def classify(self, data):
        pass


class FeatureClassifier(ImageClassifier):
    def __init__(self, cascade_path):
        import cv2
        # os.path.exists(cascade_path)
        self.sift = cv2.SIFT_create()
        self.cascade = cv2.CascadeClassifier(cascade_path)

    def classify(self, gray):
        data = self.cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        return data


class Detector:

    def __init__(self, classifier: ImageClassifier):
        self.classifier = classifier
