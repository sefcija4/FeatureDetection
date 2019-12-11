#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

# My imports
import feature_detection

THE_CHOSEN_ONE = "C:\\Users\Sefci\\Documents\\_FIT\\_Bakalarka\\__MainImage\\fa_fit.jpg"

# folder should contain only img files
FOLDER_PATH = "C:\\Users\Sefci\\Documents\\_FIT\\_Bakalarka\\1_FeatureDetection"


# take all images (all files and folders)
def compare_all_images_from_folder():
    for img in os.listdir(FOLDER_PATH):
        path = str(f'{FOLDER_PATH}\{img}')

        feature_detection.compare_descriptors(THE_CHOSEN_ONE, path)
        # feature_detection.compare_descriptors(THE_CHOSEN_ONE, path)

compare_all_images_from_folder()

# TODO: Uložit obrázky s počtem dobrých příznaků atd.

# TODO: Filtrovat rozložení příznaků (zda nevzdnikají shluky)
