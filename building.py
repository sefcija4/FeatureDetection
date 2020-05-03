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

    def print_id_name(self):
        print("---------------------------")
        print(self.id, self.name)


class BuildingFeature(object):
    """
    Building for feature computation
    """

    def __init__(self, name, path, path_org):
        self.id = name
        self.path = path
        self.original = path_org
        self.img = None
        self.keypoints = None
        self.descriptor = None
        self.matches = None

    def load_image(self, path):
        """
        Load image from path and convert it to grayscale
        :param path:
        """
        self.img = cv2.imread(path)
        # print(self.img.shape)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

    def set_keypoints(self, kp):
        self.keypoints = kp

    def set_descriptor(self, desc):
        self.descriptor = desc

    def update_matches(self, matches):
        self.matches = matches

    def get_num_of_matches(self):
        return len(self.matches)

    def get_sum_of_matches(self):
        """
        Sum distances of 10 best matches
        :return: sum of all distances
        """
        total_distance = 0

        self.sort_matches_by_distance()

        for m in self.matches[:10]:
            total_distance += m.distance

        return total_distance

    def sort_matches_by_distance(self):
        self.matches.sort(key=lambda x: x.distance)