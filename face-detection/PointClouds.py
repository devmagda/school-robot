import cv2
import matplotlib.pyplot as plt
import numpy as np

import Constants
import ImageUtils
import Shapes


class PointCloud:

    @staticmethod
    def fromLimits(hsv, sift, lowerLimit, upperLimit, count=5, scale=1.0, color=Constants.COLOR_PINK):
        # print("hsv______________")
        # print(hsv)
        hsv = ImageUtils.ImageUtils.scaleImage(hsv, scale=scale)
        mask = ImageUtils.ImageUtils.getMaskByLimits(hsv, lowerLimit, upperLimit)
        mask = cv2.fastNlMeansDenoising(mask, None, h=20, templateWindowSize=3, searchWindowSize=5)
        bbox = ImageUtils.ImageUtils.getBoxPointsByMask(mask)

        x1, y1, x2, y2 = 0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT
        if bbox is not None:
            x1, y1, x2, y2 = bbox
        # print(str(x1), str(y1), str(x2), str(y2), " == ")
        pos = Shapes.Rectangle.fromTwoCorners(x1, y1, x2, y2, margin=0, color=Constants.COLOR_GREEN)
        cut, offset = ImageUtils.ImageUtils.getSubImageRect(hsv, pos.position)
        if cut is not None and len(cut) != []:
            # print("fromList-------------------------------------------------")
            # print(offset)
            # print(bbox)
            # print(cut)
            mask = ImageUtils.ImageUtils.getMaskByLimits(cut, lowerLimit, upperLimit)

            ImageUtils.ImageUtils.helperShow(mask, 'Limits')

            kp = ImageUtils.ImageUtils.getKeyPointsByMask(mask, sift)
            return PointCloud.fromKeypoints(kp, count, offset=offset, scale=1 / scale, color=color)
        return None

    @staticmethod
    def fromKeypoints(keypoints, count=5, offset=[0, 0], scale=1.0, color=Constants.COLOR_PINK):
        nparray = np.empty((len(keypoints), 2), np.float32)  # creates empty 2d numpy array

        xOffset = offset[0]
        yOffset = offset[1]

        for i in range(len(keypoints)):
            x = np.float32(int(keypoints[i].pt[0] * scale) + xOffset)
            y = np.float32(int(keypoints[i].pt[1] * scale) + yOffset)
            nparray[i] = (x, y)

        return PointCloud(nparray, count, keypoints=keypoints, color=color)

    def __init__(self, points, count=5, keypoints=None, color=Constants.COLOR_PINK):
        self.points = points
        self.centers = None
        self.labels = None
        self.compactness = 0
        self.keypoints = keypoints
        self.color = color
        if len(self.points) > Constants.KM_GROUP_COUNT * 2:
            self.group(count)

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

    def getAsPositions(self, img=None):
        rects = []
        if self.centers is None:
            return rects
        if not len(self.centers) == 0:
            for c in self.centers:
                x, y = int(c[0]), int(c[1])
                rect = Shapes.Rectangle.fromCenter((x, y), color=self.color)
                if img is not None:
                    b, g, r = img[y, x]
                    color = (0, [int(r), int(g), int(b)], [int(b), int(g), int(r)])
                    rect.color = color
                rects.append(rect)
        return rects

    def get_as_xy_wh(self):
        output = []
        for c in self.centers:
            x, y = int(c[0]), int(c[1])
            output.append([x, y, 0, 0])
        return output

    @staticmethod
    def fromImage(img, sift, color=None, count=5):
        selfkeypoints = None
        keypoints = ImageUtils.ImageUtils.getKeyPoints(img, sift, color)
        if keypoints is not None:
            return PointCloud.fromKeypoints(keypoints, Constants.KM_GROUP_COUNT)
        return None
