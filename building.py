#!/usr/bin/env python
# -*- coding: utf-8 -*-

from input_image import *
from homography import *


class Building(object):
    """
    Building meta information
    """
    def __init__(self):
        self.id = None
        self.location = None
        self.name = None
        self.path = None

    def set_from_json(self, data):
        """
        Initialize object Building parameters from json file
        :param data: (dict)
        """
        self.id = data['id']
        self.location = GPSLocation(data['latitude'], data['longtitude'])
        self.name = data['name']
        self.path = data['path']

    def get_longtitude(self):
        return self.location.get_longtitude()

    def get_latitude(self):
        return self.location.get_latitude()

    def print(self):
        print("---------------------------")
        print(self.id)
        self.location.print()
        print(self.name)
        print(self.path)
        print("---------------------------")


class BuildingFeature(object):
    """
    Building for feature computation
    """

    def __init__(self, name, path, path_org):
        """
        :param name: name
        :param path: dataset image path
        :param path_org: path to original image, used to show result of transformation on whole image
        """
        self.id = name
        self.path = path
        self.original = path_org
        self.img = None
        self.keypoints = None
        self.descriptor = None
        self.matches = None

    def load_image(self, path):
        """
        Load image from path
        :param path:
        """
        self.img = cv2.imread(path)

    def set_keypoints(self, kp):
        self.keypoints = kp

    def set_descriptor(self, desc):
        self.descriptor = desc

    def update_matches(self, matches):
        self.matches = matches

    def get_num_of_matches(self):
        return len(self.matches)

    def get_sum_of_matches(self, count=10):
        """
        Sum distances of 10 best matches
        :param count: how many distances will be summed
        :return: sum of all distances
        """
        total_distance = 0
        self.sort_matches_by_distance()

        for m in self.matches[:count]:
            total_distance += m.distance

        return total_distance

    def sort_matches_by_distance(self):
        self.matches.sort(key=lambda x: x.distance)
