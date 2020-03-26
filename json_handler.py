#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from input_image import *


class Building(dict):

    data = dict()

    def __init__(self, data):
        self.data = data

    def extract_features(self):
        pass


class App(str):

    img_in = None
    buildings = list()
    matches = None

    sift = None
    orb = None
    surf = None

    def __init__(self, path):
        with open(path) as file:
            data = json.load(file)

        for x in data:
            for y in data[x]:
                self.buildings.append(Building(y))

    def check_perimeter(self):
        # are any buildings nearby?
        pass

    def compare_features(self):
        # feature matching
        pass

    def print_buildings(self):
        for x in self.buildings:
            print(x.data['name'])


app = App('data.txt')
app.print_buildings()

img = Image('C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\_p\\IMG_3481.jpg')
img.preprocess()
img.show()
