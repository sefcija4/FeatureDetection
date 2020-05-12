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

    PATH = 'config.json'

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
        # 'path': 'data\\_p\\test.jpg'         # OK
        # 'path': 'data\\_p\\test_b_4.jpg'     # BAD example
        # 'path': 'data\\_p\\test_b_5.jpg'     # OK
        # 'path': 'data\\_p\\test_b_7.jpg'     # OK
        # 'path': 'data\\_p\\test_b_8.jpg'     # OK
        # 'path': 'data\\_p\\test_b_9.jpg'     # BAD example - hard shadows, signs
        # 'path': 'data\\_p\\test_b_10_1.jpg'    # OK
        # 'path': 'data\\_p\\test_b_10_2.jpg'  # Total miss
        'path': 'data\\_p\\test_b_11_1.jpg'  # OK - not perfect
        # 'path': 'data\\_p\\test_b_11_2.jpg'  # Keypoints are too close
        # 'path': 'data\\_p\\test_b_12.jpg'    # OK - not perfect
        # 'path': 'data\\_p\\IMG_3513.jpg'
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

    with open(PATH, 'w+') as file:
        json.dump(data, file)


if __name__ == "__main__":
    main()
