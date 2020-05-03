#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

"""
Script for generating json config file
"""

data = dict()
data['metadata'] = []
data['input_img'] = []
data['gps'] = []
data['flann_matching'] = []

PATH = 'config.json'

# METADATA
data['metadata'].append({
    'metadata_path': 'data.json'
})

# INPUT IMAGE
data['input_img'].append({
    'path': 'data\\_p\\test.jpg'
})

# GPS
data['gps'].append({
    'radius': '0.003'
})

# MATCHING
data['flann_matching'].append({
    'pixel_distance': '100',
    'min_number_of_matches': '10',
    'flann_index': '1',
    'flann_trees': '5',
    'flann_checks': '100'
})

with open(PATH, 'w+') as file:
    json.dump(data, file)
