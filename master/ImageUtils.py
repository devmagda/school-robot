from typing import Any

from PIL import Image

import cv2
import numpy as np

import Constants
import PointClouds
import Shapes


class ColorPicker:

    def __init__(self, color, count):
        self.color = color
        self.lower, self.upper = Colors.getColorLimits(color)
        self.count = count

    def calculate(self, hsv, sift, scale=1.0):
        return PointClouds.PointCloud.fromLimits(hsv, sift, self.lower, self.upper, count=self.count, scale=scale, color=self.color)

class Colors:

    @staticmethod
    def getColorLimits(color):
        range, bgr, _ = color
        c = np.uint8([[bgr]])
        hsv = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
        lowerlimit = hsv[0][0][0] - range, Constants.HSV_LIMIT_LOWER, Constants.HSV_LIMIT_LOWER
        upperlimit = hsv[0][0][0] + range, Constants.HSV_LIMIT_UPPER, Constants.HSV_LIMIT_UPPER

        lowerlimit = np.array(lowerlimit, dtype=np.uint8)
        upperlimit = np.array(upperlimit, dtype=np.uint8)

        return lowerlimit, upperlimit


class ImageDetectionUtil:

    @staticmethod
    def scaleImage(img, scale=1.0):
        width = int(img.shape[1] * scale)
        height = int(img.shape[0] * scale)
        dim = (width, height)

        # resize image
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        return resized

    @staticmethod
    def helperShow(img, title='Default'):
        try:
            cv2.imshow(title, img)
        except:
            True

    @staticmethod
    def getKeyPointsByColor(img, color, sift) -> Any:
        mask = ImageDetectionUtil.getMaskByColor(img, color)
        return ImageDetectionUtil.getKeyPointsByMask(mask, sift)

    @staticmethod
    def getKeyPoints(img, sift, color=None):
        if color is None:
            return ImageDetectionUtil.getKeyPointsByMask(img, sift)
        else:
            return ImageDetectionUtil.getKeyPointsByColor(img, color)

    @staticmethod
    def getKeyPointsByMask(mask, sift):
        kp = sift.detect(mask, None)
        return kp

    @staticmethod
    def getBoxPointsByMask(mask):
        _mask = Image.fromarray(mask)
        bbox = _mask.getbbox()  # Creates bounding box
        return bbox

    @staticmethod
    def getObjectByCascade(cascade, gray, offset=[0, 0], color=Constants.COLOR_BLACK) -> [Shapes.Rectangle]:
        xOffset = offset[0]
        yOffset = offset[1]
        faces = cascade.detectMultiScale(gray, 1.1, 4)
        ret = []
        for (x, y, w, h) in faces:
            x = xOffset + x
            y = yOffset + y
            ret.append(Shapes.Rectangle([x, y], [x + w, y], [x, y + h], [x + w, y + h], color=color))
        return ret

    @staticmethod
    def getSubImage(img, position):
        a, b, c, d = position
        x1 = a[0]
        y1 = a[1]
        x2 = d[0]
        y2 = d[1]
        roi = None
        if len(img.shape) == 2:
            roi = img[y1:y2, x1:x2]

        if len(img.shape) == 3:
            roi = img[y1:y2, x1:x2, 0:3]
        offset = [abs(x1), abs(y1)]
        return roi, offset

    @staticmethod
    def getMaskByColor(img, color):
        lower_limit, upper_limit = Colors.getColorLimits(color=color)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_limit, upper_limit)
        return mask

    @staticmethod
    def getMaskByLimits(hsv, lower_limit, upper_limit):
        # print("getMaskByLimits-----------------------------------------")
        # print(upper_limit)
        # print(lower_limit)
        # print(hsv)
        mask = None
        try:
            mask = cv2.inRange(hsv, lower_limit, upper_limit)
        except:
            return None
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
