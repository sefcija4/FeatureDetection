#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class Visualization(object):
    """
    Class just for visualization methods
    This class has no use in future app development
    """

    @staticmethod
    def create_mask(img):
        """
        Create mask from cropped image (from database)
        :param img: image
        :return: mask - binary 2D image
        """
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        _, mask_bool = cv2.threshold(img, 1, 255, cv2.THRESH_BINARY)

        # Morphology
        kernel_open = np.ones((3, 3), np.uint8)
        kernel_close = np.ones((2, 2), np.uint8)
        mask_bool = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel_open)
        mask_bool = cv2.morphologyEx(mask_bool, cv2.MORPH_CLOSE, kernel_close)

        _, mask_bool = cv2.threshold(mask_bool, 1, 255, cv2.THRESH_BINARY)

        return mask_bool

    @staticmethod
    def merge_images(path1, path2):
        pass

    def warp_original_image(self):
        # warp + merge originálního obrázku, tak aby byla vidět transformace z původního
        pass

    @staticmethod
    def merge_images(img1, path2, homography):
        """
        Merge two images using binary masks
        :param img1: (img) background grayscale image
        :param path2: path to foreground image
        :param homography: (Homography)
        :return: merged image
        -
        Images must have same dimension (img.shape)
        """
        # Load images
        img2 = cv2.imread(path2)
        #
        fg = homography.warp_image(img1, img2.copy())  # Warped Foreground image
        bg = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)  # Background image

        # Mask
        fg_mask = Visualization.create_mask(fg)
        bg_mask = cv2.bitwise_not(fg_mask)

        bg = cv2.bitwise_or(bg, bg, mask=bg_mask[:, :, 0])
        fg = cv2.bitwise_or(fg, fg, mask=fg_mask[:, :, 0])

        return cv2.bitwise_or(fg, bg)
