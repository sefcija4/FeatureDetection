#!/usr/bin/env python
# -*- coding: utf-8 -*-

import extract_gps as gps
from extractor import *


class GPSLocation(object):
    """
    GPS location data

    Parameters:
    :param self.latitude (float)
    :param self.longtitude (float)
    """
    def __init__(self, lat, lng):
        self.latitude = float(lat)
        self.longtitude = float(lng)

    def get_latitude(self):
        return self.latitude

    def get_longtitude(self):
        return self.longtitude

    @staticmethod
    def check_if_belongs(input_img, db_building):
        """
        Check if building (latitude, longtitude) belongs in perimeter of input image
        :param input_img: (object) Image
        :param db_building: (object) Building
        :return: (boolean)
        """
        radius = 0.003  # in degrees -> 200m
        # (x - center_x)^2 + (y - center_y)^2 < radius^2

        if (pow(db_building.get_longtitude() - input_img.get_longtitude(), 2) + pow(db_building.get_latitude()
                                                                                    - input_img.get_latitude(), 2)) <= (radius**2):

            return True
        else:
            return False

    def print(self):
        print((self.latitude, self.longtitude))
