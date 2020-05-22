#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from scipy.spatial import distance


class Matcher(object):
    """
    Methods for feature and image matching
    """

    def __init__(self):
        self.matcher = None

    def set_sift_match(self, flann_data):
        """
        Set FLANN matcher for SIFT
        :param flann_data: (dict) flann parameters
        """
        index_params = dict(algorithm=flann_data['flann_index'], trees=flann_data['flann_trees'])
        search_params = dict(checks=flann_data['flann_checks'])   # or pass empty dictionary
        self.matcher = cv2.FlannBasedMatcher(index_params, search_params)

    def match_sift(self, in_img_descriptor, dataset):
        """
        Match each image from dataset with input image using SIFT
        :param in_img_descriptor: () input image descriptor
        :param dataset: (BuildingFeature) list of buildings
        :return:
        """

        # Match each building (in surroundings) witch input image
        for building in dataset:
            for img in dataset[building]:  # img type (BuildingFeature)

                img.matches = self.matcher.knnMatch(in_img_descriptor, img.descriptor, k=2)
                img.update_matches(self.ratio_test(img.matches))

    @staticmethod
    def ratio_test(matches, ratio=0.6):
        """
        Filter out bad matches using Lowe's ratio test
        :param matches: (list) matches
        :param ratio: default value 0.6
        :return: sorted list of good matches
        """
        good_matches = list()
        count = 0

        for m, n in matches:
            if m.distance < ratio * n.distance:
                # print(m.distance)
                good_matches.append(m)
                count += 1

        # matches are sorted by euclid's distance (lower=better)
        return sorted(good_matches, key=lambda x: x.distance)

    def show_matches(self, img_in, dataset):
        """
        Show mathes
        :param img_in: input image
        :param dataset: dataset of buildings
        :return: list of images
        """
        matches = list()

        for building in dataset:
            for img in dataset[building]:
                img.load_image(img.path)
                img_matches = self.draw_matches(img_in.img, img.img, img_in.keypoints, img.keypoints, img.matches)
                matches.append(img_matches)

        return matches

    @staticmethod
    def draw_matches(img1, img2, keypoints1, keypoints2, matches,
                     flag=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS):
        """
        Create new image with img1 and img2 and draw lines between matched keypoints
        :param img1: input_image
        :param img2: building (dataset) image
        :param keypoints1: input_image keypoints
        :param keypoints2: building's keypoints
        :param matches: matched features for img1 and image2
        :param flag: cv2.flag for cv2.drawMatches()
        :return: image with visualized mathes
        """
        img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1] + img2.shape[1], 3), dtype=np.uint8)
        # drawMatchesNkk for list
        # drawMatches for cv::DMatch
        cv2.drawMatches(img1, keypoints1, img2, keypoints2, matches[:4], img_matches, flags=flag)
        return img_matches

    @staticmethod
    def best_match(matches, threshold):
        """
        Find best matching image to input image
        :param matches: matches
        :param threshold: minimal number of good matches to be consider as successful recognition
        :return: best matching image / None
        """
        results = list()

        for building in matches:
            for img in matches[building]:
                if img.get_num_of_matches() < threshold['min_number_of_matches']:
                    continue
                else:
                    results.append(img)

        if len(results) == 0:
            print("No match!")
            return False, matches  # used later: show_matches()

        results = sorted(results, key=lambda x: x.get_sum_of_matches(), reverse=False)

        for res in results:
            print(res.get_sum_of_matches())

        print("Best match:", results[0].path)

        return True, results[0]

    @staticmethod
    def check_distances(kp, prev_match, cur_match, threshold):
        """
        Check distance between two keypoints in input image
        :param kp: current keypoint
        :param prev_match:
        :param cur_match:
        :param threshold: minimal distance between two keypoints
        :return: (boolean) if keypoints are further than threshold value
        """
        min_distance = threshold['pixel_distance']  # in pixels

        curr = cur_match.queryIdx

        for p_m in prev_match:
            prev = p_m.queryIdx

            # x - columns, y - rows
            (x1, y1) = kp[curr].pt  # previous keypoint's coordinates
            (x2, y2) = kp[prev].pt  # current  keypoint's coordinates

            if distance.euclidean((x1, y1), (x2, y2)) <= min_distance:
                return False

        print("Add keypoint:", (x2, y2))
        return True

    @staticmethod
    def filter_out_close_keypoints(matches, kp, threshold):
        """
        Find best four keypoints. Start from best keypoint and than check every other keypoint is far enough
        :param matches:
        :param kp: keypoints
        :param threshold: minimal distance between two points
        :return: best four keypoints
        """

        best_four = list()

        start = matches[0]
        best_four.append(start)

        for m in matches:
            if len(best_four) > 4:
                break
            if Matcher.check_distances(kp, best_four, m, threshold):
                best_four.append(m)

        if len(best_four) < 4:
            print('Keypoints are not far enough')
            return False, matches  # used later: show_matches()

        return True, best_four
