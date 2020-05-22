#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

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

    # PATH TO FOLDER WITH BUILDINGS
    data['buildings'].append({
        'path': 'data'
    })

    # INPUT IMAGE
    data['input_img'].append({
        'path': 'data\\_p\\test.jpg'
        # 'path': 'data\\_p\\test_b_4.jpg'
        # 'path': 'data\\_p\\test_b_5.jpg'
        # 'path': 'data\\_p\\test_b_7.jpg'
        # 'path': 'data\\_p\\test_b_8.jpg'
        # 'path': 'data\\_p\\test_b_8_2.jpg'
        # 'path': 'data\\_p\\test_b_9.jpg'
        # 'path': 'data\\_p\\test_b_10_1.jpg'
        # 'path': 'data\\_p\\test_b_11_1.jpg'
        # 'path': 'data\\_p\\test_b_12.jpg'
    })

    # GPS
    data['gps'].append({
        'radius': '0.0250'
    })

    # MATCHING
    data['flann_matching'].append({
        'pixel_distance': '100',
        'min_number_of_matches': '10',
        'flann_index': '1',
        'flann_trees': '5',
        'flann_checks': '100'
    })

    with open(path, 'w+') as file:
        json.dump(data, file)


if __name__ == "__main__":
    main()
