#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


class Config(object):
    """
    Config class implements loading of data from json file
    """

    def __init__(self, path):

        self.path = path
        self.data = None

        self.load()

    def load(self):
        """
        Load json from self.path and set self.data
        """
        with open(self.path, 'r') as file:
            self.data = json.load(file)
            file.close()

    def get_metadata(self):
        """
        Get metadata from config file
        :return: (string) metadata
        """
        for p in self.data['metadata']:
            metadata = p['metadata_path']

        # print(metadata)
        return metadata

    def get_folder_name(self):
        """
        Get metadata from config file
        :return: (string) metadata
        """
        for p in self.data['buildings']:
            path = p['path']

        # print(metadata)
        return path

    def get_input_image(self):
        """
        Get path to input image from config file
        :return: (string) path to input image
        """
        for p in self.data['input_img']:
            path = p['path']

        # print(path)
        return path

    def get_gps_radius(self):
        """
        Get gps radius from config file
        :return: (float) radius
        """
        for p in self.data['gps']:
            radius = float(p['radius'])

        # print(radius)
        return radius

    def get_flann_matching_setup(self):
        """
        Get FLANN matching setup from config file
        :return: (dict) matching setup data
        -
        data['flann_index'] - index for flann algorithms
        data['flann_trees'] - number of trees
        data['flann_checks'] - maximal number of return in recursion
        """
        data = dict()

        for p in self.data['flann_matching']:
            data['flann_index'] = int(p['flann_index'])
            data['flann_trees'] = int(p['flann_trees'])
            data['flann_checks'] = int(p['flann_checks'])

        # print(data['pixel_distance'], data['min_number_of_matches'], data['flann_index'], data['flann_trees'],
        # data['flann_checks'])

        return data

    def get_filter_features(self):
        """
        Get thresholds for filter out bad features
        :return: (dict) thresholds
        -
        data['pixel_distance'] - minimal distance between keypoints (in pixels)
        data['min_number_of_matches'] - minimal number of matches to successful match (less then that won't be
                                        considered as possible match)
        """
        data = dict()

        for p in self.data['flann_matching']:
            data['pixel_distance'] = int(p['pixel_distance'])
            data['min_number_of_matches'] = int(p['min_number_of_matches'])

        return data
