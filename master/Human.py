import Constants
import ImageUtils
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
    def getValidFaces(gray, eyeCascade, faceCascade, scale=1.0):

        # Scale image
        gray = ImageUtils.ImageDetectionUtil.scaleImage(gray, scale)
        faces = Face.getFromImg(gray, faceCascade)
        eyes = None
        c = 0

        validFaces = []

        if len(faces) == 0:
            # print("No faces found")
            return [], []

        for face in faces:
            roi, offset = ImageUtils.ImageDetectionUtil.getSubImage(gray, face.position)
            eyes = Eye.getFromImg(roi, eyeCascade, offset=offset)
            x = len(eyes)
            if x >= 2 or not Constants.FILTER_FACES:
                face.scale(1/scale)
                validFaces.append(face)
                c = c + 1
                ImageUtils.ImageDetectionUtil.helperShow(roi, 'Faces_' + str(c))

        return validFaces

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
