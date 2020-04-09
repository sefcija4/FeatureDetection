#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
# my imports
import extract_gps as gps
from extractor_and_matcher import *


class GPSLocation(object):
    """
    GPS location data

    Parameters:
    :param self.latitude (float)
    :param self.longtitude (float)
    """
    def __init__(self, lat, lng):
        self.latitude = float(lat)
        self.longtitude = float(lng)

    def get_latitude(self):
        return self.latitude

    def get_longtitude(self):
        return self.longtitude

    @staticmethod
    def check_if_belongs(input_img, db_building):
        """
        Check if building (latitude, longtitude) belongs in perimeter of input image
        :param input_img: (object) Image
        :param db_building: (object) Building
        :return: (boolean)
        """
        radius = 0.002  # in degrees
        # (x - center_x)^2 + (y - center_y)^2 < radius^2

        if (pow(db_building.get_longtitude() - input_img.get_longtitude(), 2) +
            pow(db_building.get_latitude() - input_img.get_latitude(), 2)) <= (radius**2):

            return True
        else:
            return False

    def print(self):
        print((self.latitude, self.longtitude))


class Image(object):

    def __init__(self, path):
        """
        Load image
        :param path: path to input image (from users camera)
        """

        self.path = path

        self.img = cv2.imread(self.path)
        self.location = self.load_location()  # tuple (latitude, longtitude) in degrees

        # self.img = cv2.imread(path, cv2.IMREAD_COLOR)
        # get GPS
        # load img? maybe later

        self.keypoints = None
        self.descriptor = None

    def get_descriptor(self):
        return self.descriptor

    def load_location(self):
        """
        Load latitude and longtitude from image metadata (exif format)
        -
        location (tuple) - (latitude, longtitude) in degrees
        """
        meta_data = gps.ImageMetaData(self.path)
        coords = meta_data.get_lat_lng()
        location = GPSLocation(coords[0], coords[1])
        # print(self.location)
        return location

    def get_longtitude(self):
        return self.location.get_longtitude()

    def get_latitude(self):
        return self.location.get_latitude()

    def preprocess(self):
        """
        Convert image to grayscale than equalize it's histogram.
        """
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.img = cv2.equalizeHist(self.img)
        self.resize()
        # resize, ekvalization of histogram

    def resize(self):
        """
        Resize image
        # TODO: relative scale?
        :return:
        """
        (h, w) = self.img.shape[:2]
        width = 960
        r = width / float(w)
        dim = (width, int(h * r))
        self.img = cv2.resize(self.img, dim)

    def extract_features(self):
        """
        Extract features, save keypoints and descriptors
        :return:
        """
        self.keypoints, self.descriptor = FeatureExtractor.extract_sift(self.img)
        print("IMG fearues extracted")

    def merge_image(self, img):
        return cv2.addWeighted(self.img.copy(), 1, img, 1, 0, self.img.copy())

    def show(self):
        cv2.imshow('Input img', self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def print(self):
        print("----  IMG  ----")
        print(self.path)
        self.location.print()
