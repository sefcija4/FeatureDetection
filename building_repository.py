#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import pickle

from building import *
from opencv_serializer import *


class BuildingRepository(object):
    """
    Loading building's data
    """

    @staticmethod
    def get_all_buildings(path):
        """
        Load building data (in json format) from file
        :param path: (string) path to json file
        :return: (object) Building
        """
        buildings = list()

        with open(path) as file:
            data = json.load(file)

            for x in data:
                for y in data[x]:
                    b = Building()
                    b.set_from_json(y)
                    buildings.append(b)
            file.close()

        return buildings

    @staticmethod
    def get_building_features(folder):
        """
        Load keypoints and descriptors from each image of building's file and return them.
        :param folder: (str) folder in db of specific building
        :return: (object) list of BuildingFeatures
        """
        buildings = list()

        for img in os.listdir(folder):

            if img.endswith('.txt'):
                continue

            tmp_b = BuildingFeature(img[:-4], str(f'{folder}\{img}'), str(f'{folder}_original\{img[:-4]}_small.jpg'))
            path = str(f'{folder}\{img[:-4]}')

            # KEYPOINTS
            kp_load = list()

            with open(str(f'{path}_keypoints.txt'), 'rb') as file:
                to_load = pickle.load(file, encoding='utf-8')

            for kp in to_load:
                kp_load.append(CVSerializer.dict_to_cv_keypoint(kp))

            # DESCRIPTOR
            with open(str(f'{path}_descriptor.txt'), 'rb') as file:
                desc_load = pickle.load(file, encoding='utf-8')

            tmp_b.set_keypoints(kp_load)
            tmp_b.set_descriptor(desc_load)

            buildings.append(tmp_b)

        return buildings
