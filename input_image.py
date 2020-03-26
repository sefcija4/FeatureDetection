#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
# my imports
import extract_gps as gps


class Image(str):

    path = None
    img = None
    state = None  # v jaké fázi se img nachází preprocessing, feature_extraction, matching, ...
    location = tuple()  # tuple (latitude, longtitude) in degrees
    features = None

    def __init__(self, path):
        """
        Load image
        :param path: path to input image (from users camera)
        """
        self.path = path

        self.load_location()

        self.img = cv2.imread(path, cv2.IMREAD_COLOR)
        # get GPS
        # load img? maybe later

    def load_location(self):
        """
        Load latitude and longtitude from image metadata (exif format)
        -
        location (tuple) - (latitude, longtitude) in degrees
        """
        meta_data = gps.ImageMetaData(self.path)
        self.location = meta_data.get_lat_lng()
        # print(self.location)

    def preprocess(self):
        """
        Convert image to grayscale than equalize it's histogram.
        """
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.img = cv2.equalizeHist(self.img)
        # resize, ekvalization of histogram

    def resize(self):
        pass

    def extract_features(self):
        pass

    def show(self):
        cv2.imshow('Input img', self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

