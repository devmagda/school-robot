import threading
from typing import Any

import cv2
import numpy as np

import Constants
from Human import FacesUtil
from ImageUtils import ColorPicker, ImageUtils


def getFaceDistance(a, b) -> float:
    return np.linalg.norm(np.array(a)-np.array(b))


# Does not contain the camera object
class State:

    def __init__(self):

        # OpenCV objects
        self.sift = cv2.SIFT_create()
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

        # Color Selectors
        self.selector = ColorPicker(Constants.OBJECT_COLOR, Constants.KM_GROUP_COUNT)

        # Objects to Track
        self.faces = None
        self.found = False
        self.eyes = None
        self.trashes = None
        self.old = None
        self.thread = None
        # self.qrcodes = None

        # Point cloud to find objects
        self.cloud = None

    def update(self, img) -> Any:
        # from api.img.api import Client
        # Images to generate per frame to save in conversion time (e.g. Only run Once)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Client.post_faces(img)
        # Updating values
        self.faces, self.found = \
            FacesUtil.get_valid_faces(gray, self.eye_cascade, self.face_cascade, scale=Constants.FACE_DETECTION_SCALE)

        if self.found and self.old is not None and Constants.DO_FACE_COMPARISON:
            x, y, w, h = self.old.to_x_y_width_height()

            img1 = ImageUtils.getSubImage(img, x, y, w, h, margin=Constants.FACE_COMPARISON_MARGIN)
            img1 = ImageUtils.scaleImage(img1, scale=Constants.FACE_COMPARISON_SCALE)

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
                print(verified, distance, threshold, end='')
        print()  # print after to still have a new line

        if self.found:
            self.old = self.faces[0]

        self.cloud = self.selector.calculate(hsv, self.sift, scale=Constants.SCALE_OBJECT_DETECTION)
        if self.cloud is not None:
            self.trashes = self.cloud.getAsPositions(img=img)

    def visualize(self, img):

        if self.found:
            for face in self.faces:
                face.draw(img, True)

        # for eye in self.eyes:
        #   eye.draw(img, True, color=Constants.COLOR_PINK)

        for trash in self.trashes:
            trash.draw(img, True)

        # if self.cloud.keypoints == None:
        #     for point in self.cloud.points:
        #         x, y = point
        #         Rectangle.drawCircle(img, int(x), int(y))
        # else:
        #     img = cv2.drawKeypoints(img, self.cloud.keypoints, img)
