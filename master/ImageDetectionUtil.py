from typing import Any

import cv2
import numpy as np

from Positions import Position

# Limit Values
RANGE = 20

# Colors
BLUE = [255, 0, 0]
RED = [0, 0, 255]
GREEN = [0, 255, 0]
YELLOW = [0, 255, 255]
PINK = [255, 0, 255]
TURQUOISE = [255, 255, 0]

class Colors:

    @staticmethod
    def getColorLimits(color):
        c = np.uint8([[color]])
        hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
        p = PINK
        lowerlimit = hsvC[0][0][0] - RANGE, 100, 100
        upperlimit = hsvC[0][0][0] + RANGE, 255, 255

        lowerlimit = np.array(lowerlimit, dtype=np.uint8)
        upperlimit = np.array(upperlimit, dtype=np.uint8)

        return lowerlimit, upperlimit


class ImageDetectionUtil:

    @staticmethod
    def getKeyPointsByColor(img, color) -> Any:
        mask = ImageDetectionUtil.getMaskByColor(img, color)
        # gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        sift = cv2.SIFT_create()
        kp = sift.detect(mask, None)
        return kp

    @staticmethod
    def getObjectByCascade(cascade, img) -> [Position]:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray, 1.1, 4)
        ret = []
        for (x, y, w, h) in faces:
            ret.append(Position([x, y], [x + w, y], [x, y + h], [x + w, y + h]))
        return ret

    @staticmethod
    def getMaskByColor(img, color):
        lower_limit, upper_limit = Colors.getColorLimits(color=color)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_limit, upper_limit)
        return mask

    @staticmethod
    def getQRLocation(qcd, img) -> tuple[bool, Position, Any]:

        # Enhancing the image for better QR code locating
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # _, enhanced = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        # Retrieving the QR code data
        retval, _, points, _ = qcd.detectAndDecodeMulti(gray)
        print(points)

        if retval:
            a, b, c, d = points[0]
            return True, Position(b.astype(int), a.astype(int), c.astype(int), d.astype(int)), gray

        return False, None, gray
