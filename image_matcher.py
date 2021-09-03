import numpy as np
import cv2


def check_subscribed(image, template, threshold=0.65):
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    if loc == None:
        return False
    return loc[0].shape[0] > 0
