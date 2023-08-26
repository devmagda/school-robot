import cv2
import numpy as np

import matplotlib.pyplot as plt

import Constants
import ImageUtils
import Shapes


class PointCloud:

    @staticmethod
    def fromLimits(hsv, sift,  lowerLimit, upperLimit, count=5, scale=1.0):
        # print("hsv______________")
        # print(hsv)
        hsv = ImageUtils.ImageDetectionUtil.scaleImage(hsv, scale=scale)
        mask = ImageUtils.ImageDetectionUtil.getMaskByLimits(hsv, lowerLimit, upperLimit)
        mask = cv2.fastNlMeansDenoising(mask, None, h=20,  templateWindowSize=3, searchWindowSize=5)
        bbox = ImageUtils.ImageDetectionUtil.getBoxPointsByMask(mask)

        x1, y1, x2, y2 = 0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT
        if bbox is not None:
            x1, y1, x2, y2 = bbox

        pos = Shapes.Rectangle.fromTwoCorners(x1, y1, x2, y2, margin=100)
        cut, offset = ImageUtils.ImageDetectionUtil.getSubImage(hsv, pos.position)
        if cut is not None and len(cut) != []:
            # print("fromList-------------------------------------------------")
            # print(offset)
            # print(bbox)
            # print(cut)
            mask = ImageUtils.ImageDetectionUtil.getMaskByLimits(cut, lowerLimit, upperLimit)

            ImageUtils.ImageDetectionUtil.helperShow(mask, 'Limits')

            kp = ImageUtils.ImageDetectionUtil.getKeyPointsByMask(mask, sift)
            return PointCloud.fromKeypoints(kp, count, offset=offset, scale=1/scale)
        return None


    @staticmethod
    def fromKeypoints(keypoints, count=5, offset=[0, 0], scale=1.0):
        nparray = np.empty((len(keypoints), 2), np.float32) # creates empty 2d numpy array

        xOffset = offset[0]
        yOffset = offset[1]

        for i in range(len(keypoints)):
            x = np.float32(int(keypoints[i].pt[0] * scale) + xOffset)
            y = np.float32(int(keypoints[i].pt[1] * scale) + yOffset)
            nparray[i] = (x, y)

        return PointCloud(nparray, count, keypoints=keypoints)

    def __init__(self, points, count=5, keypoints=None):
        self.points = points
        self.centers = None
        self.labels = None
        self.compactness = 0
        self.keypoints = keypoints
        if len(self.points) > Constants.KM_GROUP_COUNT * 2:
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
    def fromImage(img, sift, color=None, count=5):
        selfkeypoints = None
        keypoints = ImageUtils.ImageDetectionUtil.getKeyPoints(img, sift,  color)
        if keypoints is not None:
            return PointCloud.fromKeypoints(keypoints, Constants.KM_GROUP_COUNT)
        return None





