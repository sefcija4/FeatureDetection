#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from config_handler import *
from opencv_serializer import *
import extractor
import pickle

data = list()

data.append("b1")
data.append("b2")
data.append("b3")
data.append("b4")
data.append("b5")
# data.append("b6")
data.append("b7")
data.append("b8")
data.append("b9")

"""
Script for pre-compute features for dataset images
"""


def main():
    config = Config('config.json')
    ex = extractor.FeatureExtractor()
    dir_name = os.path.dirname(__file__)

    for folder in data:
        for img in os.listdir(os.path.join(dir_name, config.get_folder_name(), folder)):
            # Check if file has extension .jpg
            if not img.endswith('.jpg'):
                continue

            path = os.path.join(dir_name, config.get_folder_name(), folder, img)

            print(path)

            # CLAHE
            clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8))

            try:
                tmp_img = cv2.imread(path)
                tmp_img = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2GRAY)
                tmp_img = clahe.apply(tmp_img)

                tmp_kp, tmp_des = ex.extract_sift(tmp_img)
            except:
                print("Something went wrong with:" + img)
                continue

            # KEYPOINTS
            tmp_kp_dict = list()

            for kp in tmp_kp:
                tmp_kp_dict.append(CVSerializer.cv_keypoint_to_dict(kp))

            with open(os.path.join(dir_name, config.get_folder_name(), folder, str(f'{img[:-4]}_keypoints.txt')),
                      'wb+') as file:
                pickle.dump(tmp_kp_dict, file, protocol=pickle.HIGHEST_PROTOCOL)

                # print("KP : Ok")
                file.close()

            # DESCRIPTORS
            with open(os.path.join(dir_name, config.get_folder_name(), folder,str(f'{img[:-4]}_descriptor.txt')),
                      'wb+') as file:
                pickle.dump(tmp_des, file, protocol=pickle.HIGHEST_PROTOCOL)

                # print("DES: Ok")
                file.close()


if __name__ == "__main__":
    main()
