#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

data = {}
data['buildings'] = []

# Dům u kameného zvonu
data['buildings'].append({
    'id': '0',
    'name': 'Dům u kameného zvonu',
    'path': 'C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b1',
    'latitude':   '50.0877694',
    'longtitude': '14.4196813,',
    'features': 'None'
})

data['buildings'].append({
    'id': '1',
    'name': 'Dům - Hard rock cafe',
    'path': 'C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b2',
    'latitude':   '50.0923047',
    'longtitude': '14.408226,',
    'features': 'None'
})

with open('data.txt', 'w') as file:
    json.dump(data, file)