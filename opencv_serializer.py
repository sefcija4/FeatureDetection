#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2


class CVSerializer(object):
    """
    Preparation of openCV object for serialization
    """

    def __init__(self):
        pass

    @staticmethod
    def cv_keypoint_to_dict(kp):
        """
        Create dictionary from cv2.Keypoint object
        :param kp: (cv2.Keypoint) keypoint
        :return: (dict) keypoint
        """
        tmp = {
            'point': kp.pt,
            'size': kp.size,
            'angle': kp.angle,
            'response': kp.response,
            'octave': kp.octave,
            'id': kp.class_id
        }
        return tmp

    @staticmethod
    def dict_to_cv_keypoint(kp):
        """
        Create cv2.Keypoint object from dictionary
        :param kp: (dict) keypoint
        :return: (cv2.Keypoint) keypoint
        """
        tmp = cv2.KeyPoint(x=kp['point'][0], y=kp['point'][1], _size=kp['size'], _angle=kp['angle'],
                           _response=kp['response'], _octave=kp['octave'], _class_id=kp['id'])
        return tmp
