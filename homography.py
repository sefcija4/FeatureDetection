#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from scipy.spatial import distance as dist


class Homography(object):

    def __init__(self):
        self.H = None
        self.keypoints1 = list()
        self.keypoints2 = list()

    def add_keypoints(self, kp1, kp2):
        self.keypoints1 = kp1
        self.keypoints2 = kp2

    @staticmethod
    def order_points(pts):
        # sort the points based on their x-coordinates
        xSorted = pts[np.argsort(pts[:, 0]), :]
        # grab the left-most and right-most points from the sorted
        # x-roodinate points
        leftMost = xSorted[:2, :]
        rightMost = xSorted[2:, :]
        # now, sort the left-most coordinates according to their
        # y-coordinates so we can grab the top-left and bottom-left
        # points, respectively
        leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
        (tl, bl) = leftMost
        # now that we have the top-left coordinate, use it as an
        # anchor to calculate the Euclidean distance between the
        # top-left and right-most points; by the Pythagorean
        # theorem, the point with the largest distance will be
        # our bottom-right point
        D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
        (br, tr) = rightMost[np.argsort(D)[::-1], :]
        # return the coordinates in top-left, top-right,
        # bottom-right, and bottom-left order
        return np.array([tl, tr, br, bl], dtype="float32")

    def sort_points(self):

        kp1 = np.asanyarray(self.keypoints1)
        kp2 = np.asanyarray(self.keypoints2)

        # print("KP1:", kp1)
        # print("KP2:", kp2)

        '''print("KP1:", kp1)

        # sorted(kp1, key=self.clockwiseangle_and_distance)
        # sorted(kp2, key=self.clockwiseangle_and_distance)

        rect1 = np.zeros((4, 2))
        rect2 = np.zeros((4, 2))

        print("-------------------")
        print(kp1)
        print(kp2)
        print("-------------------")

        s1 = kp1.sum(axis=1)
        diff1 = np.diff(kp1, axis=1)
        rect1[0] = kp1[np.argmin(s1)]
        rect1[3] = kp1[np.argmax(s1)]
        rect1[1] = kp1[np.argmin(diff1)]
        rect1[2] = kp1[np.argmax(diff1)]

        s2 = kp2.sum(axis=1)
        diff2 = np.diff(kp2, axis=1)
        rect2[0] = kp2[np.argmin(s2)]
        rect2[3] = kp2[np.argmax(s2)]
        rect2[1] = kp2[np.argmin(diff2)]
        rect2[2] = kp2[np.argmax(diff2)]

        print("-------------------")
        print(rect1)
        print(rect2)
        print("-------------------")

        self.keypoints1 = [(rect1[0][0], rect1[0][1]), (rect1[1][0], rect1[1][1]),
                           (rect1[2][0], rect1[2][1]), (rect1[3][0], rect1[3][1])]
        self.keypoints2 = [(rect2[0][0], rect2[0][1]), (rect2[1][0], rect2[1][1]),
                           (rect2[2][0], rect2[2][1]), (rect2[3][0], rect2[3][1])]

        print("-------------------")
        print(self.keypoints1)
        print(self.keypoints2)
        print("-------------------")'''

        kp1 = self.order_points(kp1)
        kp2 = self.order_points(kp2)

        # self.keypoints1 = [(kp1[3][0], kp1[3][1]), (kp1[2][0], kp1[2][1]), (kp1[1][0], kp1[1][1]), (kp1[0][0], kp1[0][1])]
        # self.keypoints2 = [(kp2[3][0], kp2[3][1]), (kp2[2][0], kp2[2][1]), (kp2[1][0], kp2[1][1]), (kp2[0][0], kp2[0][1])]

        # self.keypoints1 = [(139.41652, 333.90176), (162.03053, 520.54266), (193.66374, 474.945), (117.28797, 332.34634)]
        # self.keypoints2 = [(115.96728, 197.7768), (194.0934, 423.02094), (225.09505, 364.2162), (140.33514, 195.30168)]

        # print("KP1::", self.keypoints1)
        # print("KP2::", self.keypoints2)

        # https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/?fbclid=IwAR0ZLhmnMZehc2gCZsRq5ESM6_LPheqlIOEp4mM2uFKLfXiYEMpqfhRvQzg

    def find_matrix(self, matches, kp1, kp2):

        for m in matches[:4]:
            # Get the matching keypoints for each of the images
            img1_idx = m.queryIdx
            img2_idx = m.trainIdx

            # x - columns
            # y - rows
            # Get the coordinates
            (x1, y1) = kp1[img1_idx].pt
            (x2, y2) = kp2[img2_idx].pt

            # print(x1, y1)
            # print(x2, y2)

            # Append to each list
            self.keypoints1.append((x1, y1))
            self.keypoints2.append((x2, y2))

        # print("")
        # print(self.keypoints1)
        # print(self.keypoints2)

        # print("SORT")

        # self.sort_points()

        self.H, mask = cv2.findHomography(np.array(self.keypoints2), np.array(self.keypoints1))

    def warp_image(self, img1, img2):
        print(img1.shape, img2.shape)
        return cv2.warpPerspective(img2, self.H, dsize=(img1.shape[1], img1.shape[0]))

    @staticmethod
    def merge_images(img1, img2):
        return cv2.addWeighted(img1.copy(), 1, img2, 1, 0, img1.copy())
