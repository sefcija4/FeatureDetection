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
        self.keypoints1 = kp1
        self.keypoints2 = kp2

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

        self.H, mask = cv2.findHomography(np.array(self.keypoints2), np.array(self.keypoints1))

    def warp_image(self, img1, img2):
        # print(img1.shape, img2.shape)
        return cv2.warpPerspective(img2, self.H, dsize=(img1.shape[1], img1.shape[0]))

    @staticmethod
    def merge_images(img1, img2):
        return cv2.addWeighted(img1.copy(), 1, img2, 1, 0, img1.copy())


class Visualization(object):

    def __init__(self):
        pass

    def merge_images_red(self):
        # aby warpnutá budova byla v černobílém obrazu červená
        pass

    def warp_original_image(self):
        # warp + merge originálního obrázku, tak aby byla vidět transformace z původního
        pass

    def merge_images_cropped(self):
        # "dokonale" oříznuté obrázky
        pass
