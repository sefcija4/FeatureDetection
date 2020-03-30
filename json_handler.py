#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import pickle

from opencv_serializer import *
from input_image import *
from extractor_and_matcher import *

data = list()

data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b1")
# data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b2")
# data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b3")
# data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b4")
# data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b5")


class Building(object):

    def __init__(self):
        self.id = None
        self.location = None
        self.name = None
        self.path = None

    def set_from_json(self, data):
        self.id = data['id']
        self.location = GPSLocation(data['latitude'], data['longtitude'])
        self.name = data['name']
        self.path = data['path']

        return None

    def print(self):
        print("---------------------------")
        print(self.id)
        self.location.print()
        print(self.name)
        print(self.path)


class BuildingFeature(object):

    def __init__(self, name, path):
        self.id = name
        self.path = path
        self.img = None
        self.keypoints = None
        self.descriptor = None
        self.matches = None

    def set_from_dict_file(self, data):
        # TODO: load kp a desc using BuildingRepository
        pass

    def load_image(self, path):
        self.img = cv2.imread(path)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

    def set_keypoints(self, kp):
        self.keypoints = kp

    def set_descriptor(self, desc):
        self.descriptor = desc


class BuildingRepository(object):

    @staticmethod
    def get_all_buildings(path):
        # loads metadata
        # returns dict with metadata

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
        Load keypoints and descriptors from to file and return them.
        :param folder: (str) folder in db of specific building
        :return: (object) list of BuildingFeatures (objects)
        """
        # return features for building

        buildings = list()

        for img in os.listdir(folder):

            if img.endswith('.txt'):
                continue

            tmp_b = BuildingFeature(img[:-4], str(f'{folder}\{img}'))
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


class App(str):

    def __init__(self, path):
        self.img_in = None
        self.db_path = path
        self.buildings = list()
        self.buildings_features = dict()
        self.matcher = None
        self.matches = None

        self.sift = None
        self.orb = None
        self.surf = None

    def load_buildings(self):
        # load all buildings metadata

        self.buildings = BuildingRepository.get_all_buildings(self.db_path)

        for x in self.buildings:
            x.print()

    def load_features(self, building):
        # load keypoints and descriptor for specific building
        self.buildings_features[building.id] = BuildingRepository.get_building_features(building.path)

        print(f'Number of images: {len(self.buildings_features[building.id])}')

    def load_image(self, path):
        self.img_in = Image(path)

    def check_perimeter(self):
        # are any buildings nearby?
        pass

    def match_features(self):
        # Match features using Matcher.match_sift()

        # TODO: zatím match pro všechny domy, později je budu muset filtrovat podle lokace

        self.img_in.extract_features()

        self.matcher = Matcher()
        self.matcher.set_sift_match()

        self.matcher.match_sift(self.img_in.get_descriptor(), self.buildings_features)

        print("Done")

    def show_matches(self):
        self.matcher.show_matches(self.img_in, self.buildings_features)

    def compare_features(self):
        # feature matching
        pass

    def print_buildings(self):
        for x in self.buildings:
            print(x.data['name'])


app = App('data.txt')
app.load_buildings()

app.load_image('C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\_p\\test.jpg')
app.img_in.preprocess()
app.img_in.print()

# app.img_in.show()

app.load_features(app.buildings[0])  # take first building 0-ID

app.match_features()

app.show_matches()

# img.show()
