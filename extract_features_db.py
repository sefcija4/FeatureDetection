#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from config_handler import *
from opencv_serializer import *
import extractor
import pickle
import building_repository

"""
Script for pre-compute features for dataset images
"""


def main():
    config = Config('config.json')
    ex = extractor.FeatureExtractor()
    dir_name = Path(__file__).parent.absolute()
    metadata_path = Path(f'{dir_name}/{config.get_metadata()}')

    data = list()  # list for buildings folders

    buildings = building_repository.BuildingRepository.get_all_buildings(metadata_path)

    # load buildings folder paths
    for b in buildings:
        data.append(b.path)

    for folder in data:
        for img in os.listdir(Path(f'{dir_name}/{folder}')):
            # Check if file in building's folder has extension .jpg
            if not img.endswith('.jpg'):
                continue

            path = str(Path(f'{dir_name}/{folder}/{img}'))

            print(path)

            # CLAHE
            clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8))

            try:
                tmp_img = cv2.imread(path)
                tmp_img = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2GRAY)
                # tmp_img = cv2.equalizeHist(tmp_img)
                tmp_img = clahe.apply(tmp_img)

                tmp_kp, tmp_des = ex.extract_sift(tmp_img)
            except:
                print("Something went wrong with:" + img)
                continue

            # KEYPOINTS
            tmp_kp_dict = list()

            for kp in tmp_kp:
                tmp_kp_dict.append(CVSerializer.cv_keypoint_to_dict(kp))

            with open(Path(f'{dir_name}/{folder}/{img[:-4]}_keypoints.txt'), 'wb+') as file:
                pickle.dump(tmp_kp_dict, file, protocol=pickle.HIGHEST_PROTOCOL)

                file.close()

            # DESCRIPTORS
            with open(Path(f'{dir_name}/{folder}/{img[:-4]}_descriptor.txt'), 'wb+') as file:
                pickle.dump(tmp_des, file, protocol=pickle.HIGHEST_PROTOCOL)

                file.close()


if __name__ == "__main__":
    main()
