#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

sift = cv2.xfeatures2d.SIFT_create()
# surf = cv2.xfeatures2d.SURF_create()
# orb = cv2.ORB_create(nfeatures=2500)

DISTANCE_THRESHOLD = 45.0
NUM_OF_MATCHES = 50
# results = list()


def load_images(pth1, pth2):
    img_1 = cv2.imread(pth1, cv2.IMREAD_GRAYSCALE)
    img_2 = cv2.imread(pth2, cv2.IMREAD_GRAYSCALE)

    return img_1, img_2


def equalize_histogram(img):
    return cv2.equalizeHist(img)


def detect_and_compute(img1, img2):
    key_pt_orb1, desc1 = sift.detectAndCompute(img1, None)
    key_pt_orb2, desc2 = sift.detectAndCompute(img2, None)

    return key_pt_orb1, desc1, key_pt_orb2, desc2


def draw_keypoints(img, keypoints):
    return cv2.drawKeypoints(img, keypoints, None)


def brute_force_matching(desc1, desc2):
    # OBR
    # bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # SIFT
    bf = cv2.BFMatcher()

    match = bf.match(desc1, desc2)
    # Sort matches by distance (ascending)
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


def get_good_and_unused_keypoints_ration(keypoints1, keypoints2, good_keypoints):
    # min_value = len(keypoints1) if len(keypoints1) <= len(keypoints2) else len(keypoints2)
    max_value = len(keypoints1) if len(keypoints1) > len(keypoints2) else len(keypoints2)
    return good_keypoints/max_value


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    """
    Resize an image
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

    new_height = get_smaller_img(img1, img2)

    img1 = equalize_histogram(img1)

    img1 = image_resize(img1, height=new_height)
    img2 = image_resize(img2, height=new_height)

    keypoints1, descriptors1, keypoints2, descriptors2 = detect_and_compute(img1, img2)

    # FLANN based matcher
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=100)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    knn_matches = flann.knnMatch(descriptors1, descriptors2, k=2)

    # Filter matching using Lowe's ration test
    ratio_thresh = 0.6  # recommended value is 0.7
    good_matches = []
    count = 0
    for m, n in knn_matches:
        if m.distance < ratio_thresh * n.distance:
            # print(m.distance)
            good_matches.append(m)
            count += 1

    top_10 = sorted(good_matches, key=lambda x: x.distance)[:10]

    # check if there is more than 10 good matches
    if len(top_10) < 10:
        print("Less than 10 mathes found!")
        return None

    # position of each matched keypoints (x,y)
    '''list_keypoints1 = []
    list_keypoints2 = []

    # Take four best matches and save their positions
    for m in top_10[:4]:
        print(m.distance)
        # Get the matching keypoints for each of the images
        img1_idx = m.queryIdx
        img2_idx = m.trainIdx

        # x - columns
        # y - rows
        # Get the coordinates
        (x1, y1) = keypoints1[img1_idx].pt
        (x2, y2) = keypoints2[img2_idx].pt

        print(x1, y1)
        print(x2, y2)

        # Append to each list
        list_keypoints1.append((x1, y1))
        list_keypoints2.append((x2, y2))

    print((img1.shape[0], img1.shape[1]))
    H, mask = cv2.findHomography(np.array(list_keypoints2), np.array(list_keypoints1))

    print(H)

    warped_img = cv2.warpPerspective(img2, H, dsize=(img1.shape[1], img1.shape[0]))

    res_image = cv2.addWeighted(img1.copy(), 1, warped_img, 1, 0, img1.copy())

    cv2.imwrite('warped.png', res_image)'''

    # TODO: výše uvedenou funkcionalitu udělat pouze na výsledný obrázek, ten s nejlepší shodou

    # -- Print info
    get_filename(p2)  # print name of current file
    print(f'{len(keypoints1)} × {len(keypoints2)}')
    print(f'ratio: {get_good_and_unused_keypoints_ration(keypoints1, keypoints2, len(good_matches)):.4f} :,'
          f'{len(keypoints1), len(keypoints2)}')
    print(f'number of "good" matches:{count}')

    # -- Results
    # distance_avg = 0
    # for n in good_matches:
    #    distance_avg += n.distance

    # results.append((count, distance_avg/count, p2, top_10[:4]))

    # -- Draw matches
    img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1] + img2.shape[1], 3), dtype=np.uint8)
    cv2.drawMatches(img1, keypoints1, img2, keypoints2, top_10[:4], img_matches,
                    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # -- Show detected matches
    cv2.imshow('Good Matches', img_matches)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # cv2.imwrite("C:\\Users\\Sefci\\Documents\\_FIT\\_Bakalarka\\data_staromak\\images\\"+img_name, img_matches)
    print('------------------------------')

    total_distance = 0
    for m in top_10[:4]:
        total_distance += m.distance

    return p2, img1, img2, count, total_distance, keypoints1, keypoints2, top_10[:4]
