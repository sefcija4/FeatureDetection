#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pathlib import Path

"""
Script for generating json config file
"""


def main():

    data = dict()
    data['metadata'] = []
    data['buildings'] = []
    data['input_img'] = []
    data['gps'] = []
    data['flann_matching'] = []

    path = 'config.json'

    # METADATA
    data['metadata'].append({
        'metadata_path': 'data.json'
    })

    # PATH TO FOLDER WITH BUILDINGS FOLDERS
    data['buildings'].append({
        'path': 'data'
    })

    # INPUT IMAGE
    data['input_img'].append({
        'path': str(Path('data/_p/test.jpg'))
        # 'path': str(os.path.join('data', '_p', 'test_b_4.jpg'))  # fail
        # 'path': str(os.path.join('data', '_p', 'test_b_5.jpg'))
        # 'path': str(os.path.join('data', '_p', 'test_b_7.jpg'))
        # 'path': str(os.path.join('data', '_p', 'test_b_8.jpg'))
        # 'path': str(os.path.join('data', '_p', 'test_b_9.jpg'))  # fail
        # 'path': str(os.path.join('data', '_p', 'test_b_10_1.jpg'))
        # 'path': str(os.path.join('data', '_p', 'test_b_11_1.jpg'))
        # 'path': str(os.path.join('data', '_p', 'test_b_12.jpg'))
    })

    # GPS
    data['gps'].append({
        'radius': '0.0025'
    })

    # MATCHING
    data['flann_matching'].append({
        'pixel_distance': '100',
        'min_number_of_matches': '10',
        'flann_index': '1',
        'flann_trees': '5',
        'flann_checks': '10'
    })

    with open(path, 'w+') as file:
        json.dump(data, file)


if __name__ == "__main__":
    main()
