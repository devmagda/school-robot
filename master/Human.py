import Constants
import ImageUtils
from ImageUtils import ImageDetectionUtil
from Shapes import Rectangle

class Faces():

    @staticmethod
    def getValidFaces(gray, eyeCascade, faceCascade, scale=1.0):

        found = False

        # Scale image
        gray = ImageUtils.ImageDetectionUtil.scaleImage(gray, scale)

        faces = Faces.getFromImg(gray, faceCascade)

        c = 0

        validFaces = []

        if len(faces) == 0:
            # print("No faces found")
            return [], []

        for face in faces:
            roi, offset = ImageUtils.ImageDetectionUtil.getSubImage(gray, face.position)
            eyes = Eyes.getFromImg(roi, eyeCascade, offset=offset)
            x = len(eyes)
            if x >= Constants.EYES_MINIMUM or not Constants.FILTER_FACES:
                found = True
                face.scale(1/scale)
                validFaces.append(face)
                c = c + 1
                ImageUtils.ImageDetectionUtil.helperShow(roi, 'Faces')

        return validFaces, found

    @staticmethod
    def getFromImg(gray, cascade):
        return ImageDetectionUtil.getObjectByCascade(cascade, gray, color=Constants.FACES_COLOR)


class Eyes():

    @staticmethod
    def getFromImg(image, cascade, offset=[0, 0]):
        return ImageDetectionUtil.getObjectByCascade(cascade, image, offset, color=Constants.EYES_COLOR)
