#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2


class FeatureExtractor(object):

    @staticmethod
    def extract_sift(img):
        """
        Detect and compute SIFT features
        :param img: grayscale image
        :return: (cv2.KeyPoint, list) keypoints, feature vector
        """
        sift = cv2.xfeatures2d.SIFT_create()
        keypoint, descriptor = sift.detectAndCompute(img, None)
        return keypoint, descriptor
