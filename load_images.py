#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
import operator
# My imports
import feature_detection
import extract_gps

THE_CHOSEN_ONE = "C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\_p\\IMG_3481.jpg"

# folder should contain only img files
FOLDER_PATH = "C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b1"

data = list()

data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b1")
data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b2")
data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b3")
data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b4")
data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b5")
# data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b6")
data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b7")

# result = []
list_keypoints1 = []
list_keypoints2 = []


def by_count(value):
    return value[0]


# take all images (all files and folders)
def compare_all_images_from_folder(result):
    for folder in data:
        for img in os.listdir(folder):
            path = str(f'{folder}\{img}')
            # print(path)
            result.append((feature_detection.compare_descriptors(THE_CHOSEN_ONE, path)))

    return result


def get_keypoints_coordinates(keypoints1, keypoints2, top_matches):
    for match in top_matches:  # take best img and its 4 best matches
        # print(match.distance)
        # Get the matching keypoints for each of the images
        img1_idx = match.queryIdx
        img2_idx = match.trainIdx

        # x - columns
        # y - rows
        # Get the coordinates
        (x1, y1) = keypoints1[img1_idx].pt
        (x2, y2) = keypoints2[img2_idx].pt

        # print(x1, y1)
        # print(x2, y2)

        list_keypoints1.append((x1, y1))
        list_keypoints2.append((x2, y2))


# feature_detection.results.sort(reverse=True)
# for item in feature_detection.results:
#     if item[0] >= 10:
#         print(item)

# TODO: Projít všechny složky s obrázky k porovnání
# TODO: Uložit nějaka data do složek (jako soubor) - název stavby, lokalita(GPS), ...
# TODO: Ukládat data z výpočtu práznaků
# TODO: Determinovat jaký obrázek je nejlepší match

def main():
    result = []

    # START
    # load input img metadata
    meta_data = extract_gps.ImageMetaData(THE_CHOSEN_ONE)
    latlng = meta_data.get_lat_lng()
    print(latlng)
    print("**********************************")
    # END

    res = compare_all_images_from_folder(result)

    # filter out None items
    result = list(filter(None, res))
    # sort by shortest distance for 4 features per image
    result.sort(key=operator.itemgetter(4))
    # take best image an its propetries
    img_path, img1, img2, count, total_distance, keypoints1, keypoints2, top_matches = result[0]

    print(img_path)

    get_keypoints_coordinates(keypoints1, keypoints2, top_matches)

    H, mask = cv2.findHomography(np.array(list_keypoints2), np.array(list_keypoints1))

    warped_img = cv2.warpPerspective(img2, H, dsize=(img1.shape[1], img1.shape[0]))

    res_image = cv2.addWeighted(img1.copy(), 1, warped_img, 1, 0, img1.copy())

    cv2.imwrite('warped.png', res_image)


if __name__ == "__main__":
    main()
