#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config_handler import *
from building_repository import *
from input_image import *
from matcher import *
from homography import *
from visualization import *
import config


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
        Match features using FLANN matcher for SIFT #TODO: volba příznaku
        """
        self.img_in.extract_features()

        self.matcher = Matcher()
        self.matcher.set_sift_match(self.config.get_flann_matching_setup())

        self.matcher.match_sift(self.img_in.get_descriptor(), self.buildings_features)

    def find_best_match(self):
        """
        Get best match from all matches
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
        Get 4 keypoints from the best match. Keypoints must be far enough from each other.
        -
        More about the distance threshold: matcher.py or written documentation
        """
        # Find best 4 keypoints from best match
        self.best_match.matches = Matcher.filter_out_close_keypoints(self.best_match.matches, self.img_in.keypoints,
                                                                     self.config.get_filter_features())

        return self.best_match.matches

    def show_matches(self):
        """
        Show matches of all buildings nearby in new window
        """
        matches = self.matcher.show_matches(self.img_in, self.buildings_features)

        for m in matches:
            cv2.imshow('Matches', m)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def warp_image(self):
        """
        Get transformation matrix from best four keypoints
        """
        homography = Homography()
        homography.find_matrix(self.best_match.matches, self.img_in.keypoints, self.best_match.keypoints)
        self.best_match.load_image(self.best_match.path)

        # VISUALIZATION
        self.visualization(homography)

    def visualization(self, homography):
        """
        Visualize final transformation using original input image and final dataset cropped image
        :param homography: (Homography)
        """
        # ORIGINAL IMAGE
        original_photo = Visualization.merge_images(self.img_in.img, self.best_match.original, homography)

        cv2.imshow('Warped original', original_photo)
        cv2.waitKey(0)

        # FINAL
        final_photo = Visualization.merge_images(self.img_in.img, self.best_match.path, homography)

        cv2.imshow('Final', final_photo)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def print_buildings(self):
        for x in self.buildings:
            print(x.data['name'])


if __name__ == "__main__":

    # update config
    config.main()

    app = App('config.json')
    app.load_buildings()

    app.load_image()
    app.img_in.preprocess()
    app.img_in.print()

    if app.check_perimeter():

        app.match_features()

        if app.find_best_match():

            if app.find_best_keypoints() is not None:

                app.warp_image()

                app.show_matches()
