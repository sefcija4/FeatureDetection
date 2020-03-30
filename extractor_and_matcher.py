#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


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
            print(type(dataset))
            for img in dataset[building]:
                # TODO: získat jednu budovu, poronat, spočítat match a uložit do Building Features

                img.matches = self.matcher.knnMatch(in_img_descriptor, img.descriptor, k=2)
                print(f'Number of matches {img.id}: {len(img.matches)}')

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
        for building in dataset:
            print(type(dataset))
            for img in dataset[building]:
                print(img.path)
                img.load_image(img.path)
                img_matches = self.draw_matches(img_in.img, img.img, img_in.keypoints, img.keypoints, img.matches)

                cv2.imshow('Matches', img_matches)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    def draw_matches(self, img1, img2, keypoints1, keypoints2, matches,
                     flag=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS):

        print(img1.shape[0], img1.shape[1])
        print(img2.shape[0], img2.shape[1])
        print(type(matches))

        img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1] + img2.shape[1], 3), dtype=np.uint8)
        #drawMatchesNkk for list
        #drawMatches for cv::DMatch
        cv2.drawMatchesKnn(img1, keypoints1, img2, keypoints2, matches, img_matches,
                        flags=flag)
        return img_matches
