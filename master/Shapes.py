import cv2
import numpy as np

import ImageUtils


class Rectangle:

    def __init__(self, a, b, c, d):
        self.position = [a, b, c, d]
        self.center = Rectangle.center((a, b, c, d))
        self.selected = False

    def __str__(self):
        text = "Rectangle: " + str(self.position) + " -> " + str(self.center)
        return text

    @staticmethod
    def fromTwoCorners(x1, y1, x2, y2):
        b = (x1, y1)
        a = (x2, y1)
        c = (x2, y2)
        d = (x1, y2)
        return Rectangle(a, b, c, d)

    def contains(self, other):
        x1, y1, x2, y2 = self.position
        a, b = self.center
        return (a >= x1 & a <= x2) & (b >= y1 & b <= y2)

    @staticmethod
    def center(face):
        points = np.array(face)
        x, y = np.mean(points, axis=0)
        return [int(x), int(y)]

    @staticmethod
    def getRectByColor(img, color):
        mask = ImageUtils.ImageDetectionUtil.getMaskByColor(img, color)
        bbox = ImageUtils.ImageDetectionUtil.getBoxPointsByMask(mask)
        if bbox is not None:
            x1, y1, x2, y2 = bbox
            pos = Rectangle.fromTwoCorners(x1, y1, x2, y2)
            return pos
        return Rectangle((-100, -100), (-100, -100), (-100, -100), (-100, -100))

    def draw(self, img, drawOutline=False, color=(0, 255, 0), thickness=1):
        a, b, c, d = self.position

        if self.selected:
            x, y = self.center
            color = (0, 0, 255) # Red
            Rectangle.drawCircle(img, x, y, color)

        if drawOutline:
            Rectangle.drawLine(img, a, b, color, thickness)
            Rectangle.drawLine(img, a, c, color, thickness)
            Rectangle.drawLine(img, b, d, color, thickness)
            Rectangle.drawLine(img, c, d, color, thickness)

        Rectangle.drawLine(img, self.center, self.center, color, 6)

    @staticmethod
    def drawLine(img, a, b, color, t):
        ax, ay = a
        bx, by = b
        cv2.line(img, [ax, ay], [bx, by], color, t)

    @staticmethod
    def drawCircle(img, a, b, color):
        cv2.circle(img, (a, b), 10, color, 5)

    def toNumpyArray(self) -> np.array:
        return np.array(self.center)

    def getDistance(self, other) -> float:
        a = self.toNumpyArray()
        b = other.toNumpyArray()
        return np.linalg.norm(a - b)

    # def getCenter(self, other) -> np.array:
