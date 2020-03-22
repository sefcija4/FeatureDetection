#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
# My imports
import feature_detection
import extract_gps

THE_CHOSEN_ONE = "C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\_p\\test1.jpg"

# folder should contain only img files
FOLDER_PATH = "C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b1"

data = list()

data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b1")
data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b2")
data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b3")
data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b4")
data.append("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\b5")


def by_count(value):
    return value[0]


# take all images (all files and folders)
def compare_all_images_from_folder():
    for folder in data:
        for img in os.listdir(folder):
            path = str(f'{folder}\{img}')
            # print(path)
            feature_detection.compare_descriptors(THE_CHOSEN_ONE, path)


compare_all_images_from_folder()


feature_detection.results.sort(reverse=True)
for item in feature_detection.results:
    if item[0] >= 10:
        print(item)

# TODO: Projít všechny složky s obrázky k porovnání
# TODO: Uložit nějaka data do složek (jako soubor) - název stavby, lokalita(GPS), ...
# TODO: Ukládat data z výpočtu práznaků
# TODO: Determinovat jaký obrázek je nejlepší match
