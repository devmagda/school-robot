import cv2
import numpy as np

import matplotlib.pyplot as plt

import Constants
import ImageUtils
import Shapes


class PointCloud:

    @staticmethod
    def fromKeypoints(keypoints, count=5):
        nparray = np.empty((len(keypoints), 2), np.float32) # creates empty 2d numpy array

        for i in range(len(keypoints)):
            x = np.float32(keypoints[i].pt[0])
            y = np.float32(keypoints[i].pt[1])
            nparray[i] = (x, y)

        return PointCloud(nparray, count, keypoints=keypoints)

    def __init__(self, points, count=5, keypoints=None):
        self.points = points
        self.centers = None
        self.labels = None
        self.compactness = 0
        self.keypoints = keypoints
        if len(self.points) > 10:
            self.group(count)
        # print("Done")


    def group(self, n):
        # graph = self.getElbowGraphData()
        self.compactness, self.labels, self.centers = PointCloud.kmeans(self.points, n)


    def getElbowGraphData(self):
        comps = []
        counts = []
        for n in range(1, int(len(self.points) / 4.0)):
            compac, _, _ = PointCloud.kmeans(self.points, n)
            comps.append(compac)
            counts.append(n)
        # print("Compactnesses: " + str(comps))
        # print("Counts       : " + str(comps))
        plt.plot(counts, comps)
        plt.axis([0, 6, 0, 10000000])
        plt.show()
        return list


    @staticmethod
    def kmeans(points, n=5):
        return cv2.kmeans(points, n, None, Constants.KM_CRITERIA, Constants.KM_TRIES, Constants.KM_FLAGS)


    def getAsPositions(self):
        rects = []
        if self.centers is None:
            return rects
        if not len(self.centers) == 0:
            for c in self.centers:
                x, y = int(c[0]), int(c[1])
                rects.append(Shapes.Rectangle.fromCenter((x, y)))
        return rects



    @staticmethod
    def fromImage(img, color=None, count=5):
        selfkeypoints = None
        keypoints = ImageUtils.ImageDetectionUtil.getKeyPoints(img, color)
        if keypoints is not None:
            return PointCloud.fromKeypoints(keypoints, Constants.KM_GROUP_COUNT)
        return None





