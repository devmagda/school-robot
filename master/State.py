from typing import Any

import cv2
import numpy as np

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
        self.qrcodes = None
        self.cloud = PointCloud
        self.trash = None
        self.trash_before = None
        self.lastQRCodeLocation = Rectangle([-1000, -1000], [-1000, -1000], [-1000, -1000], [-1000, -1000])
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        # self.banana_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')
        self.qcd = cv2.QRCodeDetector()
        self.keypoints = Any

    def update(self, img) -> Any:
        self.faces = ImageDetectionUtil.getObjectByCascade(self.face_cascade, img)
        self.eyes = ImageDetectionUtil.getObjectByCascade(self.eye_cascade, img)
        self.trash_before = self.trash
        self.cloud = PointCloud.fromImage(img, color=[0, 255, 255])
        self.keypoints = ImageDetectionUtil.getKeyPointsByColor(img, [0, 255, 255])
        self.trash = self.cloud.getAsPositions()

        # distance = self.trash_before.getDistance(self.trash)

        found, pos, enhanced = ImageDetectionUtil.getQRLocation(self.qcd, img)
        if found:
            self.lastQRCodeLocation = pos
            # self.qrcodes = pos

        if self.keypoints is not None:
            d = PointCloud(self.keypoints)

        return enhanced

    def draw(self, img):
        for face in self.faces:
            face.draw(img, True, (0, 255, 0))

        for eye in self.eyes:
            eye.draw(img, True, (255, 0, 0))

        for code in self.trash:
            code.draw(img, True, (255, 255, 0))

        img = cv2.drawKeypoints(img, self.keypoints, img)

        self.lastQRCodeLocation.draw(img, True, (127, 127, 127), 3)
