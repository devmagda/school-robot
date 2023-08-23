from ImageUtils import ImageDetectionUtil
from Shapes import Rectangle


class Human:
    def __init__(self, ):
        self.eyes = [Rectangle]
        self.face = Rectangle


class Face(Rectangle):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)

    @staticmethod
    def getValidFaces(image, eyeCascade, faceCascade):
        faces = Face.getFromImg(image, faceCascade)
        eyes = Eye.getFromImg(image, eyeCascade)
        faces = list(filter(lambda f: Eye.getEyesInsidePosition(f, eyes) >= 2, faces))
        return faces, eyes

    @staticmethod
    def getFromImg(image, cascade):
        return ImageDetectionUtil.getObjectByCascade(cascade, image)


class Eye(Rectangle):

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
                # print(str("Adding: " + str(position)))
        return len(ret)
