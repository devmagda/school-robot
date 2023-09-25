import cv2
import numpy as np

import Constants


class Colors:

    @staticmethod
    def get_color_limits(color):
        hsv_color_range, bgr, rgb = color
        c = np.uint8([[bgr]])
        hsv = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
        lower_limit = hsv[0][0][0] - hsv_color_range, Constants.HSV_LIMIT_LOWER, Constants.HSV_LIMIT_LOWER
        upper_limit = hsv[0][0][0] + hsv_color_range, Constants.HSV_LIMIT_UPPER, Constants.HSV_LIMIT_UPPER

        lower_limit = np.array(lower_limit, dtype=np.uint8)
        upper_limit = np.array(upper_limit, dtype=np.uint8)

        return lower_limit, upper_limit


class ImageUtils:

    @staticmethod
    def mirror(img, mode):
        return cv2.flip(img, mode)

    @staticmethod
    def draw_key_points(image, key_points):
        image_copy = image.copy()
        cv2.drawKeypoints(image_copy, key_points, image_copy)
        return image_copy

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
