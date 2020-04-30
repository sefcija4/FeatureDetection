#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import pickle

from opencv_serializer import *
from input_image import *
from extractor_and_matcher import *
from homography import *


class Building(object):

    def __init__(self):
        self.id = None
        self.location = None
        self.name = None
        self.path = None

    def set_from_json(self, data):
        """
        Initialize object Building parameters from json file
        :param data: (dict)
        """
        self.id = data['id']
        self.location = GPSLocation(data['latitude'], data['longtitude'])
        self.name = data['name']
        self.path = data['path']

    def get_longtitude(self):
        return self.location.get_longtitude()

    def get_latitude(self):
        return self.location.get_latitude()

    def print(self):
        print("---------------------------")
        print(self.id)
        self.location.print()
        print(self.name)
        print(self.path)

    def print_id_name(self):
        print("---------------------------")
        print(self.id, self.name)


class BuildingFeature(object):

    def __init__(self, name, path, path_org):
        self.id = name
        self.path = path
        self.original = path_org
        self.img = None
        self.keypoints = None
        self.descriptor = None
        self.matches = None

    def set_from_dict_file(self, data):
        # TODO: load kp a desc using BuildingRepository
        pass

    def load_image(self, path):
        self.img = cv2.imread(path)
        # print(self.img.shape)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

    def set_keypoints(self, kp):
        self.keypoints = kp

    def set_descriptor(self, desc):
        self.descriptor = desc

    def update_matches(self, matches):
        self.matches = matches

    def get_num_of_matches(self):
        return len(self.matches)

    def get_sum_of_matches(self):
        """
        Sum distances of 10 best matches
        :return: sum of all distances
        """
        total_distance = 0

        self.sort_matches_by_distance()

        for m in self.matches[:10]:
            total_distance += m.distance

        return total_distance

    def sort_matches_by_distance(self):
        self.matches.sort(key=lambda x: x.distance)


class BuildingRepository(object):

    @staticmethod
    def get_all_buildings(path):
        """
        Load building data (in json format) from file
        :param path: (string) path to json file
        :return: (object) Building
        """
        buildings = list()

        with open(path) as file:
            data = json.load(file)

            for x in data:
                for y in data[x]:
                    b = Building()
                    b.set_from_json(y)
                    buildings.append(b)
            file.close()

        return buildings

    @staticmethod
    def get_building_features(folder):
        """
        Load keypoints and descriptors from each image of building's file and return them.
        :param folder: (str) folder in db of specific building
        :return: (object) list of BuildingFeatures
        """
        buildings = list()

        for img in os.listdir(folder):

            if img.endswith('.txt'):
                continue

            tmp_b = BuildingFeature(img[:-4], str(f'{folder}\{img}'), str(f'{folder}_original\{img[:-4]}_small.jpg'))
            path = str(f'{folder}\{img[:-4]}')

            # KEYPOINTS
            kp_load = list()

            with open(str(f'{path}_keypoints.txt'), 'rb') as file:
                to_load = pickle.load(file, encoding='utf-8')

            for kp in to_load:
                kp_load.append(CVSerializer.dict_to_cv_keypoint(kp))

            # DESCRIPTOR
            with open(str(f'{path}_descriptor.txt'), 'rb') as file:
                desc_load = pickle.load(file, encoding='utf-8')

            tmp_b.set_keypoints(kp_load)
            tmp_b.set_descriptor(desc_load)

            buildings.append(tmp_b)

        return buildings


class App(str):

    def __init__(self, path):
        self.img_in = None
        self.dir_name = os.path.dirname(__file__)
        self.db_path = os.path.join(self.dir_name, path)
        self.buildings = list()
        self.buildings_features = dict()
        self.matcher = None
        self.matches = None
        self.warped_img = None

        self.sift = None
        self.orb = None
        self.surf = None

        self.best_match = None

    def load_buildings(self):
        """
        Load all buildings metadata
        """

        self.buildings = BuildingRepository.get_all_buildings(self.db_path)

        print("Loaded buildings:")

        for x in self.buildings:
            x.print_id_name()
        print("************************")

    def load_features(self, building):
        """
        Load keypoints and descriptors from specific building
        :param building: (object) Building
        """
        self.buildings_features[building.id] = BuildingRepository.get_building_features(building.path)

    def load_image(self, path):
        """
        Load image from path
        :param path: (str)
        """
        self.img_in = Image(path)

    def check_perimeter(self):
        """
        Check if buildings from dataset belongs in perimeter + load it's features
        """
        num_of_loaded = 0
        for building in self.buildings:
            if GPSLocation.check_if_belongs(self.img_in, building):
                print(building.path, "Patří do okolí")
                self.load_features(building)
                num_of_loaded += 1
            else:
                print(building.path, "Nepatří do okolí")

        if num_of_loaded == 0:
            print("No building has been found in your perimeter")
            return False
        else:
            return True

    def match_features(self):
        """
        Match features using selected matcher #TODO: volba příznaku
        :return:
        """
        self.img_in.extract_features()

        self.matcher = Matcher()
        self.matcher.set_sift_match()

        self.matcher.match_sift(self.img_in.get_descriptor(), self.buildings_features)

    def find_best_match(self):
        self.best_match = self.matcher.best_match(self.buildings_features)
        # print("Best match img:", self.best_match.path)

        if self.best_match is None:
            print("No building has good match. You should change your viewing angle and position")
            return False

        else:
            self.best_match.sort_matches_by_distance()
            return True

    def find_best_keypoints(self):
        # Find best 4 keypoints from best match
        self.best_match.matches = Matcher.filter_out_close_keypoints(self.best_match.matches, self.img_in.keypoints)

    def show_matches(self):
        matches = self.matcher.show_matches(self.img_in, self.buildings_features)

        for m in matches:
            cv2.imshow('Matches', m)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def warp_image(self):
        homography = Homography()
        homography.find_matrix(self.best_match.matches, self.img_in.keypoints, self.best_match.keypoints)
        self.best_match.load_image(self.best_match.path)

        # print(self.best_match.img.shape)

        # warped_img = homography.warp_image(self.img_in.img, self.best_match.img.copy())

        # VISUALIZATION

        self.visualization(homography)

        #merged_img = self.img_in.merge_image(warped_img)

        # cv2.imshow('Warped', merged_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # get keypoints, matches and img1, im2 to Homography
        # maybe try using Building_features?

    def visualization(self, homography):
        # ORIGINAL IMAGE
        print(self.best_match.original)
        original_img = cv2.imread(self.best_match.original)
        # original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

        print(original_img.shape)

        warped_original_img = homography.warp_image(self.img_in.img, original_img.copy())
        original_bg = cv2.cvtColor(self.img_in.img, cv2.COLOR_GRAY2BGR)

        # masks
        original_mask = Visualization.create_mask(warped_original_img)
        bg_original_mask = cv2.bitwise_not(original_mask)

        print(warped_original_img.shape, original_mask.shape)

        original_img = cv2.bitwise_or(warped_original_img, warped_original_img, mask=original_mask[:, :, 0])
        original_bg = cv2.bitwise_or(original_bg, original_bg, mask=bg_original_mask[:, :, 0])

        print(original_bg.shape, original_img.shape)

        original_final = cv2.bitwise_or(original_img, original_bg)

        cv2.imshow('Warped original', original_final)
        cv2.waitKey(0)

        # MERGING
        img_mask = Visualization.create_mask(self.best_match.img)
        img_to_merge = cv2.imread(self.best_match.original)
        building_rgba = cv2.bitwise_or(img_to_merge, img_to_merge, mask=img_mask)
        building_rgba = homography.warp_image(self.img_in.img, building_rgba.copy())

        # warp mask, etc.
        bg_mask = homography.warp_image(self.img_in.img, img_mask.copy())
        bg_mask = cv2.bitwise_not(bg_mask)

        bk = cv2.bitwise_or(self.img_in.img, self.img_in.img, mask=bg_mask)

        # combine foreground+background
        bk = cv2.cvtColor(bk, cv2.COLOR_GRAY2BGR)

        print(bk.shape, building_rgba.shape)

        final = cv2.bitwise_or(building_rgba, bk)

        cv2.imshow('Final', final)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def print_buildings(self):
        for x in self.buildings:
            print(x.data['name'])


app = App('data.txt')
app.load_buildings()

app.load_image('data\\_p\\test.jpg')
# app.load_image('data\\_p\\test_b_4.jpg') # lepší dataset
# app.load_image('data\\_p\\test_b_5.jpg')
# app.load_image('data\\_p\\test_b_7.jpg')
# app.load_image('data\\_p\\test_b_8.jpg')
# app.load_image('data\\_p\\test_b_9.jpg') # stíny/lampa atd.
# app.load_image('data\\_p\\IMG_3513.jpg')
app.img_in.preprocess()
app.img_in.print()

# app.img_in.show()

if app.check_perimeter():

    app.match_features()

    if app.find_best_match():

        app.find_best_keypoints()

        app.warp_image()

        app.show_matches()


# img.show()
