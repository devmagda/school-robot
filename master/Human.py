import Constants
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
    def getValidFaces(gray, eyeCascade, faceCascade):
        faces = Face.getFromImg(gray, faceCascade)
        validFaces = []

        if len(faces) == 0:
            return [], []

        for face in faces:
            a, b, c, d = face.position
            x1 = a[0]
            y1 = a[1]
            x2 = d[0]
            y2 = d[1]
            roi = gray[y1:y2, x1:x2]
            eyes = Eye.getFromImg(roi, eyeCascade, offset=[x1, y1])
            if len(eyes) >= 2:
                validFaces.append(face)

        # faces = list(filter(lambda f: (Eye.getEyesInsidePosition(f, eyes) >= 2) or Constants.FILTER_FACES , faces))
        return faces, eyes

    @staticmethod
    def getFromImg(gray, cascade):
        return ImageDetectionUtil.getObjectByCascade(cascade, gray)


class Eye(Rectangle):

    def __init__(self, position):
        x1, y1, x2, y2 = position
        super().__init__(x1, y1, x2, y2)

    @staticmethod
    def getFromImg(image, cascade, offset=[0, 0]):
        return ImageDetectionUtil.getObjectByCascade(cascade, image, offset)

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
