from typing import Any

from PIL import Image

import cv2
import numpy as np

import Shapes
from PointClouds import PointCloud

# Limit Values
RANGE = 10
LOWER = 100
UPPER = 255


class Colors:

    @staticmethod
    def createColorMap():
        blue = [255, 0, 0]
        pink = [255, 0, 255]
        red = [0, 0, 255]
        yellow = [0, 255, 255]
        green = [0, 255, 0]
        turquoise = [255, 255, 0]

    @staticmethod
    def getColorLimits(color):
        c = np.uint8([[color]])
        hsv = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
        lowerlimit = hsv[0][0][0] - RANGE, LOWER, LOWER
        upperlimit = hsv[0][0][0] + RANGE, UPPER, UPPER

        lowerlimit = np.array(lowerlimit, dtype=np.uint8)
        upperlimit = np.array(upperlimit, dtype=np.uint8)

        return lowerlimit, upperlimit


class ImageDetectionUtil:

    @staticmethod
    def getKeyPointsByColor(img, color) -> Any:
        mask = ImageDetectionUtil.getMaskByColor(img, color)
        return ImageDetectionUtil.getKeyPointsByMask(mask)

    @staticmethod
    def getKeyPoints(img):
        mask = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return ImageDetectionUtil.getKeyPointsByMask(mask)

    @staticmethod
    def getKeyPointsByMask(mask):
        sift = cv2.SIFT_create()
        return sift.detect(mask, None)
    @staticmethod
    def getOneRectByColor(img, color) -> Shapes.Rectangle:

        cloud = PointCloud.fromImage(img)

    @staticmethod
    def getBoxPointsByMask(mask):
        _mask = Image.fromarray(mask)
        bbox = _mask.getbbox()  # Creates bounding box
        return bbox

    @staticmethod
    def getObjectByCascade(cascade, img) -> [Shapes.Rectangle]:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray, 1.1, 4)
        ret = []
        for (x, y, w, h) in faces:
            ret.append(Shapes.Rectangle([x, y], [x + w, y], [x, y + h], [x + w, y + h]))
        return ret

    @staticmethod
    def getMaskByColor(img, color):
        lower_limit, upper_limit = Colors.getColorLimits(color=color)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_limit, upper_limit)
        return mask

    @staticmethod
    def getQRLocation(qcd, img) -> tuple[bool, Shapes.Rectangle, Any]:

        # Enhancing the image for better QR code locating
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # _, enhanced = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        # Retrieving the QR code data
        retval, _, points, _ = qcd.detectAndDecodeMulti(gray)
        # print(points)

        if retval:
            a, b, c, d = points[0]
            return True, Shapes.Rectangle(b.astype(int), a.astype(int), c.astype(int), d.astype(int)), gray

        return False, None, gray
