#### Helper file with methods for Logo detection (Pat)

import json
import cv2
import os
import glob
import face_recognition
import numpy as np
import asyncio


def getFeatures(img):
    """Find and return features from image

    Parameters:
    img ():

    Returns:
    key points: kps
    descriptors: descs
    image: img.shape
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detector = createDetector()
    kps, descs = detector.detectAndCompute(gray, None)
    return kps, descs, img.shape[:2][::-1]

def createDetector():

    """Create cv2 detector to read image

    Parameters:
    None

    Returns:
    ORB: detector
    """

    detector = cv2.ORB_create(nfeatures=2000)
    return detector



def detectFeatures(img, train_features):

    """Uses key points and descriptors to detect features

    Parameters:
    img (image): frame from camera
    train_features (): features to look for in the frame

    Returns:
    boolean: rect
    """
    train_kps, train_descs, shape = train_features
    # get features from input image
    kps, descs, _ = getFeatures(img)
    # check if keypoints are extracted
    if not kps:
        return None
    # now we need to find matching keypoints in two sets of descriptors (from sample image, and from current image)
    # knnMatch uses k-nearest neighbors algorithm for that
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(train_descs, descs, k=2)
    good = []
    # apply ratio test to matches of each keypoint
    # idea is if train KP have a matching KP on image, it will be much closer than next closest non-matching KP,
    # otherwise, all KPs will be almost equally far
    for m, n in matches:
        if m.distance < 0.8 * n.distance:
            good.append([m])
    # stop if we didn't find enough matching keypoints
    if len(good) < 0.1 * len(train_kps):
        return None
    # estimate a transformation matrix which maps keypoints from train image coordinates to sample image
    src_pts = np.float32([train_kps[m[0].queryIdx].pt for m in good
                          ]).reshape(-1, 1, 2)
    dst_pts = np.float32([kps[m[0].trainIdx].pt for m in good
                          ]).reshape(-1, 1, 2)
    m, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    if m is not None:
        # apply perspective transform to train image corners to get a bounding box coordinates on a sample image
        scene_points = cv2.perspectiveTransform(
            np.float32([(0, 0), (0, shape[0] - 1), (shape[1] - 1, shape[0] - 1), (shape[1] - 1, 0)]).reshape(-1, 1, 2),
            m)
        rect = cv2.minAreaRect(scene_points)
        # check resulting rect ratio knowing we have almost square train image
        if rect[1][1] > 0 and 0.8 < (rect[1][0] / rect[1][1]) < 1.2:
            return rect
    return None


def detectLogo(frame, brand):

    """ Use frame from camrea and image file in folder to compare logos

    Parameters:
    frame (img): frame from camera with logo being shown
    brand (img): image file used for logo comparison

    Returns:
    None
    """
    print("detecting...")
    files = [f for f in glob.glob("Logos/" + brand + '/*.jpg')]
    train_features = []

    for file in files:
        img = cv2.imread(file)
        train_features.append(getFeatures(img))
        # print("trained: " + file)

    for trained in train_features:
        found = False
        region = detectFeatures(frame, trained)
        if region is not None:
            # draw rotated bounding box
            box = cv2.boxPoints(region)
            box = np.int0(box)
            cv2.drawContours(img, [box], 0, (0, 255, 0), 2)
            print("We recognize this " + brand + " logo.")
        # display the image
        cv2.imshow("Preview", img)
    if not found:
        print("We do not recognize this " + brand + " logo.")
