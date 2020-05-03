#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class Homography(object):

    def __init__(self):
        self.H = None
        self.keypoints1 = list()
        self.keypoints2 = list()

    def add_keypoints(self, kp1, kp2):
        """
        Set keypoints
        :param kp1: (list)
        :param kp2: (list)
        """
        self.keypoints1 = kp1
        self.keypoints2 = kp2

    def find_matrix(self, matches, kp1, kp2):
        """
        Calculate homography matrix
        :param matches:
        :param kp1: (list) keypoints from first image
        :param kp2: (list) keypoints from second image
        """
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

        self.H, mask = cv2.findHomography(np.array(self.keypoints2), np.array(self.keypoints1))

    def warp_image(self, img1, img2):
        """
        Warp image2 using homography matrix to
        :param img1: image1
        :param img2: image2
        :return: Warped image2
        """
        # print(img1.shape, img2.shape)
        return cv2.warpPerspective(img2, self.H, dsize=(img1.shape[1], img1.shape[0]))

    @staticmethod
    def merge_images(img1, img2):
        """
        Merge two images together
        :param img1: image1
        :param img2: image2
        :return: merged image
        -
        Images must be same size  #TODO: Check if they are same size
        """
        return cv2.addWeighted(img1.copy(), 0.5, img2, 0.5, 0, img1.copy())


class Visualization(object):
    """
    Class just for visualization methods
    This class has no use in future app development
    """

    @staticmethod
    def create_mask(img):
        _, mask_bool = cv2.threshold(img, 1, 255, cv2.THRESH_BINARY)

        # Morphology
        kernel = np.ones((5, 5), np.uint8)
        mask_bool = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

        _, mask_bool = cv2.threshold(mask_bool, 1, 255, cv2.THRESH_BINARY)

        return mask_bool

    @staticmethod
    def make_img_rgba(img, mask):
        pass

    @staticmethod
    def merge_images_red(path1, path2):
        pass

    def warp_original_image(self):
        # warp + merge originálního obrázku, tak aby byla vidět transformace z původního
        pass

    def merge_images_cropped(self):
        # "dokonale" oříznuté obrázky
        pass
