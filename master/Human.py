from ImageDetectionUtil import ImageDetectionUtil
from Positions import Position


class Human:
    def __init__(self, ):
        self.eyes = [Position]
        self.face = Position

class Face(Position):
    def __init__(self, x1, y1, x2, y2):
        super().init(x1, y1, x2, y2)

class Eye(Position):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)

    def __init__(self, position):
        x1, y1, x2, y2 = position
        super().__init__(x1, y1, x2, y2)

    @staticmethod
    def getFromImg(image, cascade):
        return ImageDetectionUtil.getObjectByCascade(cascade, image)

    @staticmethod
    def getInsidePosition(image, cascade, position):
        positions = Eye.getFromImg(image, cascade)
        ret = [Position]
        for pos in positions:
            print(position)
            if (position.contains(pos)):
                ret.__add__(position)
                print(str("Adding: " + str(position)))
        return ret


class Body:
    @staticmethod
    def getFromImg(image):
        print("test")
