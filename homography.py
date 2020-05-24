#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class Homography(object):
    """
    Matrix for affine transformation, image warp perspective
    """

    def __init__(self):
        self.H = None  # Homography (transform) matrix
        self.keypoints1 = list()  # Coordinates of keypoints1
        self.keypoints2 = list()  # Coordinates of keypoints2

    def add_keypoints(self, kp1, kp2):
        """
        Set keypoints
        :param kp1: (list)
        :param kp2: (list)
        """
        self.keypoints1 = kp1
        self.keypoints2 = kp2

    def find_matrix(self, matches, kp1, kp2, ransac=False):
        """
        Calculate homography matrix
        :param matches:
        :param kp1: (list) keypoints from first image
        :param kp2: (list) keypoints from second image
        :param ransac (bool) while using RANSAC
        """
        if ransac:
            self.find_matrix_ransac(matches, kp1, kp2)
        else:
            for m in matches[:4]:
                # Get the matching keypoints for each of the images
                img1_idx = m.queryIdx
                img2_idx = m.trainIdx

                # x - columns, y - rows
                # Get the keypoint's coordinates
                (x1, y1) = kp1[img1_idx].pt
                (x2, y2) = kp2[img2_idx].pt

                # Append coordinates to each list
                self.keypoints1.append((x1, y1))
                self.keypoints2.append((x2, y2))

            self.H, mask = cv2.findHomography(np.array(self.keypoints2), np.array(self.keypoints1))

    def find_matrix_ransac(self, matches, kp1, kp2):
        """
        Ransac version of find_matrix()
        :param matches:
        :param kp1: (list) keypoints from first image
        :param kp2: (list) keypoints from second image
        """
        self.keypoints1 = np.zeros((len(matches), 2), dtype=np.float32)
        self.keypoints2 = np.zeros((len(matches), 2), dtype=np.float32)

        for i, m in enumerate(matches):
            self.keypoints1[i, :] = kp1[m.queryIdx].pt
            self.keypoints2[i, :] = kp2[m.trainIdx].pt

        self.H, mask = cv2.findHomography(self.keypoints2, self.keypoints1, cv2.RANSAC)

    def warp_image(self, img1, img2):
        """
        Warp image2 using homography matrix to
        :param img1: image1
        :param img2: image2
        :return: Warped image2
        """
        return cv2.warpPerspective(img2, self.H, dsize=(img1.shape[1], img1.shape[0]))
