from typing import Any

import cv2

from Positions import Position


class ImageDetectionUtil:

    @staticmethod
    def getKeyPoints(img) -> Any:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        sift = cv2.SIFT_create()
        kp = sift.detect(gray, None)
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


































