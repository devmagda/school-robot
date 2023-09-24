from typing import Any

import cv2
import numpy as np

import Constants
from Human import FacesUtil
from ImageUtils import ColorPicker, ImageUtils
from imagedetector import ColorDetector, FaceDetector


def getFaceDistance(a, b) -> float:
    return np.linalg.norm(np.array(a)-np.array(b))


# Does not contain the camera object
class State:

    def __init__(self):

        self.objects_by_color_detector = ColorDetector(Constants.COLOR_TRASH)
        self.faces_detector = FaceDetector()

        # OpenCV objects
        self.sift = cv2.SIFT_create()
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

        # Color Selectors
        self.cpGreen = ColorPicker(Constants.COLOR_GREEN, Constants.KM_GROUP_COUNT)

        # Objects to Track
        self.faces = None
        self.found = False
        self.eyes = None
        self.trashes = None
        self.old = None
        # self.qrcodes = None

        # Point cloud to find objects
        self.cloud = None

    def update(self, img) -> Any:
        from imagedetector import ColorDetector
        from imagedetector import FaceDetector
        # Images to generate per frame to save in conversion time (e.g. Only run Once)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # self.face_detector_test(gray, hsv)

        # Updating values
        self.faces, self.found = \
            FacesUtil.get_valid_faces(gray, self.eye_cascade, self.face_cascade, scale=Constants.FACE_DETECTION_SCALE)

        if self.found and self.old is not None and Constants.DO_FACE_COMPARISON:
            x, y, w, h = self.old.to_x_y_width_height()
            scale = 1/4
            margin = 50

            img1 = ImageUtils.getSubImage(img, x, y, w, h, margin=Constants.FACE_COMPARISON_MARGIN)
            img1 = ImageUtils.scaleImage(img1, scale=Constants.FACE_COMPARISON_SCALE)

            cv2.imshow('Web Capture img2', img1)
            for i, face in enumerate(self.faces):
                x, y, w, h = face.to_x_y_width_height()
                img2 = ImageUtils.getSubImage(img, x, y, w, h, margin=Constants.FACE_COMPARISON_MARGIN)
                img2 = ImageUtils.scaleImage(img2, scale=Constants.FACE_COMPARISON_SCALE)
                verified, distance, threshold = FacesUtil.compare(img1, img2)
                try:
                    d = FacesUtil.analyze(img1)
                    print(d)
                except:
                    pass
                cv2.imshow(f'Web Capture img2 {i}', img2)
                print(verified, distance, threshold, end='')

        if self.found:
            self.old = self.faces[0]

        # print("HSV: " + str(hsv))
        self.cloud = self.cpGreen.calculate(hsv, self.sift, scale=Constants.SCALE_OBJECT_DETECTION)
        if self.cloud is not None:
            self.trashes = self.cloud.getAsPositions(img=img)

    def face_detector_test(self, gray, hsv):
        from imagedetector import ColorDetector
        cd = ColorDetector()
        from imagedetector import FaceDetector
        fd = FaceDetector()
        try:
            # print('\nFace  Detection: ', end='')
            print(fd.detect(gray), end='')
        except:
            pass
        try:
            print('\nColor  Detection: ', end='')
            # print(cd.detect(hsv), end='')
        except:
            pass

    def visualize(self, img):

        if self.found:
            for face in self.faces:
                face.draw(img, True)

        # for eye in self.eyes:
        #   eye.draw(img, True, color=Constants.COLOR_PINK)
        # print(self.trashes)

        for trash in self.trashes:
            trash.draw(img, True)

        # if self.cloud.keypoints == None:
        #     for point in self.cloud.points:
        #         x, y = point
        #         Rectangle.drawCircle(img, int(x), int(y))
        # else:
        #     img = cv2.drawKeypoints(img, self.cloud.keypoints, img)
