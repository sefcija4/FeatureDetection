#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import os
from pathlib import Path
from config_handler import *

"""
Script for generating metadata json
-
id         - db id (str)
name       - name of the building (str)
path       - relative path to building's folder (str)
latitude   - latitude in degrees (float)
longtitude - longtitude in degrees (float)
"""

data_b = dict()
data_b['buildings'] = []

config = Config('config.json')

# Dům u kamenného zvonu
data_b['buildings'].append({
    'id': '0',
    'name': 'Dům u kamenného zvonu',
    'path': str(Path(f'{config.get_folder_name()}/b1')),
    'latitude':   50.0877694,
    'longtitude': 14.4196813
})

data_b['buildings'].append({
    'id': '1',
    'name': 'Dům - Hard rock cafe',
    'path': str(Path(f'{config.get_folder_name()}/b2')),
    'latitude':   50.0923047,
    'longtitude': 14.408226
})

data_b['buildings'].append({
    'id': '2',
    'name': 'U Zlaté konvice',
    'path': str(Path(f'{config.get_folder_name()}/b3')),
    'latitude':   50.0864621,
    'longtitude': 14.4185757
})

data_b['buildings'].append({
    'id': '3',
    'name': 'Štorchův dům, U Kamenné panny Marie',
    'path': str(Path(f'{config.get_folder_name()}/b4')),
    'latitude':   50.087185,
    'longtitude': 14.4198699
})

data_b['buildings'].append({
    'id': '4',
    'name': 'Pražská městská pojišťovna',
    'path': str(Path(f'{config.get_folder_name()}/b5')),
    'latitude':   50.087677,
    'longtitude': 14.4213159
})

data_b['buildings'].append({
    'id': '6',
    'name': 'Liberec - Zelený domek',
    'path': str(Path(f'{config.get_folder_name()}/b7')),
    'latitude':   50.7608511,
    'longtitude': 15.0634765
})

data_b['buildings'].append({
    'id': '7',
    'name': 'Liberec - Radnice',
    'path': str(Path(f'{config.get_folder_name()}/b8')),
    'latitude':   50.7700012,
    'longtitude': 15.0562721
})

data_b['buildings'].append({
    'id': '8',
    'name': 'Liberec - CAFE Kristián',
    'path': str(Path(f'{config.get_folder_name()}/b9')),
    'latitude':   50.7779843,
    'longtitude': 15.07934
})

data_b['buildings'].append({
    'id': '9',
    'name': 'Chrastava - Radnice',
    'path': str(Path(f'{config.get_folder_name()}/b10')),
    'latitude':   50.8169181,
    'longtitude': 14.969265
})

data_b['buildings'].append({
    'id': '10',
    'name': 'Chrastava - Hnědý dům',
    'path': str(Path(f'{config.get_folder_name()}/b11')),
    'latitude':   50.8162457,
    'longtitude': 14.9672913
})

data_b['buildings'].append({
    'id': '11',
    'name': 'Chrastava - Podstávkový dům',
    'path': str(Path(f'{config.get_folder_name()}/b12')),
    'latitude':   50.8183335,
    'longtitude': 14.9667979
})

with open(config.get_metadata(), 'w+') as file:
    json.dump(data_b, file)
