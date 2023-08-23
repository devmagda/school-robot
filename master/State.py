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
        self.faces, self.eyes = Face.getValidFaces(img, self.eye_cascade, self.face_cascade)
        self.trash_before = self.trashList
        self.cloud = PointCloud.fromImage(img, color=Constants.FILTER_COLOR, count=10)
        # self.cloud = PointCloud.fromImage(img, color=[0, 255, 255], count=2)
        self.trashList = self.cloud.getAsPositions()

        # found, pos, enhanced = ImageDetectionUtil.getQRLocation(self.qcd, img)
        # if found:
        #    self.lastQRCodeLocation = pos
        #    self.qrcodes = pos

    def visualize(self, img):
        for face in self.faces:
            face.draw(img, True, (0, 255, 0))

        for eye in self.eyes:
            eye.draw(img, True, (255, 0, 0))

        for trash in self.trashList:
            trash.draw(img, True, (0, 0, 255))


        if self.cloud.keypoints == None:
            for point in self.cloud.points:
                x, y = point
                Rectangle.drawCircle(img, int(x), int(y))
        else:
            img = cv2.drawKeypoints(img, self.cloud.keypoints, img)

        # self.lastQRCodeLocation.draw(img, True, (127, 127, 127), 3)
