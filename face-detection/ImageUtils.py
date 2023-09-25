from typing import Any

import cv2
import numpy as np
from PIL import Image

import Constants


class Colors:

    @staticmethod
    def getColorLimits(color):
        range, bgr, rgb = color
        c = np.uint8([[bgr]])
        hsv = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
        lowerlimit = hsv[0][0][0] - range, Constants.HSV_LIMIT_LOWER, Constants.HSV_LIMIT_LOWER
        upperlimit = hsv[0][0][0] + range, Constants.HSV_LIMIT_UPPER, Constants.HSV_LIMIT_UPPER

        lowerlimit = np.array(lowerlimit, dtype=np.uint8)
        upperlimit = np.array(upperlimit, dtype=np.uint8)

        return lowerlimit, upperlimit


class ImageUtils:

    @staticmethod
    def mirror(img, mode):
        return cv2.flip(img, mode)

    @staticmethod
    def scaleImage(image, scale=1.0, image_size=None):
        image_copied = image.copy()

        if image_size is None:
            width = int(image_copied.shape[1] * scale)
            height = int(image_copied.shape[0] * scale)
            image_size = (width, height)

        # resize image
        resized = cv2.resize(image_copied, image_size, interpolation=cv2.INTER_AREA)
        return resized

    @staticmethod
    def getSubImage(image, x, y, width, height):
        roi = image[y:y + height, x:x + width]
        if 0 in roi.shape:
            raise IndexError(
                'Either the image' + str(image.shape) + ' or the cropped image ' +
                str(roi.shape) + ' are not in shape!'
            )
        return roi

    @staticmethod
    def apply_mask(image, mask):
        image_copy = image.copy()
        cv2.bitwise_and(image_copy, image_copy, mask=mask)

    class IO:
        FILE_INDEX = 0

        @staticmethod
        def loadJpg(filename):
            image = cv2.imread(filename)
            if image.size == 0:
                raise ImportError("File <" + str(filename) + "> could not be loaded")
            return image

        @staticmethod
        def saveJpg(filename, image):
            index = ImageUtils.IO.FILE_INDEX
            ImageUtils.IO.FILE_INDEX = ImageUtils.IO.FILE_INDEX + 1

            filename = f'debug/{filename}_{index}.jpg'
            cv2.imwrite(filename, image)


