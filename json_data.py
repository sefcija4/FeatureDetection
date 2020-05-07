#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config_handler import *

"""
Script for generating metadata json
-
id         - db id
name       - name of the building
path       - relative path to building's folder
latitude   - latitude in degrees
longtitude - longtitude in degrees
"""

data_b = dict()
data_b['buildings'] = []

config = Config('config.json')

# Dům u kamenného zvonu
data_b['buildings'].append({
    'id': '0',
    'name': 'Dům u kamenného zvonu',
    'path': 'data\\b1',
    'latitude':   '50.0877694',
    'longtitude': '14.4196813',
    'features': 'None'
})

data_b['buildings'].append({
    'id': '1',
    'name': 'Dům - Hard rock cafe',
    'path': 'data\\b2',
    'latitude':   '50.0923047',
    'longtitude': '14.408226',
    'features': 'None'
})

data_b['buildings'].append({
    'id': '2',
    'name': 'U Zlaté konvice',
    'path': 'data\\b3',
    'latitude':   '50.0864621',
    'longtitude': '14.4185757',
    'features': 'None'
})

data_b['buildings'].append({
    'id': '3',
    'name': 'Štorchův dům, U Kamenné panny Marie',
    'path': 'data\\b4',
    'latitude':   '50.087185',
    'longtitude': '14.4198699',
    'features': 'None'
})

data_b['buildings'].append({
    'id': '4',
    'name': 'Pražská městská pojišťovna',
    'path': 'data\\b5',
    'latitude':   '50.087677',
    'longtitude': '14.4213159',
    'features': 'None'
})

data_b['buildings'].append({
    'id': '6',
    'name': 'Liberec - Zelený domek',
    'path': 'data\\b7',
    'latitude':   '50.7608511',
    'longtitude': '15.0634765',
    'features': 'None'
})

data_b['buildings'].append({
    'id': '7',
    'name': 'Liberec - Radnice',
    'path': 'data\\b8',
    'latitude':   '50.7700012',
    'longtitude': '15.0562721',
    'features': 'None'
})

data_b['buildings'].append({
    'id': '8',
    'name': 'Liberec - CAFE Kristián',
    'path': 'data\\b9',
    'latitude':   '50.7779843',
    'longtitude': '15.07934',
    'features': 'None'
})

with open(config.get_metadata(), 'w') as file:
    json.dump(data_b, file)