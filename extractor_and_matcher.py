#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import operator
from scipy.spatial import distance


class FeatureExtractor(object):

    '''def __init__(self):
        self.sift = cv2.xfeatures2d.SIFT_create()
        # self.surf = cv2.xfeatures2d.SURF_create()
        # self.orb = cv2.ORB_create(nfeatures=number_of_features)'''

    # TODO: pick feature descriptor (SIFT, ORB, SURF)

    @staticmethod
    def extract_sift(img):
        sift = cv2.xfeatures2d.SIFT_create()
        keypoint, descriptor = sift.detectAndCompute(img, None)
        return keypoint, descriptor

    def extract_surf(self):
        pass

    def extract_orb(self):
        pass


class Matcher(object):

    def __init__(self):
        self.matcher = None

    def set_sift_match(self):
        # TODO: set flann param.
        flann_index = 1
        index_params = dict(algorithm=flann_index, trees=5)
        search_params = dict(checks=100)   # or pass empty dictionary
        self.matcher = cv2.FlannBasedMatcher(index_params, search_params)

    def match_sift(self, in_img_descriptor, dataset):

        for building in dataset:
            # print(type(dataset))
            for img in dataset[building]:
                # TODO: získat jednu budovu, poronat, spočítat match a uložit do Building Features

                img.matches = self.matcher.knnMatch(in_img_descriptor, img.descriptor, k=2)
                img.update_matches(self.ratio_test(img.matches))
                # print(len(img.matches))
                # print(f'Number of matches {img.id}: {len(img.matches)}')

    def match_surf(self):
        pass

    def match_orb(self):
        pass

    def ratio_test(self, matches, ratio=0.6):
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
        matches = list()

        for building in dataset:
            for img in dataset[building]:
                # print(img.path)
                img.load_image(img.path)
                img_matches = self.draw_matches(img_in.img, img.img, img_in.keypoints, img.keypoints, img.matches)

                matches.append(img_matches)
        return matches

    @staticmethod
    def draw_matches(img1, img2, keypoints1, keypoints2, matches,
                     flag=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS):

        img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1] + img2.shape[1], 3), dtype=np.uint8)
        #drawMatchesNkk for list
        #drawMatches for cv::DMatch
        cv2.drawMatches(img1, keypoints1, img2, keypoints2, matches[:4], img_matches, flags=flag)
        return img_matches

    @staticmethod
    def best_match(matches):

        results = list()

        for building in matches:
            for img in matches[building]:
                if img.get_num_of_matches() < 10:  # small threshold
                    continue
                else:
                    results.append(img)

        results = sorted(results, key=lambda x: x.get_sum_of_matches(), reverse=True)

        if len(results) == 0:
            print("No match!")
            return None

        print("BEST:", results[0].path)

        return results[0]

    @staticmethod
    def check_distance(kp, prev_match, cur_match):
        min_distance = 200  # pixels TODO: relative to img size

        curr = cur_match.queryIdx
        prev = prev_match.queryIdx

        # x - columns
        # y - rows
        # Get the coordinates
        (x1, y1) = kp[curr].pt
        (x2, y2) = kp[prev].pt

        if distance.euclidean((x1, y1), (x2, y2)) <= min_distance:
            return False
        else:
            print("ADD:", (x2, y2))
            return True

    @staticmethod
    def filter_out_close_keypoints(matches, kp):
        # dostanu seřezné matches. Kontrola vzdálenosti mezi top 4mi.
        # Pokud bude vzdálenst menší vezmese další match.

        best_four = list()

        start = matches[0]
        best_four.append(start)
        prev_m = start

        for m in matches:
            if len(best_four) > 4:
                break

            if Matcher.check_distance(kp, prev_m, m):
                best_four.append(m)

            prev_m = m

        # print(best_four)

        return best_four
