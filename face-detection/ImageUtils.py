from typing import Any

import cv2
import numpy as np
from PIL import Image

import Constants


class Colors:

    @staticmethod
    def getColorLimits(color):
        range, bgr, _ = color
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
    def scaleImage(image, scale=1.0):
        image_copied = image.copy()
        width = int(image_copied.shape[1] * scale)
        height = int(image_copied.shape[0] * scale)
        dim = (width, height)

        # resize image
        resized = cv2.resize(image_copied, dim, interpolation=cv2.INTER_AREA)
        return resized

    @staticmethod
    def helperShow(img, title='Default'):
        if Constants.SHOW_HELPER:
            try:
                cv2.imshow(title, img)
            except FileNotFoundError:
                pass

    @staticmethod
    def getKeyPointsByColor(img, color, sift) -> Any:
        mask = ImageUtils.getMaskByColor(img, color)
        return ImageUtils.getKeyPointsByMask(mask, sift)

    @staticmethod
    def getKeyPoints(img, sift, color=None):
        if color is None:
            return ImageUtils.getKeyPointsByMask(img, sift)
        else:
            return ImageUtils.getKeyPointsByColor(img, color)

    @staticmethod
    def getKeyPointsByMask(mask, sift):
        kp = sift.detect(mask, None)
        return kp

    @staticmethod
    def getBoxPointsByMask(mask):
        _mask = Image.fromarray(mask)
        bbox = _mask.getbbox()  # Creates bounding box
        return bbox

    @staticmethod
    def getSubImageRect(img, position):
        a, b, c, d = position
        x1 = a[0]
        y1 = a[1]
        x2 = d[0]
        y2 = d[1]
        roi = None
        if len(img.shape) == 2:
            roi = img[y1:y2, x1:x2]

        if len(img.shape) == 3:
            roi = img[y1:y2, x1:x2]
        offset = [abs(x1), abs(y1)]
        return roi, offset

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
    def getMaskByColor(img, color):
        lower_limit, upper_limit = Colors.getColorLimits(color=color)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_limit, upper_limit)
        return mask

    @staticmethod
    def getMaskByLimits(hsv, lower_limit, upper_limit):
        # print("getMaskByLimits-----------------------------------------")
        # print(upper_limit)
        # print(lower_limit)
        # print(hsv)
        mask = None
        try:
            mask = cv2.inRange(hsv, lower_limit, upper_limit)
        except:
            return None
        return mask

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
