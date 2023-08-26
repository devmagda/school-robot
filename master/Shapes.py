import cv2
import numpy as np

import Constants
import ImageUtils


class Rectangle:

    def scale(self, factor):
        a, b, c, d = self.position
        a1, a2 = a
        b1, b2 = b
        c1, c2 = c
        d1, d2 = d

        a1 = int(a1 * factor)
        a2 = int(a2 * factor)
        b1 = int(b1 * factor)
        b2 = int(b2 * factor)
        c1 = int(c1 * factor)
        c2 = int(c2 * factor)
        d1 = int(d1 * factor)
        d2 = int(d2 * factor)

        a = [a1, a2]  # upper left
        b = [b1, b2]  # upper right
        c = [c1, c2]  # lower left
        d = [d1, d2]  # lower right

        self.position = (a, b, c, d)
        self.center = Rectangle.center((a, d, c, d))

    def __init__(self, a, b, c, d, margin=0, color=Constants.COLOR_BLACK):
        a1, a2 = a
        b1, b2 = b
        c1, c2 = c
        d1, d2 = d
        a = [a1 - margin, a2 - margin]  # upper left
        b = [b1 + margin, b2 - margin]  # upper right
        c = [c1 - margin, c2 + margin]  # lower left
        d = [d1 + margin, d2 + margin]  # lower right

        self.position = [a, b, c, d]
        self.center = Rectangle.center((a, b, c, d))
        self.selected = False
        self.color = color

    def __str__(self):
        text = "Rectangle: " + str(self.position) + " -> " + str(self.center)
        return text

    @staticmethod
    def fromCenter(center, margin=50, color=Constants.COLOR_BLACK):
        x, y = center
        a = (x + margin, y + margin)
        b = (x - margin, y + margin)
        c = (x + margin, y - margin)
        d = (x - margin, y - margin)
        return Rectangle(a, b, c, d, color=color)

    @staticmethod
    def fromTwoCorners(x1, y1, x2, y2, margin=10, color=Constants.COLOR_BLACK):
        if x1 < 0:
            x1 = 0 + margin
        if y1 < 0:
            y1 = 0 + margin
        if x2 < 0:
            x2 = 10 + margin
        if y2 < 0:
            y2 = 0 + margin
        a = (x1, y1)
        b = (x2, y1)
        c = (x1, y2)
        d = (x2, y2)
        return Rectangle(a, b, c, d, margin=10, color=color)

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

    def draw(self, img, drawOutline=False, thickness=1):
        a, b, c, d = self.position
        x, y = self.center
        text = str(x) + ', ' + str(y)

        if drawOutline:
            Rectangle.drawLine(img, a, b, self.color, thickness)
            Rectangle.drawLine(img, a, c, self.color, thickness)
            Rectangle.drawLine(img, b, d, self.color, thickness)
            Rectangle.drawLine(img, c, d, self.color, thickness)

        Rectangle.drawLine(img, self.center, self.center, self.color, 6)
        Rectangle.drawText(img, x, y, color=self.color, text=text)

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

