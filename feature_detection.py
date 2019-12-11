#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np

# My imports
# import load_images

# TODO: downgrade version of opencv to older version, to make SIFT and SURF working
sift = cv2.xfeatures2d.SIFT_create()
surf = cv2.xfeatures2d.SURF_create()
orb = cv2.ORB_create(nfeatures=2500)

DISTANCE_THRESHOLD = 45.0
NUM_OF_MATCHES = 50

RESULT_PATH = "C:\\Users\Sefci\\Documents\\_FIT\\_Bakalarka\\1_FeatureDetecionResults"

def load_images(pth1, pth2):
    img_1 = cv2.imread(pth1, cv2.IMREAD_GRAYSCALE)
    img_2 = cv2.imread(pth2, cv2.IMREAD_GRAYSCALE)

    return img_1, img_2


def detect_and_compute(img1, img2):
    # SURF
    key_pt_orb1, desc1 = sift.detectAndCompute(img1, None)
    key_pt_orb2, desc2 = sift.detectAndCompute(img2, None)

    # SURF
    # key_pt_orb1, desc1 = surf.detectAndCompute(img1, None)
    # key_pt_orb2, desc2 = surf.detectAndCompute(img2, None)

    # ORB
    # key_pt_orb1, desc1 = orb.detectAndCompute(img1, None)
    # key_pt_orb2, desc2 = orb.detectAndCompute(img2, None)

    return key_pt_orb1, desc1, key_pt_orb2, desc2


def draw_keypoints(img, keypoints):
    return cv2.drawKeypoints(img, keypoints, None)


def brute_force_matching(desc1, desc2):
    # OBR
    # bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # SIFT
    bf = cv2.BFMatcher()

    match = bf.match(desc1, desc2)
    # Sort matches by distance low to height
    return sorted(match, key=lambda x: x.distance)


def get_average_distance(match):
    distance_sum = 0

    for d in match[:NUM_OF_MATCHES]:
        # print(d.distance)
        distance_sum += d.distance

    average = distance_sum/NUM_OF_MATCHES

    print(f"Average distance: {average}")
    return average


def is_same(avg_dist):
    if avg_dist <= DISTANCE_THRESHOLD:
        print("SAME")
        return True
    else:
        print("DIFFERENT")
        return False


def show_result(img_1, key_pts_orb1, img_2, key_pts_orb2, match):
    # Flags=2 -> hide unmatched keypoints
    matching_result = cv2.drawMatches(img_1, key_pts_orb1, img_2, key_pts_orb2, match[:NUM_OF_MATCHES], None, flags=2)
    cv2.imshow("Image", matching_result)


def get_smaller_img(img1, img2):
    # print(f'size h,w: {img1.shape}')
    # print(f'size h,w: {img2.shape}')

    # find minimal height
    min_height = img1.shape[0] if img1.shape[0] <= img2.shape[0] else img2.shape[0]
    # print(min_height)
    return min_height


def get_filename(path):
    print(path.split('\\')[-1:][0])


def get_keypoints_ration(keypoints1, keypoints2):
    min_value = len(keypoints1) if len(keypoints1) <= len(keypoints2) else len(keypoints2)
    max_value = len(keypoints1) if len(keypoints1) > len(keypoints2) else len(keypoints2)

    return min_value/max_value

def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    """

    :param image: image
    :param width: (int)
    :param height: (int)
    :param inter: (cv2) type of interpolation
    :return: resized image
    """
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the original image
    if width is None and height is None:
        print('set at least one dimension')
        return image

    if height is not None:
        r = height / float(h)
        dim = (int(w * r), height)

    else:
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    img_resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return img_resized


def compare_descriptors(p1, p2):
    img1, img2 = load_images(p1, p2)

    # TODO: spočítat pravděpodobnost Match rate poměr mezi nalezenými body a počtem nalezených spojení

    new_height = get_smaller_img(img1, img2)

    img1 = image_resize(img1, height=new_height)
    img2 = image_resize(img2, height=new_height)

    keypoints1, descriptors1, keypoints2, descriptors2 = detect_and_compute(img1, img2)

    print(f'{len(keypoints1)} × {len(keypoints2)}')
    print(f'ratio: {get_keypoints_ration(keypoints1, keypoints2):.4f}')
    # img1_ORB = draw_keypoints(img1, keypoints_orb1)
    # img2_ORB = draw_keypoints(img2, keypoints_orb2)

    # Brute force matching
    # matches = brute_force_matching(descriptors1, descriptors2)

    # FLANN based matcher
    # Since SURF is a floating-point descriptor NORM_L2 is used
    matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
    knn_matches = matcher.knnMatch(descriptors1, descriptors2, 2)

    # Filter matching using Lowe's ration test
    ratio_thresh = 0.7  # recommended value is 0.7
    good_matches = []
    count = 0
    for m, n in knn_matches:
        if m.distance < ratio_thresh * n.distance:
            # print(m.distance)
            good_matches.append(m)
            count += 1

    get_filename(p2)  # print name of current file
    print(f'number of "good" matches:{count}')

    # -- Draw matches
    img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1] + img2.shape[1], 3), dtype=np.uint8)
    cv2.drawMatches(img1, keypoints1, img2, keypoints2, good_matches, img_matches, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # -- Show detected matches
    cv2.imshow('Good Matches', img_matches)
    print('------------------------------')
    # result_path = str(f'C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\1_FeatureDetectionResults\\{get_filename(p2)}')
    # cv2.imwrite(result_path, img_matches)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Flags=2 -> hide unmatched keypoints
    # show_result(img1, keypoints_orb1, img2, keypoints_orb2, matches)




path1 = "C:\\Users\Sefci\\Documents\\_FIT\\_Bakalarka\\1_FeatureDetecion\\vilaTegendhat1.jpg"
path2 = "C:\\Users\Sefci\\Documents\\_FIT\\_Bakalarka\\1_FeatureDetecion\\vilaTegendhat2.jpg"
path3 = "C:\\Users\Sefci\\Documents\\_FIT\\_Bakalarka\\1_FeatureDetecion\\vilaTegendhat3.jpg"

path4 = "C:\\Users\Sefci\\Documents\\_FIT\\_Bakalarka\\1_FeatureDetecion\\house1.jpg"
path5 = "C:\\Users\Sefci\\Documents\\_FIT\\_Bakalarka\\1_FeatureDetecion\\house2.jpg"
path6 = "C:\\Users\Sefci\\Documents\\_FIT\\_Bakalarka\\1_FeatureDetecion\\house3.png"

path7 = "C:\\Users\Sefci\\Documents\\_FIT\\_Bakalarka\\1_FeatureDetecion\\dogs1.jpg"

#compare_descriptors(path1, path2)  # Same
# compare_descriptors(path1, path3)  # Same
# compare_descriptors(path1, path4)  # Different
# compare_descriptors(path1, path5)  # Different
# compare_descriptors(path1, path6)  # Different
# compare_descriptors(path1, path7)  # Different
