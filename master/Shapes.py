import cv2
import numpy as np

import Constants
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
    def fromCenter(center, margin=50, color=[0, 255, 0]):
        x, y = center
        a = (x + margin, y + margin)
        b = (x - margin, y + margin)
        c = (x + margin, y - margin)
        d = (x - margin, y - margin)
        return Rectangle(a, b, c, d)

    @staticmethod
    def fromTwoCorners(x1, y1, x2, y2):
        b = (x1, y1)
        a = (x2, y1)
        c = (x2, y2)
        d = (x1, y2)
        return Rectangle(a, b, c, d)

    def contains(self, other):
        x, _, _, y = self.position
        x1, x2 = x
        y1, y2 = y
        a, b = other.center

        # print("[" + str(a) + "] >= " + str(x1) + " & [" + str(a) + "] <= " + str(y1) + " & [" + str(b) + "] >= " + str(x2) + " & [" + str(b) + "] <= " + str(y2))
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

    def draw(self, img, drawOutline=False, color=Constants.COLOR_WHITE, thickness=1):
        a, b, c, d = self.position
        x, y = self.center
        text = str(x) + ', ' + str(y)

        if drawOutline:
            Rectangle.drawLine(img, a, b, color, thickness)
            Rectangle.drawLine(img, a, c, color, thickness)
            Rectangle.drawLine(img, b, d, color, thickness)
            Rectangle.drawLine(img, c, d, color, thickness)

        Rectangle.drawLine(img, self.center, self.center, color, 6)
        Rectangle.drawText(img, x, y, color=color, text=text)

    @staticmethod
    def drawLine(img, a, b, color, t):
        _, _, rgb = color
        ax, ay = a
        bx, by = b
        cv2.line(img, [ax, ay], [bx, by], rgb, t)

    def toNumpyArray(self) -> np.array:
        return np.array(self.center)

    def getAngle(self, other) -> float:
        a = self.toNumpyArray()
        b = other.toNumpyArray()
        c = a - b
        return np.angle(c, deg=True)

    def getDistance(self, other) -> float:
        a = self.toNumpyArray()
        b = other.toNumpyArray()
        return np.linalg.norm(a - b)

    @staticmethod
    def drawText(img, x, y, color=Constants.COLOR_WHITE, text='No Text Specified'):
        _, _, rgb = color
        org = (x, y)
        cv2.putText(img, text, org, Constants.TEXT_FONT, Constants.TEXT_FONT_SCALE, rgb, Constants.TEXT_FONT_THICK, cv2.LINE_AA)

    # def getCenter(self, other) -> np.array:

