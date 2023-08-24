from typing import Any

import cv2
import numpy as np

import Constants
import ImageUtils
from Human import Face
from ImageUtils import ImageDetectionUtil
from PointClouds import PointCloud
from Shapes import Rectangle


def getFaceDistance(a, b) -> float:
    return np.linalg.norm(np.array(a)-np.array(b))


# Does not contain the camera object
class State:

    def __init__(self):
        # List of current faces
        self.sift = cv2.SIFT_create()
        self.cpGreen = ImageUtils.ColorPicker(Constants.COLOR_GREEN, Constants.KM_GROUP_COUNT)
        self.faces = None
        self.eyes = None
        # self.qrcodes = None
        self.cloud = PointCloud
        self.trashList = None
        self.trash_before = None
        # self.lastQRCodeLocation = Rectangle([-1000, -1000], [-1000, -1000], [-1000, -1000], [-1000, -1000])
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        # self.qcd = cv2.QRCodeDetector()

    def update(self, img) -> Any:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.faces, self.eyes = Face.getValidFaces(gray, self.eye_cascade, self.face_cascade)
        self.trash_before = self.trashList
        self.cloud = self.cpGreen.calculate(hsv, self.sift)
        self.trashList = self.cloud.getAsPositions()

    def visualize(self, img):
        for face in self.faces:
            face.draw(img, True, color=Constants.COLOR_GREEN)

        for eye in self.eyes:
           eye.draw(img, True, color=Constants.COLOR_PINK)

        for trash in self.trashList:
            trash.draw(img, True, color=Constants.COLOR_RED)


        # if self.cloud.keypoints == None:
        #     for point in self.cloud.points:
        #         x, y = point
        #         Rectangle.drawCircle(img, int(x), int(y))
        # else:
        #     img = cv2.drawKeypoints(img, self.cloud.keypoints, img)

        # self.lastQRCodeLocation.draw(img, True, (127, 127, 127), 3)
