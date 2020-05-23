#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gps_location import *


class Image(object):

    def __init__(self, path):
        """
        Load image
        :param path: path to input image (from users camera)
        """

        self.path = path

        self.img = cv2.imread(str(self.path))
        self.location = self.load_location()

        self.keypoints = None
        self.descriptor = None

    def get_descriptor(self):
        return self.descriptor

    def load_location(self):
        """
        Load latitude and longtitude from image metadata (exif format)
        -
        :return location (tuple) - (latitude, longtitude) in degrees
        """
        meta_data = gps.ImageMetaData(self.path)
        coords = meta_data.get_lat_lng()
        location = GPSLocation(coords[0], coords[1])
        return location

    def get_longtitude(self):
        return self.location.get_longtitude()

    def get_latitude(self):
        return self.location.get_latitude()

    def preprocess(self):
        """
        Convert image to grayscale than equalize it's histogram and resize
        """
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        # self.img = cv2.equalizeHist(self.img)

        # CLAHE
        clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8))
        self.img = clahe.apply(self.img)

        self.resize()

    def resize(self, max_dimension=960):
        """
        Resize image's larger dimension according to max_dimension value
        and second dimension is relatively resized
        """
        (h, w) = self.img.shape[:2]

        if h > w:
            height = max_dimension
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            width = max_dimension
            r = width / float(w)
            dim = (width, int(h * r))

        self.img = cv2.resize(self.img, dim)

    def extract_features(self):
        """
        Extract features, save keypoints and descriptors
        :return:
        """
        self.keypoints, self.descriptor = FeatureExtractor.extract_sift(self.img)
        print("Input image features have been extracted")

    def merge_image(self, img):
        """
        Merge image with other image
        :param img: image
        :return: merged image
        """
        return cv2.addWeighted(self.img.copy(), 1, img, 1, 0, self.img.copy())

    def show(self):
        """
        Show image in new window
        """
        cv2.imshow('Image', self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def print(self):
        print(self.path)
        self.location.print()
