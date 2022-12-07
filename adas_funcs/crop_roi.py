import cv2
import numpy as np


def crop_area(img, points):
    # (1) Crop the bounding rect
    rect = cv2.boundingRect(points)
    x, y, w, h = rect
    croped = img[y : y + h, x : x + w].copy()

    # (2) make mask
    points = points - points.min(axis=0)

    mask = np.zeros(croped.shape[:2], np.uint8)
    cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)

    # (3) do bit-op
    dst = cv2.bitwise_and(croped, croped, mask=mask)

    return dst
