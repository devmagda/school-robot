import cv2
import numpy as np

import ImageUtils
import Shapes


class PointCloud:

    @staticmethod
    def fromKeypoints(keypoints):
        nparray = np.empty((len(keypoints), 2), np.float32) # creates empty 2d numpy array

        for i in range(len(keypoints)):
            x = np.float32(keypoints[i].pt[0])
            y = np.float32(keypoints[i].pt[1])
            nparray[i] = (x, y)

        return nparray

    def __init__(self, keypoints, count):
        self.points = PointCloud.fromKeypoints(keypoints)
        self.centers = []
        self.labels = []
        self.compactness = 0
        self.keypoints = keypoints
        if len(self.points) > 10:
            self.group(count)


    def group(self, n):
        # Define criteria = ( type, max_iter = 10 , epsilon = 1.0 )
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 2.0)
        # Set flags (Just to avoid line break in the code)
        flags = cv2.KMEANS_RANDOM_CENTERS
        # if len(self.points) >
        # Apply KMeans
        self.compactness, self.labels, self.centers = cv2.kmeans(self.points, n, None, criteria, 5, flags)

    def getAsPositions(self):
        rects = []
        if not len(self.centers) == 0:
            for c in self.centers:
                x, y = int(c[0]), int(c[1])
                rects.append(Shapes.Rectangle.fromCenter((x, y)))
        return rects

    @staticmethod
    def fromImage(img, color=None, count=5):
        selfkeypoints = None
        if color is None:
            keypoints = ImageUtils.ImageDetectionUtil.getKeyPoints(img)
        else:
            keypoints = ImageUtils.ImageDetectionUtil.getKeyPointsByColor(img, color)

        if keypoints is not None:
            return PointCloud(keypoints, count)

        return None



