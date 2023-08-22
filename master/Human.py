from ImageUtils import ImageDetectionUtil
from Shapes import Rectangle


class Human:
    def __init__(self, ):
        self.eyes = [Rectangle]
        self.face = Rectangle

class Face(Rectangle):
    def __init__(self, x1, y1, x2, y2):
        super().init(x1, y1, x2, y2)

    def __init__(self, position):
        x1, y1, x2, y2 = position
        super().__init__(x1, y1, x2, y2)

    @staticmethod
    def getValidFaces(image, eyecascade, facecascade):
        faces = Face.getFromImg(image, facecascade)
        eyes = Eye.getFromImg(image, eyecascade)
        faces = list(filter(lambda f: Eye.getEyesInsidePosition(f, eyes), faces))
        return faces

    @staticmethod
    def getFromImg(image, cascade):
        return ImageDetectionUtil.getObjectByCascade(cascade, image)

class Eye(Rectangle):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)

    def __init__(self, position):
        x1, y1, x2, y2 = position
        super().__init__(x1, y1, x2, y2)

    @staticmethod
    def getFromImg(image, cascade):
        return ImageDetectionUtil.getObjectByCascade(cascade, image)


    # Needs Refactoring
    # here, we always check the same image again..
    @staticmethod
    def getEyesInsidePosition(position, eyes):
        ret = [Rectangle]
        for eye in eyes:
            if position.contains(eye):
                ret.append(position)
                print(str("Adding: " + str(position)))
        return len(ret)
