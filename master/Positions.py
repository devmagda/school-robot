import cv2
import numpy as np


class Position:

    def __init__(self, a, b, c, d):
        self.position = [a, b, c, d]
        self.center = Position.center((a, b, c, d))
        self.selected = False

    def __str__(self):
        text = "Position: " + str(self.position) + " -> " + str(self.center)
        return text

    def contains(self, other):
        x1, y1, x2, y2 = self.position
        a, b = self.center
        return (a >= x1 & a <= x2) & (b >= y1 & b <= y2)

    @staticmethod
    def center(face):
        points = np.array(face)
        x, y = np.mean(points, axis=0)
        return [int(x), int(y)]

    def draw(self, img, drawOutline=False, color=(0, 255, 0), thickness=1):
        a, b, c, d = self.position
        if self.selected:
            x, y = self.center
            color = (0, 0, 255) # Red
            Position.drawCircle(img, x, y, color)

        if drawOutline:
            Position.drawLine(img, a, b, color, thickness)
            Position.drawLine(img, a, c, color, thickness)
            Position.drawLine(img, b, d, color, thickness)
            Position.drawLine(img, c, d, color, thickness)

        Position.drawLine(img, self.center, self.center, color, 6)

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
