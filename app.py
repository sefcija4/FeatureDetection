#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config_handler import *
from building_repository import *
from input_image import *
from matcher import *
from homography import *


class App(str):

    def __init__(self, path):
        """
        App constructor
        :param path: path to config json file
        """
        self.config = Config(path)

        self.img_in = None
        self.dir_name = os.path.dirname(__file__)
        self.db_path = os.path.join(self.dir_name, self.config.get_metadata())
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
        print("-----------------------")

    def load_features(self, building):
        """
        Load keypoints and descriptors from specific building
        :param building: (object) Building
        """
        self.buildings_features[building.id] = BuildingRepository.get_building_features(building.path)

    def load_image(self):
        """
        Load image from path
        :param path: (str)
        """
        self.img_in = Image(self.config.get_input_image())

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
        self.matcher.set_sift_match(self.config.get_flann_matching_setup())

        self.matcher.match_sift(self.img_in.get_descriptor(), self.buildings_features)

    def find_best_match(self):
        """

        :return:
        """
        self.best_match = self.matcher.best_match(self.buildings_features, self.config.get_filter_features())
        # print("Best match img:", self.best_match.path)

        if self.best_match is None:
            print("No building has good match. You should change your viewing angle and position")
            return False

        else:
            self.best_match.sort_matches_by_distance()
            return True

    def find_best_keypoints(self):
        """

        :return:
        """
        # Find best 4 keypoints from best match
        self.best_match.matches = Matcher.filter_out_close_keypoints(self.best_match.matches, self.img_in.keypoints,
                                                                     self.config.get_filter_features())

    def show_matches(self):
        """

        :return:
        """
        matches = self.matcher.show_matches(self.img_in, self.buildings_features)

        for m in matches:
            cv2.imshow('Matches', m)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def warp_image(self):
        """

        :return:
        """
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
        """

        :param homography:
        :return:
        """
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


if __name__ == "__main__":

    app = App('config.json')
    app.load_buildings()

    app.load_image()

    # app.load_image('data\\_p\\test.jpg')
    # app.load_image('data\\_p\\test_b_4.jpg') # lepší dataset
    # app.load_image('data\\_p\\test_b_5.jpg')
    # app.load_image('data\\_p\\test_b_7.jpg')
    # app.load_image('data\\_p\\test_b_8.jpg')
    # app.load_image('data\\_p\\test_b_9.jpg') # stíny/lampa atd.
    # app.load_image('data\\_p\\IMG_3513.jpg')
    app.img_in.preprocess()
    app.img_in.print()

    if app.check_perimeter():

        app.match_features()

        if app.find_best_match():

            app.find_best_keypoints()

            app.warp_image()

            app.show_matches()
