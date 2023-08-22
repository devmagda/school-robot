from typing import Any

import cv2
import numpy as np

from ImageUtils import ImageDetectionUtil
from Positions import Position


def getFaceDistance(a, b) -> float:
    return np.linalg.norm(np.array(a)-np.array(b))


# Does not contain the camera object
class State:

    def __init__(self):
        # List of current faces
        self.faces = [Position]
        self.qrcodes = [Position]
        self.objects = Position
        self.lastQRCodeLocation = Position([-1000, -1000], [-1000, -1000], [-1000, -1000], [-1000, -1000])
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        # self.banana_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')
        self.qcd = cv2.QRCodeDetector()
        self.keypoints = Any

    def update(self, img) -> Any:
        self.faces = ImageDetectionUtil.getObjectByCascade(self.face_cascade, img)
        self.eyes = ImageDetectionUtil.getObjectByCascade(self.eye_cascade, img)
        self.keypoints = ImageDetectionUtil.getKeyPointsByColor(img, [255, 0, 0])
        self.objects = Position.getPositionByColor(img, [0, 255, 255])
        found, pos, enhanced = ImageDetectionUtil.getQRLocation(self.qcd, img)
        if found:
            self.lastQRCodeLocation = pos
            # self.qrcodes = pos
        return enhanced

    def draw(self, img):
        # for face in self.faces:
        #     face.draw(img, True, (255, 255, 255))

        # for code in self.eyes:
        #     code.draw(img, True, (255, 255, 0))

        self.objects.draw(img, True, (255, 255, 0))

        img = cv2.drawKeypoints(img, self.keypoints, img)

        self.lastQRCodeLocation.draw(img, True, (127, 127, 127), 3)
