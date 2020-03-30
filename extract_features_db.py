#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from extract_gps import *
from opencv_serializer import *
import extractor_and_matcher
import pickle

data = list()

data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b1")
# data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b2")
# data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b3")
# data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b4")
# data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b5")


def main():

    # TODO: tak folder path as parameter

    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))

    extractor = extractor_and_matcher.FeatureExtractor()

    for folder in data:
        for img in os.listdir(folder):
            # Check if file has extension .jpg
            if not img.endswith('.jpg'):
                continue

            path = str(f'{folder}\{img}')

            try:
                tmp_img = cv2.imread(path, cv2.COLOR_BGR2GRAY)
                tmp_kp, tmp_des = extractor.extract_sift(tmp_img)
            except:
                print("Something went wrong with:" + img)
                continue

            #############
            # KEYPOINTS #
            #############
            tmp_kp_dict = list()

            for kp in tmp_kp:
                tmp_kp_dict.append(CVSerializer.cv_keypoint_to_dict(kp))

            with open(str(folder+'\\'+img[:-4]+'_keypoints.txt'), 'wb+') as file:
                pickle.dump(tmp_kp_dict, file, protocol=pickle.HIGHEST_PROTOCOL)

                print("KP : Ok")

                file.close()

            ###############
            # DESCRIPTORS #
            ###############

            with open(str(folder+'\\'+img[:-4]+'_descriptor.txt'), 'wb+') as file:
                pickle.dump(tmp_des, file, protocol=pickle.HIGHEST_PROTOCOL)

                print("DES: Ok")

                file.close()

if __name__ == "__main__":
    main()
